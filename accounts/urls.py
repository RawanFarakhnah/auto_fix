from django.urls import path
from accounts import views

app_name = 'accounts'

urlpatterns = [
    path('register/', views.user_register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    
    path('profile/', views.profile, name='profile'),
    path('profile/update/', views.profile_update, name='profile_update'),
    path('profile/update/address/', views.update_address, name='update_address'),
    path('profile/change-password/', views.change_password, name='change_password'),
    path('profile/delete_account', views.delete_account, name="delete_account")
]