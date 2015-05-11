from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    # Examples:
    url(r'^$', 'comments.views.home',name = 'home'),
    url(r'^like_category/$', 'comments.views.like_category', name='like_category'),
    url(r'^((?:\w|-)+)/submit/$','comments.views.submit', name='submit'),
    url(r'^((?:\w|-)+)/$', 'comments.views.news', name='news_id'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^admin/', include(admin.site.urls)),
]
