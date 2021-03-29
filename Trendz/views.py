from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
def home(request):
    return render(request, "Trendz/home.html")

def compare(request):
    return render(request, "Trendz/comp-product.html")
def trend(request):
    return render(request, "Trendz/top-trndz.html")
def rated(request):
    return render(request, "Trendz/rat-product.html")
def contact(request):
    return render(request, "Trendz/contact.html")
