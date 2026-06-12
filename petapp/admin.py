from django.contrib import admin
from django.core.mail import send_mail
from django.conf import settings
from .models import Category, Pet, PetImage, AdoptionApplication, ContactMessage, SiteSetting, Service, WorkingStep, AboutFeature, WhyChooseUsItem, BlogPost, Testimonial

class PetImageInline(admin.TabularInline):
    model = PetImage
    extra = 1

class PetAdmin(admin.ModelAdmin):
    list_display = ('name', 'species', 'category', 'is_available', 'date_added')
    list_filter = ('category', 'is_available', 'species')
    search_fields = ('name', 'species')
    inlines = [PetImageInline]

admin.site.register(Category)
admin.site.register(Pet, PetAdmin)

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'replied', 'created_at')
    readonly_fields = ('name', 'email', 'subject', 'message', 'created_at')
    fields = ('name', 'email', 'subject', 'message', 'admin_reply', 'replied', 'created_at')
    list_filter = ('replied',)

    def save_model(self, request, obj, form, change):
        if obj.admin_reply and not obj.replied:
            send_mail(
                subject=f"Reply from PetCare: {obj.subject}",
                message=obj.admin_reply,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[obj.email],
                fail_silently=True,
            )
            obj.replied = True
        super().save_model(request, obj, form, change)

@admin.register(AdoptionApplication)
class AdoptionApplicationAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'pet_name', 'status', 'replied', 'created_at')
    readonly_fields = ('name', 'email', 'phone', 'address', 'pet_name', 'message', 'created_at')
    fields = ('name', 'email', 'phone', 'address', 'pet_name', 'message', 'status', 'admin_reply', 'replied', 'created_at')
    list_filter = ('status', 'replied')
    search_fields = ('name', 'email')

    def save_model(self, request, obj, form, change):
        if obj.admin_reply and not obj.replied:
            send_mail(
                subject="Your Pet Adoption Application – PetCare",
                message=obj.admin_reply,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[obj.email],
                fail_silently=True,
            )
            obj.replied = True
        super().save_model(request, obj, form, change)

admin.site.register(SiteSetting)
admin.site.register(Service)
admin.site.register(WorkingStep)
admin.site.register(AboutFeature)
admin.site.register(WhyChooseUsItem)

@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'published', 'created_at')
    list_filter = ('published',)
    search_fields = ('title', 'content')
    prepopulated_fields = {'slug': ('title',)}

@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ('name', 'pet_name', 'featured', 'order')
    list_filter = ('featured',)

