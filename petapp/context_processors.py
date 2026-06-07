from .models import SiteSetting, Service, WorkingStep, AboutFeature, WhyChooseUsItem

def site_settings(request):
    settings_dict = {}
    for s in SiteSetting.objects.all():
        settings_dict[s.key] = s.value
    return {
        'site_settings': settings_dict,
    }

def site_data(request):
    return {
        'all_services': Service.objects.all(),
        'all_working_steps': WorkingStep.objects.all(),
        'all_about_features': AboutFeature.objects.all(),
        'all_why_choose_us': WhyChooseUsItem.objects.all(),
    }
