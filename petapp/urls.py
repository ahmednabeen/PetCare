from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('adoption/', views.adoption_process, name='adoption_process'),
    path('category/<str:category_name>/', views.pet_list_view, name='pet_list'),
    path('pet/<int:pet_id>/', views.pet_detail_view, name='pet_detail'),
    path('api/load_more_categories/', views.load_more_categories, name='load_more_categories'),
    path("about/", views.about, name="about"),
    path("contact/", views.contact, name="contact"),
    path("services/", views.services, name="services"),
]