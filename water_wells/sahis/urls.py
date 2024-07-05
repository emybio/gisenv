from django.urls import path
from .views import sahis_kayit

urlpatterns = [
    path('kayit/', sahis_kayit, name='sahis_kayit'),
]
