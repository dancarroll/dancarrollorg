from django.conf.urls.defaults import *
from django.conf import settings
from mysite.blog.feeds import LatestEntriesFeed, LatestEntriesByTagFeed

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    # (r'^mysite/', include('mysite.foo.urls')),

    # Django administration
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^admin/(.*)', admin.site.root),
    
    
    #(r'^media/(?P<path>.*)$', 'django.views.static.serve',
    #    {'document_root': '/home/erunama/erunama.com/public/media/', 'show_indexes': True}),
    url(r'^activity/$', view='mysite.views.activity', name='main_activity'),
    (r'^blog/', include('mysite.blog.urls')),
    url(r'^shared/$', view='mysite.views.shared_items', name='main_shared_items'),
    
    # RSS feeds
	url(r'^feeds/latest/$', view=LatestEntriesFeed(), name='blog_entries_rss'),
    url(r'^feeds/tags/(?P<tag_name>[-\w]+)/$', view=LatestEntriesByTagFeed(), name='blog_tagged_rss'),
    
    #url(r'^$', view='mysite.views.index', name='main_index'),
    url(r'^test/$', view='mysite.views.index', name='main_index'),
)

if settings.DEBUG:
    from mysite.settings import MEDIA_ROOT, ADMIN_MEDIA_ROOT
    
    urlpatterns += patterns('',
        (r'^site-media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': MEDIA_ROOT,
             'show_indexes': True}),
        (r'^admin-media/(?P<path>.*)$', 'django.views.static.serve',
             {'document_root': ADMIN_MEDIA_ROOT, 'show_indexes': True}),
    )
