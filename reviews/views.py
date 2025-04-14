from django.shortcuts import render, HttpResponse

# Create your views here.
def reviews_list(request):
    return HttpResponse("reviews list")
def main(request):
    reviews = Review.objects.select_related('user', 'workshop', 'service').all()
    return render(request, 'landing/main.html', {'reviews': reviews})