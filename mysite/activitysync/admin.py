# Activity admin page
from activitysync.models import Provider, Activity
from django.contrib import admin

admin.site.register(Provider)

class ActivityAdmin(admin.ModelAdmin):
    list_display = ('title', 'provider', 'published', 'link', 'pub_date')
    list_filter = ['pub_date', 'provider', 'username', 'published']
    search_fields = ['title', 'comments']
    date_hierarchy = 'pub_date'

admin.site.register(Activity, ActivityAdmin)

