
from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import handler404,handler500

from wells_map import views



urlpatterns = [
    path('admin/', admin.site.urls),
    path('kuyu/', include('wells_map.urls')),
    #path('', include('leaflet.urls')),
    path('shape/', include('shape.urls')),
    path('projection/', include('projection.urls')),
    path('basvuru/', include('sahis.urls')),
    path('firma/', include('firma.urls')),
    path('pngraster/', include('pngraster.urls')),
    path('georaster/', include('georaster.urls')),
    path('serverraster/', include('serverraster.urls')),
    path('',include('users.urls')),
    path('kmz/',include('kmz.urls')),
    path('turkiye/',include('turkiye.urls')),]
# handler404 = views.custom_404
# handler500= views.custom_500
