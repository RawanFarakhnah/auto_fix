from django.urls import path
from admin_dashboard import views

app_name = 'admin_dashboard'
urlpatterns = [  
   
    path('admin/dashboard/', views.admin_dashboard, name='dashboard'),
    path('admin/profile/', views.profile, name='profile'),
    path('admin/profile/profile_update/', views.profile_update, name='profile_update'),
    path('admin/profile/update_address/', views.update_address, name='update_address'),
    path('admin/profile/change-password/', views.change_password, name='change_password'),

    path('admin/manage-users/', views.manage_users, name='manage_users'),
    path('admin/manage-user/create/', views.create_user, name='create_user'),
    path('admin/manage-user/edit/<int:user_id>/', views.edit_user, name='edit_user'),
    path('admin/manage-user/update/<int:user_id>/', views.update_user, name='update_user'),
    path('admin/manage-user/delete/<int:user_id>/', views.delete_user, name='delete_user'),
   
    path('admin/manage_workshops/', views.manage_workshops, name='manage_workshops'),
    path('admin/manage_workshop/create/', views.create_workshop, name='create_workshop'),
    path('admin/manage_workshop/edit/<int:id>', views.edit_workshop, name='edit_workshop'),
    path('admin/manage_workshop/update/<int:id>/', views.workshop_update, name='workshop_update'),
    path('admin/manage_workshop/delete/<int:id>/', views.delete_workshop, name='delete_workshop'),
    
    path('admin/manage_services/', views.manage_services, name='manage_services'),    
    path('admin/manage_services/create/', views.create_service, name='create_service'),    
    path('admin/manage_services/delete/<int:service_id>/', views.delete_service, name='delete_service'),
    path('admin/manage_services/update/<int:service_id>/', views.update_service, name='update_service'),
    path('admin/manage_services/edit/<int:service_id>/', views.edit_service, name='edit_service'),

    path('admin/notifications', views.notifications, name='notifications'),
    path('admin/notifications/mark-as-read/<int:notification_id>/', views.mark_notification_as_read, name='mark_notification_as_read'),
    path('admin/notifications/mark-all-read/', views.mark_all_notifications_as_read, name='mark_all_notifications_as_read'),
    
]

