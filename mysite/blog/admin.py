# Blog application admin page
from mysite.blog.models import Entry, Activity
from django.contrib import admin

class EntryAdmin(admin.ModelAdmin):
    list_display = ('title', 'pub_date', 'published', 'mod_date')
    list_filter = ['pub_date', 'published']
    search_fields = ['title', 'body']
    date_hierarchy = 'pub_date'
    prepopulated_fields = {'slug': ('title',)}

admin.site.register(Entry, EntryAdmin)

class ActivityAdmin(admin.ModelAdmin):
    list_display = ('source', 'title', 'link', 'pub_date', 'published', 'username', 'author', 'comments')
    list_filter = ['pub_date', 'source', 'username']
    search_fields = ['title', 'comments']
    date_hierarchy = 'pub_date'

admin.site.register(Activity, ActivityAdmin)
