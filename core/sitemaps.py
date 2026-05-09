from django.contrib.sitemaps import Sitemap
from django.urls import reverse


class StaticViewSitemap(Sitemap):
    protocol = 'https'
    changefreq = 'monthly'
    priority = 0.8

    def items(self):
        return ['home', 'about', 'courses', 'testimonials', 'gallery', 'lets_connect']

    def location(self, item):
        return reverse(item)
