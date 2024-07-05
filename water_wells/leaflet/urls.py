from django.urls import path
from . import views
urlpatterns=[
 path('shp', views.shpView, name='shp6'),
    path('upload_shapefile/', views.upload_shapefile, name='upload_shapefile'),
    path('geojson/', views.geojson_view, name='geojson_view'),]   