from django.contrib import admin
from .models import Category, Pet

# A simple way to display more info in the admin list
class PetAdmin(admin.ModelAdmin):
    list_display = ('name', 'species', 'category', 'is_available')
    list_filter = ('category', 'is_available')

admin.site.register(Category)
admin.site.register(Pet, PetAdmin)

