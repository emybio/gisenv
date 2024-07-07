from django.urls import path
from .views import firma_list, firma_detail, firma_create, firma_update, firma_delete,firma_sahis_list

urlpatterns = [
    path('', firma_list, name='firma_list'),
    path('<int:pk>/', firma_detail, name='firma_detail'),
    path('create/', firma_create, name='firma_create'),
    path('<int:pk>/update/', firma_update, name='firma_update'),
    path('<int:pk>/delete/', firma_delete, name='firma_delete'),
     path('<int:pk>/sahislar/', firma_sahis_list, name='firma_sahis_list'),
]
