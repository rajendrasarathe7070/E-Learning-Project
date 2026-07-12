from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from core.models import Note, PYQ, Syllabus  # यहाँ 'minor' का इस्तेमाल करें




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

class PYQSitemap(Sitemap):
    changefreq = "weekly"  # गूगल इस पेज को हर हफ्ते चेक करेगा
    priority = 0.7         # सर्च इंजन के लिए इस पेज की इम्पोर्टेंस (0.0 से 1.0)

    def items(self):
        # यह केवल उन्हीं PYQs को साइटमैप में लाएगा जिनका स्लग खाली नहीं है
        return PYQ.objects.filter(slug__isnull=False).exclude(slug='')

    def location(self, obj):
        return f"/pyq/{obj.slug}/"


class SyllabusSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.7

    def items(self):
        return Syllabus.objects.filter(slug__isnull=False, is_active=True).exclude(slug='')[:500]

    def location(self, obj):
        return f"/syllabus/{obj.slug}/"