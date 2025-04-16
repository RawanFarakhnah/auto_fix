from django.urls import path
from user_dashboard import views

app_name = 'user_dashboard'
urlpatterns = [  
   
    path('user/dashboard/', views.user_dashboard, name='dashboard'),
    path('user/profile', views.profile, name='profile'),
    
    path('user/vehicles', views.vehicles, name='vehicles'),
    path('user/vehicles/add_vehicle', views.add_vehicle, name='add_vehicle'),
    path('user/vehicles/edit/<int:vehicle_id>/', views.edit_vehicle, name='edit_vehicle'),
    path('user/vehicles/delete/<int:vehicle_id>/', views.delete_vehicle, name='delete_vehicle'),
    
    path('user/appointments', views.appointments, name='appointments'),
    path('user/appointments/add_appointment', views.add_appointment, name='add_appointment'),
    path('user/appointments/<int:appointment_id>/details/', views.appointment_details, name='appointment_details'),
    # path('user/appointments/edit/<int:appointment_id>/', views.edit_appointment, name='edit_appointment'),
    path('user/appointments/delete/<int:appointment_id>/', views.delete_appointment, name='delete_appointment'),
    path('user/appointments/get-workshop-services/<int:workshop_id>/', views.get_workshop_services, name='get_workshop_services'),

    path('user/services', views.services, name='services'),
    path('user/notifications', views.notifications, name='notifications'),
    path('user/notifications/mark-as-read/<int:notification_id>/', views.mark_notification_as_read, name='mark_notification_as_read'),
    path('user/notifications/mark-all-read/', views.mark_all_notifications_as_read, name='mark_all_notifications_as_read'),

    path('user/reviews', views.reviews, name='reviews')
]