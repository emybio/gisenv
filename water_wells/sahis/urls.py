from django.urls import path
from .views import sahis_create,sahis_delete,sahis_detail,sahis_list,sahis_update

urlpatterns = [
    path('', sahis_list, name='sahis_list'),
    path('<int:pk>/', sahis_detail, name='sahis_detail'),
    path('create/', sahis_create, name='sahis_create'),
    path('<int:pk>/update/', sahis_update, name='sahis_update'),
    path('<int:pk>/delete/', sahis_delete, name='sahis_delete'),
]
