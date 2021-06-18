from django.http import HttpResponse
from django.shortcuts import render, redirect
from .forms import ContactForm, CreateUserForm
from .models import Contact, Laptop, Mobile, Mobilecomment, Specification, Wishlist
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.core.paginator import Paginator
from .scrap import scrapmobileviapages, scrapmobiledetail, scraplaptopshophive, scraplaptopmega, scraplaptopdetailmega
from django.db.models import Q
import re
from django.http import JsonResponse

# Create your views here.


def home(request):

    latest_mobile = Mobile.objects.all().filter(status="Upcoming")[:10]

    return render(request, "Trendz/index.html", {"latest_mobile": latest_mobile})


def compareMobile(request):
    phone1data = None
    phone2data = None
    if request.GET.get('phone1') or request.GET.get('phone2'):
        phone1 = request.GET.get('phone1')
        phone2 = request.GET.get('phone2')
        if not phone1 == "":
            phone1obj = Mobile.objects.filter(title__icontains=phone1)[:1]
            print(phone1obj)
            if phone1obj:
                for obj in phone1obj:
                    tag1 = obj.tag
                phone1data = scrapmobiledetail(tag1)
        if not phone2 == "":
            phone2obj = Mobile.objects.filter(title__icontains=phone2)[:1]
            if phone2obj:
                for obj in phone2obj:
                    tag2 = obj.tag
                phone2data = scrapmobiledetail(tag2)
    return render(request, "Trendz/comp-Mobile.html", {'phone1': phone1data, 'phone2': phone2data})


def compareLaptop(request):
    laptop1 = None
    laptop2 = None
    if request.GET.get('laptop1') or request.GET.get('laptop2'):
        lap1 = request.GET.get('laptop1')
        lap2 = request.GET.get('laptop2')
        print(lap1, lap2)
        if not lap1 == '':
            laptop1obj = Specification.objects.filter(
                title__icontains=lap1)[:1]
            for obj in laptop1obj:
                laptop1 = obj
                print(obj.title)
        if not lap2 == '':
            laptop2obj = Specification.objects.filter(
                title__icontains=lap2)[:1]
            print(laptop2obj)
            for obj in laptop2obj:
                laptop2 = obj
                print(obj.title)
    return render(request, "Trendz/comp-Laptop.html", {"laptop1": laptop1, "laptop2": laptop2})


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
    return render(request, "Trendz/login.html", context)


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

    context = {'form': form}
    return render(request, "Trendz/signup.html", context)


def devicelistpage(request, brand_name):

    page_obj = None
    if brand_name == "latest-phone":
        Query = Mobile.objects.all().filter(status="Upcoming").order_by('id')
        paginator = Paginator(Query, 20)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
    else:
        if not request.GET.get('page'):
            scrapmobileviapages(brand_name)

        Query = Mobile.objects.all().filter(brand=brand_name).order_by('id')
        paginator = Paginator(Query, 20)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

    return render(request, "Trendz/devicelist.html", {'page_obj': page_obj})


def phonedetailpage(request, device_name):

    context = scrapmobiledetail(device_name)
    mobile = Mobile.objects.get(tag=device_name)
    wishlist = Wishlist.objects.filter(mobile=mobile)
    comments = Mobilecomment.objects.filter(mobile=mobile, parent=None)
    replies = Mobilecomment.objects.filter(mobile=mobile).exclude(parent=None)
    context.update(
        {'comments': comments, 'mobile': mobile, 'replies': replies, "wishlist": wishlist})
    return render(request, "Trendz/phonedetail.html", context)


def laptoplistpage(request, brand_name):
    if not request.GET.get('page'):
        scraplaptopmega(brand_name)

    query = Laptop.objects.all().filter(brand=brand_name).order_by('id')
    paginator = Paginator(query, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, "Trendz/devicelist.html", {'page_obj1': page_obj})


def laptopdetailpage(request, device_name):

    context = scraplaptopdetailmega(device_name)
    laptop = Laptop.objects.get(tag1=device_name)
    wishlist = Wishlist.objects.filter(laptop=laptop)
    context.update({"wishlist": wishlist, "laptop": laptop})

    return render(request, 'Trendz/laptopdetail.html', context)


def searchview(request):

    search = request.GET.get('search')
    if search == "":
        mobiles = ""
        laptops = ''
    else:
        mobiles = Mobile.objects.filter(Q(title__icontains=search))

        laptops = Laptop.objects.filter(Q(title__icontains=search))
    print(mobiles)
    return render(request, 'Trendz/search.html', {'mobiles': mobiles, 'laptops': laptops})


def postcomment(request):
    if request.method == "POST":
        comment = request.POST.get("comment")
        user = request.user
        mobileid = request.POST.get("mobileid")
        mobile = Mobile.objects.get(id=mobileid)
        parentSrno = request.POST.get('parentSrno')

        if re.search('[a-zA-Z]', comment):
            if parentSrno == "":
                comment = Mobilecomment(
                    comment=comment, user=user, mobile=mobile)
                comment.save()
                messages.success(
                    request, "Your Review has been posted successfully")

            else:
                parent = Mobilecomment.objects.get(srno=parentSrno)
                comment = Mobilecomment(
                    comment=comment, user=user, mobile=mobile, parent=parent)
                comment.save()
                messages.success(
                    request, f"Your replied to {parent.user.username}")
        else:
            messages.success(
                request, "Please Write Comment Correctly")
    return redirect('phonedetail', device_name=mobile.tag)


def wishlistdata(request):
    if request.POST.get('Mobile'):
        if request.method == "POST":
            user = request.user
            mobileid = request.POST.get('Mobile')
            mobile = Mobile.objects.get(id=mobileid)
            checkWishlist = Wishlist.objects.filter(mobile=mobile)
            if not checkWishlist:
                wishlist = Wishlist(user=user, mobile=mobile)
                wishlist.save()
                data = {
                    "msg": "Data has been POSTED!",
                }
            else:
                wishlist = Wishlist.objects.get(mobile=mobile, user=user)
                wishlist.delete()
                data = {
                    "msg": "Data has been Deleted",
                }
    else:
        if request.method == "POST":
            user = request.user
            laptopid = request.POST.get('Laptop')
            laptop = Laptop.objects.get(id=laptopid)
            checkWishlist = Wishlist.objects.filter(laptop=laptop)
            if not checkWishlist:
                wishlist = Wishlist(user=user, laptop=laptop)
                wishlist.save()
                data = {
                    "msg": "Data has been POSTED!",
                }
            else:
                wishlist = Wishlist.objects.get(laptop=laptop, user=user)
                wishlist.delete()
                data = {
                    "msg": "Data has been Deleted",
                }
    return JsonResponse(data)


def wishlist(request):
    if request.user.is_authenticated:
        user = request.user
        wishlist = Wishlist.objects.filter(user=user)
    return render(request, "Trendz/wishlist.html", {"wishlist": wishlist})
