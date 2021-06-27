from django.http import HttpResponse
from django.shortcuts import render, redirect
from .forms import ContactForm, CreateUserForm
from .models import Contact, Laptop, Mobile, Mobilecomment, Specification, Wishlist, MObiletrend, Laptoptrend, Laptopcomment
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.core.paginator import Paginator
from .scrap import scrapmobileviapages, scrapmobiledetail, scraplaptopshophive, scraplaptopmega, scraplaptopdetailmega
from .twitterApi import runtime_productgraph, runtime
from django.db.models import Q
import re
from django.http import JsonResponse

# Create your views here.


def home(request):
    print("Hello World")

    latest_mobile = Mobile.objects.all().filter(status="Upcoming")[:13]
    latestMobile1 = latest_mobile[0:6]
    latestMobile2 = latest_mobile[7:13]
    daily1 = MObiletrend.objects.get(brandName='#oppo', status="daily")
    daily2 = MObiletrend.objects.get(brandName='#vivo', status="daily")
    daily3 = MObiletrend.objects.get(brandName='#xiaomi', status="daily")
    daily4 = MObiletrend.objects.get(brandName='#Apple', status="daily")
    daily5 = MObiletrend.objects.get(brandName='#huawei', status="daily")
    daily6 = MObiletrend.objects.get(
        brandName='#teampixel', status="daily")
    daily7 = MObiletrend.objects.get(brandName='#OnePlus', status="daily")
    daily8 = MObiletrend.objects.get(
        brandName='smartphone #samsung', status="daily")
    dailyLap1 = Laptoptrend.objects.get(brandName='#dell', status="daily")
    dailyLap2 = Laptoptrend.objects.get(
        brandName='lenovo laptop', status="daily")
    dailyLap3 = Laptoptrend.objects.get(brandName='macbook', status="daily")
    dailyLap4 = Laptoptrend.objects.get(brandName='#hplaptop', status="daily")
    dailyLap5 = Laptoptrend.objects.get(
        brandName='#surfacebook', status="daily")
    dailyLap6 = Laptoptrend.objects.get(
        brandName='acer laptop', status="daily")
    dailyLap7 = Laptoptrend.objects.get(
        brandName='asus laptop', status="daily")
    dailyLap8 = Laptoptrend.objects.get(
        brandName='Msi laptop', status="daily")

    popularMobile = Mobile.objects.filter(status="popular")[:5]
    popularMac = Laptop.objects.filter(status="popular", brand="apple")[:5]
    popularLaptop = Laptop.objects.filter(
        status="popular").exclude(brand="apple")
    context = {"latestMobile1": latestMobile1, "latestMobile2": latestMobile2, "daily1": daily1, "daily2": daily2, "daily3": daily3, "daily4": daily4,
               "daily5": daily5, "daily6": daily6, "daily7": daily7, "daily8": daily8, "dailyLap1": dailyLap1, "dailyLap2": dailyLap2, "dailyLap3": dailyLap3, "dailyLap4": dailyLap4,
               "dailyLap5": dailyLap5, "dailyLap6": dailyLap6, "dailyLap7": dailyLap7, "dailyLap8": dailyLap8, "popularMobile": popularMobile, "popularMac": popularMac, "popularLaptop": popularLaptop}

    return render(request, "Trendz/index.html", context)


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


def trendMobile(request):
    context = {"daily": None}
    if request.method == "POST":
        if request.POST.get("weekly"):
            weekly1 = MObiletrend.objects.get(
                brandName='#oppo', status="weekly")
            weekly2 = MObiletrend.objects.get(
                brandName='#vivo', status="weekly")
            weekly3 = MObiletrend.objects.get(
                brandName='#xiaomi', status="weekly")
            weekly4 = MObiletrend.objects.get(
                brandName='#Apple', status="weekly")
            weekly5 = MObiletrend.objects.get(
                brandName='#huawei', status="weekly")
            weekly6 = MObiletrend.objects.get(
                brandName='#teampixel', status="weekly")
            weekly7 = MObiletrend.objects.get(
                brandName='#OnePlus', status="weekly")
            weekly8 = MObiletrend.objects.get(
                brandName='#samsung', status="weekly")
            context = {"weekly1": weekly1, "weekly2": weekly2, "weekly3": weekly3, "weekly4": weekly4,
                       "weekly5": weekly5, "weekly6": weekly6, "weekly7": weekly7, "weekly8": weekly8}
            print(context)
    else:
        daily1 = MObiletrend.objects.get(brandName='#oppo', status="daily")
        daily2 = MObiletrend.objects.get(brandName='#vivo', status="daily")
        daily3 = MObiletrend.objects.get(brandName='#xiaomi', status="daily")
        daily4 = MObiletrend.objects.get(brandName='#Apple', status="daily")
        daily5 = MObiletrend.objects.get(brandName='#huawei', status="daily")
        daily6 = MObiletrend.objects.get(
            brandName='#teampixel', status="daily")
        daily7 = MObiletrend.objects.get(brandName='#OnePlus', status="daily")
        daily8 = MObiletrend.objects.get(
            brandName='smartphone #samsung', status="daily")
        context = {"daily1": daily1, "daily2": daily2, "daily3": daily3, "daily4": daily4,
                   "daily5": daily5, "daily6": daily6, "daily7": daily7, "daily8": daily8}
        print(context)
    samsungMobiles = Mobile.objects.filter(
        brand="samsung_mobiles_prices")[:6]
    print(samsungMobiles)
    context.update({"samsungMobiles": samsungMobiles})

    return render(request, "Trendz/trendsMobile.html", context)


def trendLaptop(request):
    context = {"daily": None}
    if request.method == "POST":
        if request.POST.get("weekly"):
            weekly1 = Laptoptrend.objects.get(
                brandName='#dell', status="weekly")
            weekly2 = Laptoptrend.objects.get(
                brandName='lenovo laptop', status="weekly")
            weekly3 = Laptoptrend.objects.get(
                brandName='macbook', status="weekly")
            weekly4 = Laptoptrend.objects.get(
                brandName='#hplaptop', status="weekly")
            weekly5 = Laptoptrend.objects.get(
                brandName='#surfacebook', status="weekly")
            weekly6 = Laptoptrend.objects.get(
                brandName='acer laptop', status="weekly")
            weekly7 = Laptoptrend.objects.get(
                brandName='asus laptop', status="weekly")
            weekly8 = Laptoptrend.objects.get(
                brandName='Msi laptop', status="weekly")
            context = {"weekly1": weekly1, "weekly2": weekly2, "weekly3": weekly3, "weekly4": weekly4,
                       "weekly5": weekly5, "weekly6": weekly6, "weekly7": weekly7, "weekly8": weekly8}
    else:
        daily1 = Laptoptrend.objects.get(brandName='#dell', status="daily")
        daily2 = Laptoptrend.objects.get(
            brandName='lenovo laptop', status="daily")
        daily3 = Laptoptrend.objects.get(brandName='macbook', status="daily")
        daily4 = Laptoptrend.objects.get(brandName='#hplaptop', status="daily")
        daily5 = Laptoptrend.objects.get(
            brandName='#surfacebook', status="daily")
        daily6 = Laptoptrend.objects.get(
            brandName='acer laptop', status="daily")
        daily7 = Laptoptrend.objects.get(
            brandName='asus laptop', status="daily")
        daily8 = Laptoptrend.objects.get(
            brandName='Msi laptop', status="daily")
        context = {"daily1": daily1, "daily2": daily2, "daily3": daily3, "daily4": daily4,
                   "daily5": daily5, "daily6": daily6, "daily7": daily7, "daily8": daily8}
    return render(request, "Trendz/trendsLaptop.html", context)


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
    Brand = None
    if brand_name == "latest-phone":
        Query = Mobile.objects.all().filter(status="Upcoming").order_by('id')
        paginator = Paginator(Query, 20)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
    elif brand_name == "popular-phone":
        Query = Mobile.objects.all().filter(status="popular").order_by('id')
        paginator = Paginator(Query, 20)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
    else:
        Query = Mobile.objects.all().filter(brand=brand_name).order_by('id')
        for Obj in Query[:1]:
            Brand = Obj
        paginator = Paginator(Query, 20)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

    return render(request, "Trendz/devicelist.html", {'page_obj': page_obj, "Brand": Brand})


def phonedetailpage(request, device_name):

    context = scrapmobiledetail(device_name)
    mobile = Mobile.objects.get(tag=device_name)
    mobileGraph = runtime_productgraph(mobile.title)
    wishlist = Wishlist.objects.filter(mobile=mobile)
    comments = Mobilecomment.objects.filter(mobile=mobile, parent=None)
    replies = Mobilecomment.objects.filter(mobile=mobile).exclude(parent=None)
    context.update(
        {'comments': comments, 'mobile': mobile, 'replies': replies, "wishlist": wishlist, "mobileGraph": mobileGraph})
    return render(request, "Trendz/phonedetail.html", context)


def laptoplistpage(request, brand_name):

    query = Laptop.objects.all().filter(brand=brand_name).order_by('id')
    paginator = Paginator(query, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, "Trendz/devicelist.html", {'page_obj1': page_obj})


def laptopdetailpage(request, device_name):

    laptop = Laptop.objects.get(tag1=device_name)
    if laptop.site == "Mega":
        context = scraplaptopdetailmega(device_name)
    else:
        None
    print(laptop.id)
    wishlist = Wishlist.objects.filter(laptop=laptop)
    comments = Laptopcomment.objects.filter(laptop=laptop, parent=None)
    replies = Laptopcomment.objects.filter(laptop=laptop).exclude(parent=None)
    context.update({"wishlist": wishlist, "laptop": laptop,
                    "comments": comments, "replies": replies})

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
        if request.POST.get("mobileid"):
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
    if request.method == "POST":
        if request.POST.get("laptopid"):
            comment = request.POST.get("comment")
            user = request.user
            laptopid = request.POST.get("laptopid")
            laptop = Laptop.objects.get(id=laptopid)
            parentSrno = request.POST.get('parentSrno')

            if re.search('[a-zA-Z]', comment):
                if parentSrno == "":
                    comment = Laptopcomment(
                        comment=comment, user=user, laptop=laptop)
                    comment.save()
                    messages.success(
                        request, "Your Review has been posted successfully")

                else:
                    parent = Laptopcomment.objects.get(srno=parentSrno)
                    comment = Laptopcomment(
                        comment=comment, user=user, laptop=laptop, parent=parent)
                    comment.save()
                    messages.success(
                        request, f"Your replied to {parent.user.username}")
            else:
                messages.success(
                    request, "Please Write Comment Correctly")
            return redirect('laptopdetail', device_name=laptop.tag1)
    return redirect('home')


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
    wishlistLaptop = None
    wishlistMobile = None
    if request.user.is_authenticated:
        user = request.user
        wishlistLaptop = Wishlist.objects.filter(
            user=user).exclude(laptop=None)
        print(wishlistLaptop)
        wishlistMobile = Wishlist.objects.filter(
            user=user).exclude(mobile=None)
        print(wishlistMobile)
    return render(request, "Trendz/wishlist.html", {"wishlistLaptop": wishlistLaptop, "wishlistMobile": wishlistMobile})


def Report(request, Name):

    if Name == "Mobile":
        searchTerm = ['#oppo', '#vivo', '#xiaomi', 'Apple iphone',
                      '#huawei', '#teampixel', '#OnePlus', '#samsung']
        context = runtime(searchTerm)
        print(context)

    return render(request, "Trendz/Report.html", context)
