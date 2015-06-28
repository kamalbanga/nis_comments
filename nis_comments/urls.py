from django.conf.urls import include, url
from comments.models import EmailUser as User
from django.contrib import admin
from tastypie.api import Api
from django.conf import settings
from django.conf.urls import include, patterns, url
from comments.api import CommentResource, UserResource, FollowResource, VoteResource
admin.autodiscover()

v1_api = Api(api_name = 'v1')
v1_api.register(UserResource())
v1_api.register(CommentResource())
v1_api.register(FollowResource())
v1_api.register(VoteResource())

urlpatterns = [
    url(r'^opinions/$', 'comments.views.get_opinions'),
    url(r'^opinions_without_cache/$', 'comments.views.get_opinions_without_cache'),
    url(r'^loaderio-5b4540e24d0a6151b10967817c468dc1/$', 'comments.views.loaderio'),
    url(r'^loaderio-7caad16f2def076a5d46aaf87651efd1/$', 'comments.views.loaderio2'),
    url(r'^loaderio-5fa909c94db66f8c75cdcf5c57fc3672/$', 'comments.views.loaderio3'),
    url(r'^register-by-token/(?P<backend>[^/]+)/$', 'comments.views.register_by_access_token'),
    url(r'^api/v1/register-by-token/(?P<backend>[^/]+)/$', 'comments.views.register_by_access_token'),
    url(r'^admin-panel/$', 'comments.views.admin_panel'),
    url(r'^admin-panel2/$', 'comments.views.admin_panel2'),
    url(r'^admin-panel/approve/$', 'comments.views.approve'),
    url(r'^admin-panel2/approve/$', 'comments.views.approve'),
    url(r'^admin-panel/allApprove/$', 'comments.views.allApprove'),
    url(r'^loadAllNews/$', 'comments.views.loadAllNews'),
    url(r'^silk/', include('silk.urls', namespace='silk')),
    url(r'^home/$', 'comments.sample_view.home'),
    url(r'^logout/$', 'comments.sample_view.logout'),
    url(r'^api/', include(v1_api.urls)),
    url(r'^$', 'comments.views.admin_panel2'),
    url(r'^allApprove/$', 'comments.views.allApprove'),
    url(r'^approve/$', 'comments.views.approve'),
    url(r'^approve/$', 'comments.views.approve'),
    url(r'^oauth2/', include('provider.oauth2.urls', namespace = 'oauth2')),
    url(r'^accounts/login/$', 'comments.views.login'),
    url(r'^login-view/$','comments.views.login_view'),
    url(r'^loggedin/$','comments.views.loggedin'),
    url(r'^accounts/logout/$', 'comments.views.logout'),
    url(r'^register/$','comments.views.register'),
    url(r'^admin/', include(admin.site.urls)),
    # url(r'^news/$', 'comments.views.news',name = 'home'),
    url(r'^vote/$', 'comments.views.vote', name='vote'),
    url(r'^delete/','comments.views.delete_comment', name='delete'),
    url(r'^edit-comment/','comments.views.edit_comment',name='edit'),
    url(r'^((?:\w|-)+)/submit/$','comments.views.submit', name='submit'),
    # url(r'^((?:\w|-)+)/$', 'comments.views.news', name='news_id'),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += patterns('',
        url(r'^__debug__/', include(debug_toolbar.urls)),
    )
