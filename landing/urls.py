from django.urls import path
from landing import views

app_name = 'landing'

urlpatterns = [
    path('', views.root, name='root'),
    path('dashboard',views.dashboard,name='dashboard'),
    path('user',views.user,name='user'),
    path('add',views.add_user,name='add_user'),
    
]