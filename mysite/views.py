from django.http import Http404
from django.shortcuts import render_to_response
from django.template import RequestContext

from mysite.blog.models import Entry, Activity
from mysite.blog.paginator import InfinitePaginator
from blog.views import blog_entry_detail

def index(request):
    # This logic is to support theme detection by Windows Live Writer.
    # It needs to see the actual post display, but it stupidly goes to the main
    # blog page rather than the entry's URL. So, if we detect WLW's user agent,
    # let's just make the main index show the latest blog post.
    try:
        if request.META['HTTP_USER_AGENT'].find("Windows Live Writer") > -1:
            post = Entry.objects.published().order_by('-pub_date')[0]
            return blog_entry_detail(request, post.slug, post.pub_date.year, post.pub_date.month)
    except (KeyError, IndexError):
        pass

    return render_to_response('index.html',
                {'blog_entries': Entry.objects.published_for_list()[:2],
                 'activities': Activity.objects.published()[:5] },
                context_instance=RequestContext(request))

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
