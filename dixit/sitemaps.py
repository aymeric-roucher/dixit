from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from dixit.models import Author

class StaticSitemap(Sitemap):
    changefreq = "monthly"
    priority = 1.
    protocol = 'http'
 
    def items(self):
        return ['searchbar']
 
    def location(self, item):
        return reverse(item) #returning the static pages URL; home and contact us

class AuthorSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.8

    def items(self):
        return Author.objects.all().order_by('name')

    def location(self, obj):
        return reverse('author', kwargs={'name': obj.name})