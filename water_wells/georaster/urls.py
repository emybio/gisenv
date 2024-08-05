from django.urls import path
from . import views,flaskapi

urlpatterns=[
    path("", views.georaster, name="index"),
    path('api/layers/', views.list_layers, name='list_layers'),
    
    
    ]