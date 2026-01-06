from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'), # The empty string '' represents the root URL
    path('adoption_process', views.adoption_process, name='adoption_process'),
]