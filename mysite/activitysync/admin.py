# Activity admin page
from activitysync.models import Activity
from django.contrib import admin

class ActivityAdmin(admin.ModelAdmin):
    list_display = ('source', 'title', 'link', 'pub_date', 'published', 'username', 'author', 'comments')
    list_filter = ['pub_date', 'source', 'username']
    search_fields = ['title', 'comments']
    date_hierarchy = 'pub_date'

admin.site.register(Activity, ActivityAdmin)
