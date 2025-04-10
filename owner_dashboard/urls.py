from django.urls import path
from owner_dashboard import views

app_name = 'owner_dashboard'
urlpatterns = [  
   
    path('owner/dashboard/', views.owner_dashboard, name='dashboard'),
]