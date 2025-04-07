from django.urls import path
from cars import views

app_name = 'cars'

urlpatterns = [
    path('', views.cars_list, name='list'),
]