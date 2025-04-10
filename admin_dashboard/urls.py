from django.urls import path
from admin_dashboard import views

app_name = 'admin_dashboard'
urlpatterns = [  
   
    path('admin/dashboard/', views.admin_dashboard, name='dashboard'),
    
    path('admin/manage-users/', views.manage_users, name='manage_users'),
    path('admin/manage-user/create/', views.create_user, name='create_user'),
    path('admin/manage-user/edit/<int:user_id>/', views.edit_user, name='edit_user'),
    path('admin/manage-user/update/<int:user_id>/', views.update_user, name='update_user'),
    path('admin/manage-user/delete/<int:user_id>/', views.delete_user, name='delete_user'),
    
    path('manage_workshops/', views.manage_workshops, name='manage_workshops'),
    path('manage_workshop/create/', views.create_workshop, name='create_workshop'),
    path('manage_workshop/edit/<int:id>', views.edit_workshop, name='edit_workshop'),
    path('manage_workshop/update/<int:id>/', views.workshop_update, name='workshop_update'),
    path('delete/<int:id>/', views.delete_workshop, name='delete_workshop'),
    path('manage_services/', views.manage_services, name='manage_services'),    
    path('manage_services/create/', views.service_create, name='service_create'),
    path('manage_services/edit/<int:id>/', views.edit_service, name='edit_service'),
    # path('admin/manage_service/update/<int:id>/', views.update_service, name='update_service'),
    path('services/delete/<int:service_id>/', views.delete_service, name='delete_service'),
]
   

