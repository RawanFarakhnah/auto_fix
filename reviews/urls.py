from django.urls import path
from reviews import views

app_name = 'reviews'

urlpatterns = [
    path('', views.reviews_list, name='list'),
    path('', views.main, name='main'),
]