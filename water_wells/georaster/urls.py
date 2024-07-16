from django.urls import path
from . import views

urlpatterns=[
    path("", views.georaster, name="index"),
    
    
    ]