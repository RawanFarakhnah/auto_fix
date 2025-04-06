from django.urls import path
from landing import views

app_name = 'landing'

urlpatterns = [
    path('', views.root, name='root'),
    path('dashboard',views.dashboard,name='dashboard'),
    path('user',views.user,name='user'),
    path('add',views.add_user,name='add_user'),
    path('update/<int:user_id>',views.update_user,name='update_user'),
    path('booking/add',views. add_book,name='add_book'),
    path('booking',views.update_booking,name='update_booking'),
    path('workshop',views.list_workshop,name='workshop'),
    path('workshop/add',views.add_workshop,name='add_workshop'),
    path('review/add',views.add_review,name='add_review'),
    path('review/list',views.list_review,name='add_list'),
    path('review/adminr',views.admin_review,name='admin_review'),
    path('service/add',views.add_service,name='add_service'),
    path('service/list',views.list_service,name='list_services'),
    
]