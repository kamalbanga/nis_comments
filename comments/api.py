from tastypie.resources import ModelResource, ALL, ALL_WITH_RELATIONS
from tastypie.constants import ALL
from tastypie import fields, http
from models import *
from tastypie.authentication import Authentication, BasicAuthentication
from tastypie.authorization import Authorization, DjangoAuthorization
from comments.models import EmailUser as User
from authenticate import OAuth20Authentication, OAuth20AuthenticationOpinions
from django.db import models, IntegrityError
from tastypie.exceptions import *
from provider.oauth2.models import Client
from django.core.cache import cache
from tastypie.cache import SimpleCache
from silk.profiling.dynamic import *
from datetime import datetime

class UserResource(ModelResource):
	class Meta:
		queryset = User.objects.all()
		resource_name = 'users'
		excludes = ['password', 'is_active', 'is_staff', 'is_superuser', 'source']
		allowed_methods = ['get']
		filtering = {
			'username': ALL_WITH_RELATIONS,
			'email': ALL_WITH_RELATIONS,
			'id': ALL_WITH_RELATIONS,
		}
		authentication = OAuth20Authentication()

	def dehydrate(self, bundle):
		del bundle.data['resource_uri']
		bundle.data['date_joined'] = bundle.data['date_joined'].strftime('%s')
		return bundle

class CommentResource(ModelResource):
	user = fields.ForeignKey(UserResource, 'user', full=True)

	class Meta:
		queryset = Comment.objects.filter(is_deleted=False)
		resource_name = 'opinions'
		always_return_data = True
		# cache = SimpleCache(timeout=100)
		authorization = Authorization() # permission to POST
		fields = ['text', 'upvotes', 'downvotes', 'resource_uri', 'user', 'created', 'last_edit', 'news_id', 'id', 'is_approved', 'is_deleted']
		filtering = {
			'user': ALL_WITH_RELATIONS,
			'news_id': ALL_WITH_RELATIONS,
			'id': ALL_WITH_RELATIONS,
			'is_approved': ALL_WITH_RELATIONS,
			'is_deleted': ALL_WITH_RELATIONS,
		}
		authentication = OAuth20AuthenticationOpinions() # this doesn't need authentication on GET reqeusts

	@silk_profile()
	def get_object_list(self, request):
		opinions = super(CommentResource, self).get_object_list(request).order_by('-created')
		return opinions

	def obj_update(self, bundle, **kwargs):
		if bundle.obj.user != bundle.request.user:
			raise ImmediateHttpResponse(response=http.HttpForbidden("Signed in user isn't the author of this opinion."))
		authentication = OAuth20Authentication()
		old_text = bundle.obj.text
		try:
			new_text = bundle.data['text']
		except KeyError:
			raise NotFound("Field 'text' not found")
		cmt = Comment.objects.get(id=kwargs['pk'])
		cmt.text = new_text
		cmt.save()
		bundle.obj = cmt
		Edit(cmt=cmt, old_text = old_text, new_text = new_text).save()
		return bundle

	def obj_create(self, bundle, **kwargs):
		try: 
			news_id = bundle.data['news_id']
		except KeyError:
			raise NotFound("The field 'news_id' is needed for opinion creation and it is not present in body.")
		user = bundle.request.user
		try:
			text = bundle.data['text']
		except KeyError:
			raise NotFound("The field 'text' of the opinion is needed for opinion creation")
		c = Comment(user=user, news_id=news_id, text=text)
		all_approved_obj = AllApproved.objects.filter(news_id=news_id)
		if all_approved_obj.exists():
			c.is_approved = all_approved_obj[0].all_approved
		try:
			c.save()
		except IntegrityError:
			raise ImmediateHttpResponse(response=http.HttpForbidden())
		bundle.obj = c
		return bundle

	def obj_delete(self, bundle, **kwargs):
		c = self.obj_get(bundle, **kwargs)
		Comment.objects.filter(uuid=c.uuid).update(is_deleted=True)

	@silk_profile()
	def dehydrate(self, bundle):
		del bundle.data['resource_uri']
		bundle.data['created'] = bundle.data['created'].strftime('%s')
		bundle.data['last_edit'] = bundle.data['last_edit'].strftime('%s')
		if bundle.request.user.is_authenticated():
			votes = Vote.objects.filter(user=bundle.request.user).filter(comment=bundle.obj)
			if len(votes) > 0:
				vote = Vote.objects.filter(user=bundle.request.user).get(comment=bundle.obj)
				vote_type = vote.vote_type
			else:
				vote_type = 0
			bundle.data['vote'] = vote_type
		return bundle

class FollowResource(ModelResource):
	follower = fields.ForeignKey(UserResource, 'follower')
	followed = fields.ForeignKey(UserResource, 'followed')

	def obj_create(self, bundle, **kwargs):
		try:
			follower_id = bundle.data['follower']
		except KeyError:
			raise NotFound("Field 'follower' not found")
		try:
			followed_id = bundle.data['followed']
		except KeyError:
			raise NotFound("Field 'followed' not found")
		follower = User.objects.get(id=follower_id)
		followed = User.objects.get(id=followed_id)
		f = Follow(follower=follower, followed=followed)
		follower.follow_count = follower.follow_count + 1
		followed.followed_count = followed.followed_count + 1
		follower.save()
		followed.save()
		f.save()
		bundle.obj = f
		return bundle

	class Meta:
		queryset = Follow.objects.all()
		resource_name = 'follow'
		always_return_data = True
		authorization = Authorization()

class VoteResource(ModelResource):
	user = fields.ForeignKey(UserResource, 'user')
	comment = fields.ForeignKey(CommentResource, 'comment')

	class Meta:
		queryset = Vote.objects.all()
		authorization = Authorization()
		authentication = OAuth20Authentication()
		resource_name = 'votes'
		fields = ['user', 'comment', 'vote_type', 'id']
		filtering = {
			'user': ALL_WITH_RELATIONS,
			'comment': ALL_WITH_RELATIONS,
		}

	def get_object_list(self, request):
		# cache.set('votes', Vote.objects.all())
		return Vote.objects.all()
		# return cache.get('votes')

	def dehydrate(self, bundle):
		bundle.data['comment'] = bundle.obj.comment.id
		bundle.data['user'] = bundle.obj.user.id
		# bundle.data['ts'] = bundle.data['ts'].strftime('%s')
		del bundle.data['resource_uri']
		return bundle

	def obj_create(self, bundle, **kwargs):
		try:
			c = Comment.objects.get(id=bundle.data['opinion'])
		except KeyError:
			raise NotFound("Field 'opinion' not found")
		try:
			current_vote_type = bundle.data['vote_type']
		except KeyError:
			raise NotFound("Field 'vote_type' not found")
		has_voted = len(Vote.objects.filter(user=bundle.request.user).filter(comment=c)) > 0
		if has_voted:
			existing_vote = Vote.objects.filter(user=bundle.request.user).get(comment=c)
			existing_vote_type = existing_vote.vote_type
			if current_vote_type == existing_vote_type:
				return bundle
			elif current_vote_type == 0:
				existing_vote.delete()
				if existing_vote_type == 1:
					c.upvotes = c.upvotes - 1
				else:
					c.downvotes = c.downvotes - 1
				c.save()
			else:
				if existing_vote_type == 1:
					c.upvotes = c.upvotes - 1
					c.downvotes = c.downvotes + 1
					existing_vote.vote_type = -1
				else:
					c.upvotes = c.upvotes + 1
					c.downvotes = c.downvotes - 1
					existing_vote.vote_type = +1
				existing_vote.save()
				c.save()
			return bundle
		if current_vote_type == 1:
			c.upvotes = c.upvotes + 1
		else:
			c.downvotes = c.downvotes + 1
		c.save()
		Vote(comment = c, user = bundle.request.user, vote_type = current_vote_type).save()
		return bundle