from django.urls import path
from landing import views

app_name = 'landing'

urlpatterns = [  
    path('', views.main, name='main'),
    
    path('dashboard/', views.dashboard, name='dashboard'),
    path('send_contact_message/', views.send_contact_message, name='send_contact_message')
]