from django.shortcuts import render_to_response
from django.template import RequestContext
from mysite.blog.models import Entry, SharedItem, Activity

import feedparser

def index(request):
    return render_to_response('index.html',
                {'blog_entries': Entry.objects.published()[:3], 
                 'shared_items': SharedItem.objects.all()[:4],
                 'activities': Activity.objects.published()[:10] },
                context_instance=RequestContext(request))

def activity(request):
    return render_to_response('activity.html',
                {'activities': Activity.objects.published()[:50] },
                context_instance=RequestContext(request))

def shared_items(request):
    return render_to_response('shared_items.html',
                {'shared_items': SharedItem.objects.all()[:20] },
                context_instance=RequestContext(request))