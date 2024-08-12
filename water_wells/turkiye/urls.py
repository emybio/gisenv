from django.urls import path
from .views import get_ilceler, get_mahalleler, get_semtler,get_yerler


urlpatterns = [
    path('',get_yerler,name='get_yerler'),
    path("get_ilceler", get_ilceler, name="get_ilceler"),
    path("get_semtlet", get_semtler, name="get_semtler"),
    path("get_mahalleler", get_mahalleler, name="get_mahalleler"),
]
