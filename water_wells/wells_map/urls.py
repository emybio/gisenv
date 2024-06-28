from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('add_location/', views.add_location, name='add_location'),
    path('locations/', views.location_list, name='location_list'),
    path('georaster',views.georaster,name="georaster"),
    path('serverraster',views.serverraster,name="serverraster"),
    path('pngraster',views.pngraster,name="pngraster")
]
