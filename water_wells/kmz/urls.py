from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from kmz import views

urlpatterns = [
    path('', views.kmz_home), 
    path('kml-display/',views.kml_display,name="kml-display"),
    path('api/get-kml-files/', views.get_kml_files, name='get_kml_files'),
    path('api/get-kml-data/', views.get_kml_data, name='get_kml_data'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
