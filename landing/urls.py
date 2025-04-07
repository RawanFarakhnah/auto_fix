from django.urls import path
from landing import views

app_name = 'landing'

urlpatterns = [  
    path('', views.main, name='main'),
    path('contact/', views.contact, name='contact'),
    path('dashbord/', views.dashbord, name='dashbord'),

    # User Dashbord URLs
    path('user/dashboard/', views.user_dashboard, name='user_dashboard'),

    # User Dashbord URLs
    path('owner/dashboard/', views.owner_dashboard, name='owner_dashboard'),

    # Admin Dashboard URLs
    path('admin/dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin/manage-users/', views.manage_users, name='manage_users'),
]