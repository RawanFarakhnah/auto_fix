from django.urls import path
from ai_diagnosis import views

app_name = 'ai_diagnosis'

urlpatterns = [
    path('', views.ai_diagnosis_chat, name='ai_diagnosis_chat'),
]