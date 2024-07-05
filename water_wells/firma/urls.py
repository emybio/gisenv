from django.urls import path
from .views import firma_kayit

urlpatterns = [
    path('kayit/', firma_kayit, name='firma_kayit'),
]
