from tastypie.resources import ModelResource, ALL, ALL_WITH_RELATIONS
from tastypie.constants import ALL
from tastypie import fields
from models import *
# from tastypie.serializers import Serializer 
from tastypie.authentication import Authentication, BasicAuthentication, ApiKeyAuthentication
from tastypie.authorization import Authorization 
# from django.contrib.auth.models import User
from comments.models import EmailUser as User
from authenticate import OAuth20Authentication
# from django.contrib.auth.models import User
from django.db import models, IntegrityError
from tastypie.models import create_api_key, ApiKey
from tastypie.exceptions import *
from provider.oauth2.models import Client

models.signals.post_save.connect(create_api_key, sender=User)

class CreateUserResource(ModelResource):
	class Meta:
		allowed_methods = ['post']
		always_return_data = True
		# authentication = BasicAuthentication()
		authorization = Authorization()
		queryset = User.objects.all()
		resource_name = 'create_user'

	def obj_create(self, bundle, **kwargs):
		try:
			# email = bundle.data["user"]["email"]
			# username = bundle.data["user"]["username"]
			bundle = super(CreateUserResource, self).obj_create(bundle, **kwargs)
			bundle.obj.set_password(bundle.data.get('password'))
			bundle.obj.save()
			c = Client(user=bundle.obj, name='nis-opinions', client_type=1, url='http://nis-opinions.beanstalk.com')
			c.save()
			print "c.client_id = ", c.client_id, " c.client_secret = ", c.client_secret
			print "bundle.obj = ", bundle.obj
			print "dir(bundle.obj) = ", dir(bundle.obj), "type(bundle.obj) = ", type(bundle.obj)
			print "user passwd = ", bundle.obj.password
			print "ApiKey.objects.get(user=bundle.obj).key = ", ApiKey.objects.get(user=bundle.obj).key
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

class NewsResource(ModelResource):
	class Meta:
		queryset = News.objects.all()
		# resource_name = 'news'
		filtering = {
			'news_id': ALL_WITH_RELATIONS,
		}

class CommentResource(ModelResource):
	user = fields.ForeignKey(UserResource, 'user', full=True)
	news = fields.ForeignKey(NewsResource, 'news')

	class Meta:
		queryset = Comment.objects.filter(isDeleted=False)
		resource_name = 'comments'
		# serializer = Serializer()
		authorization = Authorization() # permission to POST
		fields = ['text', 'upvotes', 'downvotes', 'resource_uri', 'user', 'created', 'last_edit', 'uuid']
		filtering = {
			'user': ALL_WITH_RELATIONS,
			'news': ALL_WITH_RELATIONS,
		}
		# authentication = ApiKeyAuthentication()
		authentication = OAuth20Authentication()

	def obj_update(self, bundle, **kwargs):
		old_text = bundle.obj.text
		new_text = bundle.data['text']
		cmt = Comment.objects.get(uuid=bundle.data['uuid'])
		cmt.text = new_text
		cmt.save()
		Edit(cmt=cmt, old_text = old_text, new_text = new_text).save()
		return bundle

	def obj_delete(self, bundle, **kwargs):
		c = self.obj_get(bundle, **kwargs)
		Comment.objects.filter(uuid=c.uuid).update(isDeleted=True)

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
