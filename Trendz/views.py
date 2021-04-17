from django.http import HttpResponse
from django.shortcuts import render, redirect
from .forms import ContactForm, CreateUserForm
from .models import Contact
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login ,logout

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
    if request.method == 'POST':
        fm = ContactForm(request.POST)
        if fm.is_valid():
            nm = fm.cleaned_data['name']
            em = fm.cleaned_data['email']
            ms = fm.cleaned_data['message']
            reg = Contact(name=nm, email=em, message=ms)
            reg.save()
            messages.success(request, 'Form submission successful')
    else:
        fm = ContactForm()
    return render(request, "Trendz/contact.html", {'form': fm})

def loginpage(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.info(request, 'Usrname or Password is incorrect ')

    context = {}
    return render(request,"Trendz/login.html", context)

def logoutuser(request):
    logout(request)
    return redirect('home')

def signuppage(request):


    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            
            user = form.cleaned_data.get('username')
            messages.success(request, 'Account was created for ' + user)

            return redirect('login')


    context = {'form':form}
    return render(request, "Trendz/signup.html", context)
