from django.urls import path
from landing import views

app_name = 'landing'

urlpatterns = [
    path('', views.home, name='home'),
    path('contact/', views.contact, name='contact'),
    path('dashbord/', views.dashbord, name='dashbord'),
]