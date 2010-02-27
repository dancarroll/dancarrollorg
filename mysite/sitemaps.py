from django.contrib.sitemaps import Sitemap
from datetime import datetime

class SectionSitemap(Sitemap):
    changefreq = 'daily'
    priority = 0.7
    
    page_dict = {
        'Home':'/',
        'Blog':'/blog/',
        'Activity':'/activity/',
    }
    
    def items(self):
        return self.page_dict.keys()
        
    def location(self, url):
        return self.page_dict[url]
        
    def lastmod(self, obj):
        return datetime.now()
