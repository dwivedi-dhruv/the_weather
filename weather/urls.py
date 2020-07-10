from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('1', views.add_city),
    path('2', views.remove_city),
]
