from tastypie.resources import ModelResource, ALL, ALL_WITH_RELATIONS
from tastypie.constants import ALL
from tastypie import fields
from models import *
from tastypie.serializers import Serializer 
from tastypie.authorization import Authorization 
from django.contrib.auth.models import User

class UserResource(ModelResource):
	class Meta:
		queryset = User.objects.all()
		resource_name = 'users'
		excludes = ['email', 'password', 'is_active', 'is_staff', 'is_superuser']
		filtering = {
			'username': ALL_WITH_RELATIONS,
		}

class NewsResource(ModelResource):
	class Meta:
		queryset = News.objects.all()
		resource_name = 'news'
		filtering = {
			'news_id': ALL_WITH_RELATIONS,
		}

class CommentResource(ModelResource):
	user = fields.ForeignKey(UserResource, 'user')
	news = fields.ForeignKey(NewsResource, 'news')

	class Meta:
		queryset = Comment.objects.all()
		resource_name = 'comments'
		# serializer = Serializer()
		authorization = Authorization() # permission to POST
		fields = ['text', 'upvotes', 'downvotes', 'resource_uri', 'user']
		filtering = {
			'user': ALL_WITH_RELATIONS,
			'news': ALL_WITH_RELATIONS,
		}