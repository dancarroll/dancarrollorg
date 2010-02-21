from django.conf.urls.defaults import *
from mysite.polls.models import Poll
from mysite.polls.feeds import LatestEntries

info_dict = {
    'queryset': Poll.objects.all(),
}

urlpatterns = patterns('',
    (r'^$', 'django.views.generic.list_detail.object_list', info_dict),
    url(r'^(?P<object_id>\d+)/$', 'django.views.generic.list_detail.object_detail', info_dict, 'poll_detail'),
    url(r'^(?P<object_id>\d+)/results/$', 'django.views.generic.list_detail.object_detail', dict(info_dict, template_name='polls/results.html'), 'poll_results'),
    (r'^(?P<poll_id>\d+)/vote/$', 'mysite.polls.views.vote'),
)

feeds = {
    'latest': LatestEntries,
}

urlpatterns += patterns('',
    (r'^feeds/(?P<url>.*)/$', 'django.contrib.syndication.views.feed', {'feed_dict': feeds}),
)
