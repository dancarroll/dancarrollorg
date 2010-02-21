from django.db import models
from django.contrib.syndication.feeds import Feed
from mysite.blog.managers import PublishedManager
from tagging.fields import TagField

import datetime
import tagging

class Category(models.Model):
    """Category model"""
    title = models.CharField('title', max_length=100)
    slug = models.SlugField('slug', unique=True)
    
    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'
        db_table = 'blog_categories'
        ordering = ('title',)
        
    def __unicode__(self):
        return u'%s' % self.title
        
    @models.permalink
    def get_absolute_url(self):
        return ('blog_category_detail', None, {'slug': self.slug})

class Entry(models.Model):
    title = models.CharField('title', max_length=200)
    snip = models.CharField('snip', max_length=500)
    slug = models.SlugField('slug', unique_for_date='pub_date')
    
    pub_date = models.DateTimeField('Date published',
                                    default=datetime.datetime.now)
    mod_date = models.DateTimeField('Date modified',
                                    default=datetime.datetime.now,
                                    auto_now=True)
    
    tags = TagField()
    categories = models.ManyToManyField(Category, blank=True)
    body = models.TextField()
    published = models.BooleanField(default=False)
    allow_comments = models.BooleanField(default=True)
    objects = PublishedManager()
    
    class Meta:
        verbose_name = 'entry'
        verbose_name_plural = 'entries'
        db_table = 'blog_entries'
        ordering = ('-pub_date',)
        get_latest_by = 'pub_date'
    
    
    def __unicode__(self):
        return u'%s' % self.title
        
    @models.permalink
    def get_absolute_url(self):
        return ('blog_entry_detail', None, {
                'year': self.pub_date.year,
                'month': self.pub_date.strftime('%b'),
                'day': self.pub_date.day,
                'slug': self.slug
            })
    
    def get_previous_entry(self):
        return self.get_previous_by_pub_date(published=True)
    
    def get_next_entry(self):
        return self.get_next_by_pub_date(published=True)

class SharedItem(models.Model):
    """Shared items from bookmarking websites (Google Reader, etc)."""
    SOURCE_CHOICES = (
        (1, 'Google Reader'),
    )
    
    title = models.CharField('title', max_length=200)
    link = models.URLField(max_length=500)
    source = models.IntegerField(choices=SOURCE_CHOICES, default=1)
    comments = models.TextField(blank=True)
    shared_by = models.CharField(max_length=20)
    pub_date = models.DateTimeField('Date published')
    guid = models.CharField(max_length=255, unique=True, db_index=True)
    
    class Meta:
        verbose_name = 'shared item'
        verbose_name_plural = 'shared items'
        db_table = 'blog_shareditems'
        ordering = ('-pub_date',)
        get_latest_by = 'pub_date'
    
    def __unicode__(self):
        return u'%s' % self.title

class Activity(models.Model):
    """Activity from social network (Twitter, Flickr, etc)."""
    SOURCE_CHOICES = (
        ('T', 'twitter'),
        ('DG', 'digg'),
        ('DL', 'delicious'),
        ('FB', 'facebook'),
        ('HU', 'hulu'),
        ('RD', 'reddit'),
    )
    
    title = models.CharField('title', max_length=200)
    link = models.URLField(max_length=500)
    source = models.CharField(max_length=2, choices=SOURCE_CHOICES)
    username = models.CharField(max_length=20, blank=True)
    author = models.CharField(max_length=20, blank=True)
    pub_date = models.DateTimeField('Date published')
    published = models.BooleanField(default=True)
    guid = models.CharField(max_length=255, unique=True, db_index=True)
    objects = PublishedManager()
    
    class Meta:
        verbose_name = 'activity'
        verbose_name_plural = 'activities'
        db_table = 'blog_activities'
        ordering = ('-pub_date',)
        get_latest_by = 'pub_date'
    
    def __unicode__(self):
        return u'%s' % self.title

    def get_activity_prefix(self):
        if self.source == 'DG':
            return u'Dugg '
        elif self.source == 'DL':
            return u'Bookmarked '
        elif self.source == 'HU':
            return u'Watched '
        elif self.source == 'RD':
            return u'Liked '
        else:
            return u''
    
    def get_network_link(self):
        if self.source == 'T':
            return u"http://twitter.com/erunama"
        elif self.source == 'DG':
            return u"http://digg.com/users/erunama"
        elif self.source == 'DL':
            return u"http://delicious.com/erunama"
        elif self.source == 'FB':
            return u"http://www.facebook.com/people/Dan-Carroll/401024"
        elif self.source == 'HU':
            return u"http://www.hulu.com/profiles/erunama/"
        elif self.source == 'RD':
            return u"http://www.reddit.com/user/erunama/"
