from django.conf.urls.defaults import *
from mysite.blog.models import Entry, Category
from mysite.blog import views as blog_views

urlpatterns = patterns('',
    url(r'^(?P<year>\d{4})/(?P<month>\d{1,2})/(?P<day>\d{1,2})/(?P<slug>[-\w]+)/$',
        view=blog_views.blog_entry_detail,
        name='blog_entry_detail'),

    url(r'^(?P<year>\d{4})/(?P<month>\d{1,2})/$',
        view=blog_views.blog_archive_month,
        name='blog_archive_month'),

    url(r'^(?P<year>\d{4})/$',
        view=blog_views.blog_archive_year,
        name='blog_archive_year'),
        
    url(r'^tags/(?P<slug>[-\w]+)/$',
        view=blog_views.tag_detail,
        name='blog_tag_detail'),

    url (r'^tags/$',
        view=blog_views.tag_list,
        name='blog_tag_list'),

    url (r'^search/$',
        view=blog_views.search,
        name='blog_search'),

    url(r'^page/(?P<page>\w)/$',
        view=blog_views.blog_entry_list,
        name='blog_index_paginated'),

    url(r'^$',
        view=blog_views.blog_entry_list,
        name='blog_index'),
        
    (r'^comments/', include('django.contrib.comments.urls')),
)


# info_dict = {
    # 'queryset': Entry.objects.all(),
    # 'date_field': 'pub_date',
# }

# urlpatterns = patterns('',
    # (r'^entry/(?P<object_id>\d+)/$', 'django.views.generic.list_detail.object_detail', dict(queryset=Entry.objects.all())),
# )

# urlpatterns += patterns('django.views.generic.date_based',
    # url(r'^(?P<year>\d{4})/(?P<month>\d{1,2})/(?P<day>\d{1,2})/(?P<slug>[-\w]+)/$', 'object_detail', dict(info_dict, month_format="%n", day_format="%j"), 'blog_entry'),
    # url(r'^(?P<year>\d{4})/(?P<month>\d{1,2})/(?P<day>\d{1,2})/$', 'archive_day', dict(info_dict, month_format="%n", day_format="%j"), 'blog_day'),
    # url(r'^(?P<year>\d{4})/(?P<month>\d{1,2})/$', 'archive_month', dict(info_dict, month_format="%n", allow_empty=True), 'blog_month'),
    # url(r'^(?P<year>\d{4})/$', 'archive_year', dict(info_dict, make_object_list=True), 'blog_year'),
    # url(r'^$', 'archive_index', info_dict, 'blog_list'),
# )

# urlpatterns += patterns('django.views.generic.list_detail',
    # url(r'^category/(?P<slug>[-\w]+)/$', 'object_detail', dict(queryset=Category.objects.all()), 'blog_category_detail'),
    # url(r'^category/$', 'object_list', dict(queryset=Category.objects.all()), 'blog_category_list'),
# )