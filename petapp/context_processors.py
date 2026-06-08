from .models import SiteSetting, Service, WorkingStep, AboutFeature, WhyChooseUsItem, Category, Pet

def site_settings(request):
    settings_dict = {}
    for s in SiteSetting.objects.all():
        settings_dict[s.key] = s.value
    return {
        'site_settings': settings_dict,
    }

def site_data(request):
    categories = Category.objects.all()
    nav_categories = []
    for cat in categories:
        breeds = list(Pet.objects.filter(category=cat).values_list('species', flat=True).distinct().order_by('species'))
        nav_categories.append({'name': cat.name, 'breeds': breeds})
    return {
        'all_services': Service.objects.all(),
        'all_working_steps': WorkingStep.objects.all(),
        'all_about_features': AboutFeature.objects.all(),
        'all_why_choose_us': WhyChooseUsItem.objects.all(),
        'nav_categories': nav_categories,
    }
