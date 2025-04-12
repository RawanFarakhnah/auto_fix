from django.http import JsonResponse
from django.shortcuts import render, HttpResponse
from bookings.models import Notification


# Create your views here.
def bookings_list(request):
    return HttpResponse("workshops list")



def get_notifications(request):
    if request.user.is_authenticated:
        notifications = Notification.objects.filter(user=request.user, is_read=False).order_by('-created_at')
        data = [{"message": n.message, "id": n.id} for n in notifications]
        return JsonResponse({"notifications": data})
    
    return JsonResponse({"error": "Unauthorized"}, status=403)