from django.urls import path
from owner_dashboard import views

app_name = 'owner_dashboard'
urlpatterns = [  
    path('owner/dashboard/', views.dashboard, name='dashboard'),

    # Workshop Management
    path('owner/workshop/', views.workshop_management, name='workshop'),
    path('owner/workshop/edit/', views.edit_workshop, name='edit_workshop'),
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
    
    # Reviews Management
    path('owner/reviews/', views.reviews_management, name='reviews'),
    # path('owner/reviews/<int:review_id>/reply/', views.reply_review, name='reply_review'),
    
    ##------------------------------------------------------------------------------##
    #TODO: Make Sure To Implement New Logic Insted of This ..
    # path('owner/dashboard1/', views.owner_dashboard, name='dashboard1'),
    path('owner/manage_workshops/', views.manage_workshops, name='manage_workshops'),
    path('owner/manage_workshop/create/', views.create_workshop, name='create_workshop'),
    # path('owner/manage_workshop/edit/<int:id>', views.edit_workshop, name='edit_workshop'),
    path('owner/manage_workshop/update/<int:id>/', views.workshop_update, name='workshop_update'),
    # path('owner/manage_workshop/delete/<int:id>/', views.delete_workshop, name='delete_workshop'),


    # path('owner/services',views.services,name='services'),
    path('owner/manage_services/create/', views.service_create, name='service_create'),
    path('owner/manage_services/delete/<int:service_id>/', views.delete_service, name='delete_service'),


    path('owner/bookings',views.bookings,name='bookings'),
    path('owner/bookings/update/', views.update_booking, name='update_booking')
]