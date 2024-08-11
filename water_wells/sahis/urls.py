from django.urls import path
from .views import basvuru_create,basvuru_delete,basvuru_detail,basvuru_list,basvuru_update

urlpatterns = [
    path('', basvuru_list, name='basvuru_list'),
    path('<int:pk>/', basvuru_detail, name='basvuru_detail'),
    path('create/', basvuru_create, name='basvuru_create'),
    path('<int:pk>/update/', basvuru_update, name='basvuru_update'),
    path('<int:pk>/delete/', basvuru_delete, name='basvuru_delete'),
]
