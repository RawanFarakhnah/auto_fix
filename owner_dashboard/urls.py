from django.urls import path
from owner_dashboard import views

app_name = 'owner_dashboard'
urlpatterns = [  
    path('owner/dashboard/', views.dashboard, name='dashboard'),

    # Workshop Management
    path('owner/workshop/', views.workshop_management, name='workshop'),
    path('owner/workshop/edit/', views.edit_workshop, name='edit_workshop'),
    path('owner/workshop/change_image',views.change_image,name='change_image'),
    path('owner/workshop/delete/', views.delete_workshop, name='delete_workshop'),
    
    # Services Management
    path('owner/services/', views.services_management, name='services'),
    path('owner/services/add/', views.add_service, name='add_service'),
    path('owner/services/<int:service_id>/edit/', views.edit_service, name='edit_service'),
    path('owner/services/<int:service_id>/delete/', views.delete_service, name='delete_service'),

    # Bookings Management
    path('owner/bookings/', views.bookings_management, name='bookings'),
    path('owner/bookings/<int:booking_id>/update-status/', views.update_booking_status, name='update_booking_status'),
    path('owner/bookings/<int:booking_id>/confirm/',views.confirm_booking,name='confirm_booking'),
    path('owner/bookings/<int:booking_id>/cancel/',views.cancel_booking,name='cancel_booking'),
    path('owner/bookings/<int:booking_id>/complete/',views.complete_booking,name='complete_booking'),

    
    # Reviews Management
    path('owner/reviews/', views.reviews_management, name='reviews'),
    path('owner/reviews/<int:review_id>/reply/', views.reply_review, name='reply_review'),
    
    path('owner/notifications', views.notifications, name='notifications'),
    path('owner/notifications/mark-as-read/<int:notification_id>/', views.mark_notification_as_read, name='mark_notification_as_read'),
    path('owner/notifications/mark-all-read/', views.mark_all_notifications_as_read, name='mark_all_notifications_as_read'),

    
]