# Blog application admin page
from mysite.blog.models import Entry, SharedItem, Activity
from django.contrib import admin

class EntryAdmin(admin.ModelAdmin):
    list_display = ('title', 'pub_date', 'published')
    list_filter = ['pub_date', 'published']
    search_fields = ['title', 'body']
    date_hierarchy = 'pub_date'
    prepopulated_fields = {'slug': ('title',)}

admin.site.register(Entry, EntryAdmin)

class SharedItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'link', 'pub_date', 'shared_by', 'source')
    list_filter = ['pub_date', 'source', 'shared_by']
    search_fields = ['title', 'comments']
    date_hierarchy = 'pub_date'

admin.site.register(SharedItem, SharedItemAdmin)

class ActivityAdmin(admin.ModelAdmin):
    list_display = ('source', 'title', 'link', 'pub_date', 'published', 'username', 'author')
    list_filter = ['pub_date', 'source', 'username']
    search_fields = ['title']
    date_hierarchy = 'pub_date'

admin.site.register(Activity, ActivityAdmin)