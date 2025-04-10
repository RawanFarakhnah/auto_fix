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
    
    # path('admin/manage_workshops/', views.manage_workshops, name='manage_workshops'),
    # path('admin/manage_workshop/create/', views.create_workshop, name='create_workshop'),
    # path('admin/manage_workshop/edit/', views.edit_workshop, name='edit_workshops'),
    # path('admin/manage_workshop/update/<int:id>/', views.update_workshop, name='update_workshop'),
    # path('admin/manage_workshop/delete/<int:id>/', views.delete_workshop, name='delete_workshop'),
    
    # path('admin/manage_service/', views.manage_services, name='manage_services'),
    
    # path('admin/manage_service/create/', views.create_service, name='create_service'),
    # path('admin/manage_service/edit/', views.edit_service, name='edit_service'),
    # path('admin/manage_service/update/<int:id>/', views.update_service, name='update_service'),
    # path('admin/manage_service/delete/<int:id>/', views.delete_service, name='delete_service'),

]
   

