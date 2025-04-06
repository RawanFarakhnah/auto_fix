from django.shortcuts import render, HttpResponse

# Create your views here.
def locations_list(request):
    return HttpResponse("workshops list")