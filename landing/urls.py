from django.urls import path
from landing import views

app_name = 'landing'

urlpatterns = [  
    path('', views.main, name='main'),
    path('contact/', views.contact, name='contact'),
    path('dashbord/', views.dashbord, name='dashbord'),
    path('admin/manage-users/', views.manage_users, name='manage_users'),
    
    # User Dashbord URLs
    path('user/dashboard/', views.user_dashboard, name='user_dashboard'),

    # User Dashbord URLs
    path('owner/dashboard/', views.owner_dashboard, name='owner_dashboard'),

    # Admin Dashboard URLs
    path('admin/dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin/manage-users/', views.manage_users, name='manage_users'),

    # CRUD API for Users
    path('api/users/create/', views.create_user, name='create_user'),
    path('update_user/<int:user_id>/', views.update_user_view, name='update_user_view'),
    path('update_user_api/<int:user_id>/', views.update_user_api, name='update_user_api'),
    path('api/users/<int:user_id>/delete/', views.delete_user, name='delete_user'),
]