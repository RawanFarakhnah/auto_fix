from django.urls import path
from locations import views

app_name = 'locations'

urlpatterns = [
    path('', views.locations_list, name='list'),
]