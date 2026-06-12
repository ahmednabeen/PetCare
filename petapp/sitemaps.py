from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from .models import Pet, Category, BlogPost

class PetSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.8

    def items(self):
        return Pet.objects.all()

    def lastmod(self, obj):
        return obj.date_added

class CategorySitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.7

    def items(self):
        return Category.objects.all()

class BlogSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.6

    def items(self):
        return BlogPost.objects.filter(published=True)

    def lastmod(self, obj):
        return obj.updated_at

class StaticSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.5

    def items(self):
        return ['home', 'about', 'contact', 'services', 'adoption_process', 'blog_list', 'testimonial_list']

    def location(self, item):
        return reverse(item)
