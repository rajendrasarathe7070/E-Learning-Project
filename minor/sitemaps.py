from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from core.models import Note, PYQ  # यहाँ 'minor' का इस्तेमाल करें



class StaticSitemap(Sitemap):
    priority = 0.8
    changefreq = 'weekly'
    def items(self):
        return ['index', 'notes', 'syllabus', 'books', 'pyq', 'doubts', 'profile', 'search']
    def location(self, item):
        return reverse(item)

class DynamicFilterSitemap(Sitemap):
    priority = 0.6
    changefreq = 'daily'
    def items(self):
        # Notes की जगह Note का इस्तेमाल
        return Note.objects.values('branch', 'semester').distinct().order_by('branch')
    def location(self, item):
        return f"/notes/?branch={item['branch']}&semester={item['semester']}"

class DetailSitemap(Sitemap):
    priority = 0.5
    changefreq = 'monthly'
    
    def items(self):
        return Note.objects.all()[:500]
    
    def location(self, item):
        # 'item.id' ki jagah 'item.slug' use karein
        return f"/notes/{item.slug}/"