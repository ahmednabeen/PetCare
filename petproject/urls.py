from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.sitemaps.views import sitemap
from petapp.sitemaps import PetSitemap, CategorySitemap, BlogSitemap, StaticSitemap

sitemaps = {
    'pets': PetSitemap,
    'categories': CategorySitemap,
    'blog': BlogSitemap,
    'static': StaticSitemap,
}

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('petapp.urls')),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='sitemap'),
    path('robots.txt', include('petapp.robots_urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = 'petapp.views.custom_404'
handler500 = 'petapp.views.custom_500'
