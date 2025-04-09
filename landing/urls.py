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
    path('create/', views.workshop_create, name='workshop_create'),
    path('edit/', views.edith, name='edit_workshops'),
    path('update/<int:id>/', views.workshop_update, name='workshop_update'),
    path('delete/<int:id>/', views.delete, name='delete'),
    path('list_workshop/',views.workshop_list,name='workshop_list'),
    path('services/', views.service_list, name='service_list'),
    path('services/create/', views.service_create, name='service_create'),
    path('services/update/<int:id>/', views.service_update, name='service_update'),
    path('services/delete/<int:id>/', views.service_delete, name='service_delete'),

]