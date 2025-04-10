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
]