from django.http import Http404
from django.shortcuts import render_to_response
from django.template import RequestContext

from activitysync.models import Activity
from activitysync.paginator import InfinitePaginator

def activity(request):
    type = request.GET.get('type', '')
    if type:
        activity_list = Activity.objects.published().filter(source__exact=type)
    else:
        activity_list = Activity.objects.published().defer("username", "author", "comments", "guid")

    # Make sure page request is an int.  If not, deliver first page.
    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1
    
    paginator = InfinitePaginator(activity_list, 25)
    try:
        activities = paginator.page(page)
    except:
        raise Http404
        
    return render_to_response('activity.html',
                activities.create_template_context(),
                context_instance=RequestContext(request))
