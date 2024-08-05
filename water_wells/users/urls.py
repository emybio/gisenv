from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .views import CustomLoginView, approve_user,index,register,logout_view

urlpatterns=[
    path('', index, name='index'),
   path('register/', register, name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),
    #path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', logout_view, name='logout'), 
    path('approve_user/<int:user_id>/', approve_user, name='approve_user'),
    
]
   