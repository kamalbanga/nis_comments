from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^accounts/login/$', 'comments.views.login'),
    url(r'^login-view/$','comments.views.login_view'),
    url(r'^loggedin/$','comments.views.loggedin'),
    url(r'^accounts/logout/$', 'comments.views.logout'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'comments.views.home',name = 'home'),
    url(r'^vote/$', 'comments.views.vote', name='vote'),
    url(r'^delete/','comments.views.delete_comment', name='delete'),
    url(r'^((?:\w|-)+)/submit/$','comments.views.submit', name='submit'),
    url(r'^((?:\w|-)+)/$', 'comments.views.news', name='news_id'),
    # url(r'^blog/', include('blog.urls')),
]
