from django.urls import path
from workshops import views

app_name = 'workshops'

urlpatterns = [
    path('', views.workshops_list, name='list'),
]