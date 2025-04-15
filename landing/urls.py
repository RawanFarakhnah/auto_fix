from django.urls import path
from landing import views

app_name = 'landing'

urlpatterns = [  
    path('', views.main, name='main'),
    path('contact/', views.contact, name='contact'),
    path('dashboard/', views.dashboard, name='dashboard'),
    # path('reviews/', views.reviews_list, name='reviews_list'),
]