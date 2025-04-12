from django.urls import path
from owner_dashboard import views

app_name = 'owner_dashboard'
urlpatterns = [  
    path('owner/dashboard/', views.owner_dashboard, name='dashboard'),
    
    path('owner/manage_workshops/', views.manage_workshops, name='manage_workshops'),
    path('owner/manage_workshop/create/', views.create_workshop, name='create_workshop'),
    path('owner/manage_workshop/edit/<int:id>', views.edit_workshop, name='edit_workshop'),
    path('owner/manage_workshop/update/<int:id>/', views.workshop_update, name='workshop_update'),
    path('owner/manage_workshop/delete/<int:id>/', views.delete_workshop, name='delete_workshop'),


    path('owner/services',views.services,name='services'),
    path('owner/manage_services/create/', views.service_create, name='service_create'),
    path('owner/manage_services/delete/<int:service_id>/', views.delete_service, name='delete_service'),


    path('owner/bookings',views.bookings,name='bookings'),
    path('owner/bookings/update/', views.update_booking, name='update_booking'),

]