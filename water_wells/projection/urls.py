from django.urls import path
from .views import proj,proj2

urlpatterns=[
path('projection', proj, name='projection'),
path('projection2', proj2, name='projection2'),
]
