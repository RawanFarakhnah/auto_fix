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
    path('owner/workshop/register/', views.register_workshop, name="register_workshop"),
    
    # Services Management
    path('owner/services/', views.services_management, name='services'),
    path('owner/services/add/', views.add_service, name='add_service'),
    path('owner/services/<int:service_id>/edit/', views.edit_service, name='edit_service'),
    path('owner/services/<int:service_id>/delete/', views.delete_service, name='delete_service'),

    # Bookings Management
    path('owner/bookings/', views.bookings_management, name='bookings'),
    path('owner/bookings/<int:booking_id>/update-status/', views.update_booking_status, name='update_booking_status'),
    path('owner/bookings/<int:booking_id>/confirm/',views.confirm_booking,name='confirm_booking'),
    path('owner/bookings/<int:booking_id>/confirm/',views.cancel_booking,name='cancel_booking'),
    path('owner/bookings/<int:booking_id>/confirm/',views.complete_booking,name='complete_booking'),

    
    # Reviews Management
    path('owner/reviews/', views.reviews_management, name='reviews'),
    # path('owner/reviews/<int:review_id>/reply/', views.reply_review, name='reply_review'),

    path('owner/bookings/update/', views.update_booking, name='update_booking')
]