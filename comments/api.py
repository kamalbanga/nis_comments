from tastypie.resources import ModelResource, ALL, ALL_WITH_RELATIONS
from tastypie.constants import ALL
from tastypie import fields, http
from models import *
# from tastypie.serializers import Serializer 
from tastypie.authentication import Authentication, BasicAuthentication, ApiKeyAuthentication
from tastypie.authorization import Authorization, DjangoAuthorization
# from django.contrib.auth.models import User
from comments.models import EmailUser as User
from authenticate import OAuth20Authentication, OAuth20AuthenticationOpinions
# from django.contrib.auth.models import User
from django.db import models, IntegrityError
from tastypie.models import create_api_key, ApiKey
from tastypie.exceptions import *
from provider.oauth2.models import Client

# models.signals.post_save.connect(create_api_key, sender=User)

class CreateUserResource(ModelResource):
	class Meta:
		allowed_methods = ['post']
		always_return_data = True
		# authentication = BasicAuthentication()
		authorization = Authorization()
		fields = ['email', 'resource_uri']
		# excludes = ['password', 'is_active', 'is_staff', 'is_superuser']
		queryset = User.objects.all()
		resource_name = 'create_user'

	def obj_create(self, bundle, **kwargs):
		print "in obj_create"
		try:
			# email = bundle.data["user"]["email"]
			# username = bundle.data["user"]["username"]
			bundle = super(CreateUserResource, self).obj_create(bundle, **kwargs)
			bundle.obj.set_password(bundle.data.get('password'))
			print "in createuser's create: bundle.obj = ", bundle.obj
			print "bundle.obj.password = ", bundle.obj.password
			bundle.obj.save()
			c = Client(user=bundle.obj, name='nis-opinions', client_type=1, url='http://nis-opinions.beanstalk.com')
			c.save()
			print "c.client_id = ", c.client_id, " c.client_secret = ", c.client_secret
			# print "bundle.obj = ", bundle.obj
			# print "dir(bundle.obj) = ", dir(bundle.obj), "type(bundle.obj) = ", type(bundle.obj)
			# print "user passwd = ", bundle.obj.password
			# print "ApiKey.objects.get(user=bundle.obj).key = ", ApiKey.objects.get(user=bundle.obj).key
		except IntegrityError:
			raise BadRequest('That username already exists')
		# return bundle
		return bundle #ApiKey.objects.get(user=bundle.obj).key

class UserResource(ModelResource):
	class Meta:
		queryset = User.objects.all()
		resource_name = 'users'
		excludes = ['password', 'is_active', 'is_staff', 'is_superuser']
		allowed_methods = ['get']
		filtering = {
			'username': ALL_WITH_RELATIONS,
			'email': ALL_WITH_RELATIONS,
		}
		# authentication = ApiKeyAuthentication() #OAuth20Authentication()
		authentication = OAuth20Authentication()

	def dehydrate(self, bundle):
		del bundle.data['resource_uri']
		return bundle

class NewsResource(ModelResource):
	class Meta:
		queryset = News.objects.all()
		# resource_name = 'news'
		filtering = {
			'news_id': ALL_WITH_RELATIONS,
		}

class CommentResource(ModelResource):
	user = fields.ForeignKey(UserResource, 'user', full=True)
	# news = fields.ForeignKey(NewsResource, 'news')

	class Meta:
		queryset = Comment.objects.filter(is_deleted=False)
		resource_name = 'opinions'
		always_return_data = True
		# serializer = Serializer()
		authorization = Authorization() # permission to POST
		fields = ['text', 'upvotes', 'downvotes', 'resource_uri', 'user', 'created', 'last_edit', 'news_slug', 'id', 'is_approved', 'is_deleted']
		filtering = {
			'user': ALL_WITH_RELATIONS,
			'news_slug': ALL_WITH_RELATIONS,
			'id': ALL_WITH_RELATIONS,
			'is_approved': ALL_WITH_RELATIONS,
			'is_deleted': ALL_WITH_RELATIONS,
		}
		# authentication = ApiKeyAuthentication()
		authentication = OAuth20AuthenticationOpinions() # this doesn't need authentication on GET reqeusts

	def get_object_list(self, request):
		print "in comment's get_obj_list"
		opinions = super(CommentResource, self).get_object_list(request).order_by('-created')
		# if is_a == 'None':
			# return opinions.filter(is_approved=None)
		return opinions
		# is_d = request.GET.get('is_deleted')
		# if is_d is not None:
		# 	if is_d == 'true':
		# 		is_d = True
		# 	else:
		# 		is_d = False
		# is_a = request.GET.get('is_approved')
		# if is_a is not None:
		# 	if is_a == 'true':
		# 		is_a = True
		# 	elif is_a == 'false':
		# 		is_a = False
		# 	else:
		# 		is_a = 'None'
		
		# if is_a == 'None':
		# 	if is_d is None:
		# 		return opinions.filter(is_approved=None)
		# 	else:
		# 		return opinions.filter(is_approved=None, is_deleted=is_d)
		# if is_d is None and is_a is None:
		# 	return opinions
		# elif is_d is None and is_a is not None:
		# 	return opinions.filter(is_approved=is_a)
		# elif is_d is not None and is_a is None:
		# 	return opinions.filter(is_deleted=is_d)
		# else:
		# 	return opinions.filter(is_deleted=is_d, is_approved=is_a)

	def obj_update(self, bundle, **kwargs):
		# print "bunble.obj = ", bundle.obj, " bundle.request = ", bundle.request
		print "bundle.obj.user = ", bundle.obj.user
		print "bundle.request.user = ", bundle.request.user
		print "bundle.obj.user != bundle.request.user = ", bundle.obj.user != bundle.request.user
		if bundle.obj.user != bundle.request.user:
			raise ImmediateHttpResponse(response=http.HttpForbidden())
		authentication = OAuth20Authentication()
		print "after auth"
		old_text = bundle.obj.text
		new_text = bundle.data['text']
		cmt = Comment.objects.get(uuid=bundle.data['uuid'])
		cmt.text = new_text
		cmt.save()
		Edit(cmt=cmt, old_text = old_text, new_text = new_text).save()
		return bundle

	def obj_create(self, bundle, **kwargs):
		news_slug = bundle.data['news_slug']
		user = bundle.request.user
		text = bundle.data['text']		
		print "news_slug = ", news_slug, "text = ", text
		c = Comment(user=user, news_slug=news_slug, text=text)
		try:
			c.save()
		except IntegrityError:
			raise ImmediateHttpResponse(response=http.HttpForbidden())
		bundle.obj = c
		return bundle

	def obj_delete(self, bundle, **kwargs):
		c = self.obj_get(bundle, **kwargs)
		Comment.objects.filter(uuid=c.uuid).update(is_deleted=True)

	# def dehydrate(self, bundle):
		# del bundle.data['resource_uri']
		# return bundle

class FollowResource(ModelResource):
	follower = fields.ForeignKey(UserResource, 'follower')
	followed = fields.ForeignKey(UserResource, 'followed')

	def obj_create(self, bundle, **kwargs):
		follower_id = bundle.data['follower']
		followed_id = bundle.data['followed']
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

	def dehydrate(self, bundle):
		bundle.data['comment'] = bundle.obj.comment.id
		bundle.data['user'] = bundle.obj.user.id
		del bundle.data['resource_uri']
		return bundle

	def obj_create(self, bundle, **kwargs):
		c = Comment.objects.get(id=bundle.data['comment'])	
		current_vote_type = bundle.data['vote_type']
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


	# def delete_detail(self, bundle, **kwargs):
		# return bundle.obj.user == bundle.request.user
		# print "self.get_object_list(request) = ", self.get_object_list(request)
		# print "request = ", request, " request.user = ", request.user
		# print "kwargs = ", kwargs, " dir(kwargs) = ", dir(kwargs)
		# print "self = ", self, " & self.user = ", self.user, " & dir(self.user) = ", dir(self.user)
		# print "bundle.obj = ", bundle.obj, " bundle.obj.user = ", bundle.obj.user, " bundle.request = ", bundle.request, " bundle.request.user = ", bundle.request.user
		# return False

	# def apply_authorization_limits(self, request, object_list):
		# print "object_list = ", object_list

	# def get_object_list(self, request):
	# 	print "in get_object_list = ", self.get_object_list(request).filter(pk=request.user.pk)
	# 	return self.get_object_list(request).filter(pk=request.user.pk)

	# def delete_detail(self, object_list, bundle):
		# print "bundle.obj.user = ", bundle.obj.user
		# print "bundle.request.user = ", bundle.request.user
		# return bundle.obj.user == bundle.request.user
