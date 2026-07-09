from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from .models import Notes, PYQ  # अगर Notes और PYQ api/models.py में हैं

class StaticSitemap(Sitemap):
    priority = 0.8
    changefreq = 'weekly'

    def items(self):
        # ये 'name' आपके urls.py में दिए गए नामों से मैच करने चाहिए
        return ['home', 'notes_list', 'syllabus', 'books', 'pyq_list', 'doubts', 'profile', 'search']

    def location(self, item):
        return reverse(item)


class DynamicFilterSitemap(Sitemap):
    priority = 0.6
    changefreq = 'daily'

    def items(self):
        # सारी Unique Branches और Semesters निकालें
        return Notes.objects.values('branch', 'semester').distinct().order_by('branch')

    def location(self, item):
        # item = {'branch': 'CS', 'semester': 5}
        return f"/notes/?branch={item['branch']}&semester={item['semester']}"


class DetailSitemap(Sitemap):
    priority = 0.5
    changefreq = 'monthly'

    def items(self):
        # सिर्फ 500 नोट्स (ताकि Sitemap बहुत बड़ा न हो)
        return Notes.objects.all()[:500]

    def location(self, item):
        return f"/notes/{item.id}/"