from django.conf.urls import include, url
# from django.contrib.auth.models import User
from comments.models import EmailUser as User
from django.contrib import admin
# from rest_framework import serializers, viewsets, routers
from tastypie.api import Api
from comments.api import CommentResource, UserResource, NewsResource, CreateUserResource, FollowResource, VoteResource
admin.autodiscover()

v1_api = Api(api_name = 'v1')
v1_api.register(UserResource())
v1_api.register(NewsResource())
v1_api.register(CommentResource())
v1_api.register(CreateUserResource())
v1_api.register(FollowResource())
v1_api.register(VoteResource())

# comment_resource = CommentResource()

# Serializers define the API representation.
# class UserSerializer(serializers.HyperlinkedModelSerializer):
#     class Meta:
#         model = User
#         fields = ('url', 'username', 'email', 'is_staff')


# ViewSets define the view behavior.
# class UserViewSet(viewsets.ModelViewSet):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer


# Routers provide a way of automatically determining the URL conf.
# router = routers.DefaultRouter()
# router.register(r'users', UserViewSet)

urlpatterns = [
    # url(r'^openid/', include('django_openid_auth.urls')),
    url(r'loaderio-60e1acefed2821f0dd26089f4126ca85/','comments.views.loaderio'),
    url(r'^api/', include(v1_api.urls)),
    url(r'^$', 'comments.views.home'),
    url(r'^oauth2/', include('provider.oauth2.urls', namespace = 'oauth2')),
    # url(r'^o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
    # url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^accounts/login/$', 'comments.views.login'),
    url(r'^login-view/$','comments.views.login_view'),
    url(r'^loggedin/$','comments.views.loggedin'),
    url(r'^accounts/logout/$', 'comments.views.logout'),
    url(r'^register/$','comments.views.register'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^news/$', 'comments.views.home',name = 'home'),
    url(r'^vote/$', 'comments.views.vote', name='vote'),
    url(r'^delete/','comments.views.delete_comment', name='delete'),
    url(r'^edit-comment/','comments.views.edit_comment',name='edit'),
    url(r'^((?:\w|-)+)/submit/$','comments.views.submit', name='submit'),
    url(r'^((?:\w|-)+)/$', 'comments.views.news', name='news_id'),
    # url(r'^blog/', include('blog.urls')),
]
