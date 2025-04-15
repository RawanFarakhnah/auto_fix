from django.shortcuts import render, HttpResponse

# Create your views here.
def reviews_list(request):
    return HttpResponse("reviews list")
