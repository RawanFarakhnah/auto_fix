from django.urls import path
from bookings import views

app_name = 'bookings'

urlpatterns = [
    path('', views.bookings_list, name='list'),
]