from django.contrib.sitemaps import Sitemap
from django.urls import reverse

class StaticSitemap(Sitemap):
    changefreq = "monthly"
    priority = 1.
    protocol = 'http'
 
    def items(self):
        return ['searchbar', 'author']
 
    def location(self, item):
        return reverse(item) #returning the static pages URL; home and contact us