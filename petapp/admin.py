from django.contrib import admin
from django.core.mail import send_mail
from django.conf import settings
from .models import Category, Pet, AdoptionApplication, ContactMessage, SiteSetting, Service, WorkingStep, AboutFeature, WhyChooseUsItem


class PetAdmin(admin.ModelAdmin):
    list_display = ('name', 'species', 'category', 'is_available')
    list_filter = ('category', 'is_available')

admin.site.register(Category)
admin.site.register(Pet, PetAdmin)


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'replied', 'created_at')
    readonly_fields = ('name', 'email', 'subject', 'message', 'created_at')

    fields = (
        'name',
        'email',
        'subject',
        'message',
        'admin_reply',
        'replied',
        'created_at',
    )

    def save_model(self, request, obj, form, change):
        if obj.admin_reply and not obj.replied:
            send_mail(
                subject=f"Reply from PetCare: {obj.subject}",
                message=obj.admin_reply,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[obj.email],
            )
            obj.replied = True
        super().save_model(request, obj, form, change)

@admin.register(AdoptionApplication)
class AdoptionApplicationAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'pet_name', 'replied', 'created_at')
    readonly_fields = (
        'name',
        'email',
        'phone',
        'address',
        'pet_name',
        'message',
        'created_at',
    )

    fields = (
        'name',
        'email',
        'phone',
        'address',
        'pet_name',
        'message',
        'admin_reply',
        'replied',
        'created_at',
    )

    def save_model(self, request, obj, form, change):
        if obj.admin_reply and not obj.replied:
            send_mail(
                subject="Your Pet Adoption Application – PetCare",
                message=obj.admin_reply,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[obj.email],
            )
            obj.replied = True
        super().save_model(request, obj, form, change)

admin.site.register(SiteSetting)
admin.site.register(Service)
admin.site.register(WorkingStep)
admin.site.register(AboutFeature)
admin.site.register(WhyChooseUsItem)
