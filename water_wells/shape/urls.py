from django.urls import path
from .views import geojson_view,shpView,upload_shapefile,ConvertShpToGeoJSON

urlpatterns=[
 path('shp', shpView, name='shp'),
    path('upload_shapefile/', upload_shapefile, name='upload_shapefile'),
    path('geojson/<str:shp_filename>/', geojson_view, name='geojson_view'),]
