import time
from django.core.cache import cache
from .models import SiteSetting, Service, WorkingStep, AboutFeature, WhyChooseUsItem, Category, Pet, BlogPost, Testimonial

CACHE_TTL = 300

def site_settings(request):
    settings_dict = cache.get('site_settings_dict')
    if settings_dict is None:
        settings_dict = {}
        for s in SiteSetting.objects.all():
            settings_dict[s.key] = s.value
        cache.set('site_settings_dict', settings_dict, CACHE_TTL)
    return {'site_settings': settings_dict}

def site_data(request):
    data = cache.get('site_data')
    if data is None:
        categories = Category.objects.all()
        nav_categories = []
        for cat in categories:
            breeds = list(
                Pet.objects.filter(category=cat)
                .values_list('species', flat=True)
                .distinct()
                .order_by('species')
            )
            nav_categories.append({'name': cat.name, 'breeds': breeds})
        data = {
            'all_services': list(Service.objects.all()),
            'all_working_steps': list(WorkingStep.objects.all()),
            'all_about_features': list(AboutFeature.objects.all()),
            'all_why_choose_us': list(WhyChooseUsItem.objects.all()),
            'all_blog_posts': list(BlogPost.objects.filter(published=True)),
            'all_testimonials': list(Testimonial.objects.filter(featured=True)),
            'nav_categories': nav_categories,
            'static_version': int(time.time()),
        }
        cache.set('site_data', data, CACHE_TTL)
    return data
