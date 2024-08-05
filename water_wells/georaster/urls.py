from django.urls import path
from . import views,flaskapi

urlpatterns=[
    path("", views.georaster, name="georaster"),
    path('api/layers/', views.list_layers, name='list_layers'),
    
    
    ]