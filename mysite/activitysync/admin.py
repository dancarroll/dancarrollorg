# Activity admin page
from activitysync.models import Activity
from django.contrib import admin

class ActivityAdmin(admin.ModelAdmin):
    list_display = ('source', 'title', 'published', 'link', 'pub_date')
    list_filter = ['pub_date', 'source', 'username', 'published']
    search_fields = ['title', 'comments']
    date_hierarchy = 'pub_date'

admin.site.register(Activity, ActivityAdmin)

