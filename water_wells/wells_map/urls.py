from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('add_location/', views.add_location, name='add_location'),
    path('locations/', views.location_list, name='location_list'),
    path('georaster',views.georaster,name="georaster"),
    path('serverraster',views.serverraster,name="serverraster"),
    path('pngraster',views.pngraster,name="pngraster"),
    path('get_locations/', views.get_locations, name='get_locations'),
    path('update_coordinates_to_utm/', views.update_coordinates_to_utm, name='update_coordinates_to_utm'),
    path('locations/edit/<int:pk>/', views.edit_location, name='edit_location'),
    path('locations/delete/<int:pk>/', views.delete_location, name='delete_location'),   
    path('map/', views.map_view, name='map_view'),
    path('projection/', views.projection, name='projection'),
    path('projection2/', views.projection2, name='projection2'),
   
]
