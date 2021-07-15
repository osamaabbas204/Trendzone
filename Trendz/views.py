from django.http import HttpResponse
from django.shortcuts import render, redirect
from .forms import ContactForm, CreateUserForm
from .models import Contact, Laptop, Mobile, Mobilecomment, Specification, Wishlist, MObiletrend, Laptoptrend, Laptopcomment
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.core.paginator import Paginator
from .scrap import scrapmobileviapages, scrapmobiledetail, scraplaptopshophive, scraplaptopmega, scraplaptopdetailmega, scrapdetailPaklap, priceoye
from .twitterApi import runtime_productgraph, runtime
from django.db.models import Q
import re
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
import smtplib
from email.message import EmailMessage


# Create your views here.


def home(request):
    latest_mobile = Mobile.objects.all().filter(status="latest")[:13]
    print(latest_mobile)
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

    popularMobile = Mobile.objects.filter(status="popular")[:10]
    popularMac = Laptop.objects.filter(status="popular", brand="apple")
    popularLaptop = Laptop.objects.filter(
        status="popular").exclude(brand="apple")
    context = {"latestMobile": latest_mobile, "latestMobile1": latestMobile1, "latestMobile2": latestMobile2, "daily1": daily1, "daily2": daily2, "daily3": daily3, "daily4": daily4,
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
            if not laptop1obj:
                laptop1 = Laptop.objects.filter(title__icontains=lap1)[:1]
                for laptop in laptop1:
                    if laptop.site == "Mega":
                        scraplaptopdetailmega(laptop.tag1)
                    elif laptop.site == "Paklap":
                        scrapdetailPaklap(laptop.tag1)
                laptop1obj = Specification.objects.filter(
                    title__icontains=lap1)[:1]
                for obj in laptop1obj:
                    laptop1 = obj
            else:
                for obj in laptop1obj:
                    laptop1 = obj
        if not lap2 == '':
            laptop2obj = Specification.objects.filter(
                title__icontains=lap2)[:1]
            if not laptop2obj:
                laptop2 = Laptop.objects.filter(title__icontains=lap2)[:1]
                for laptop in laptop2:
                    if laptop.site == "Mega":
                        scraplaptopdetailmega(laptop.tag1)
                    elif laptop.site == "Paklap":
                        scrapdetailPaklap(laptop.tag1)
                laptop2obj = Specification.objects.filter(
                    title__icontains=lap2)[:1]
                for obj in laptop2obj:
                    laptop2 = obj
            else:
                for obj in laptop2obj:
                    laptop2 = obj
    return render(request, "Trendz/comp-Laptop.html", {"laptop1": laptop1, "laptop2": laptop2})


def trendMobile(request):
    context = {}
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
    apple = Mobile.objects.filter(
        brand="apple")[:6]
    vivo = Mobile.objects.filter(
        brand="vivo")[:6]
    oppo = Mobile.objects.filter(
        brand="oppo")[:6]
    print(samsungMobiles)
    context.update({"samsungMobiles": samsungMobiles,
                    "apple": apple, "oppo": oppo, "vivo": vivo})

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
        hp = Laptop.objects.filter(brand="hp")[:6]
        dell = Laptop.objects.filter(brand="dell")[:6]
        lenovo = Laptop.objects.filter(brand="lenovo")[:6]
        apple = Laptop.objects.filter(brand="apple")[:6]
        context.update({"hp": hp,
                        "dell": dell, "lenovo": lenovo, "apple": apple})
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
            messages.success(request, 'Thankyou for contacting us')
    else:
        fm = ContactForm()
    return render(request, "Trendz/contact.html", {'form': fm})


def loginpage(request):
    if not request.user.is_authenticated:
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
    else:
        return redirect('home')


def logoutuser(request):
    if request.user.is_authenticated:
        logout(request)
        return redirect('home')
    else:
        return redirect('home')


def signuppage(request):

    if not request.user.is_authenticated:
        form = CreateUserForm()
        if request.method == 'POST':
            form = CreateUserForm(request.POST)
            if form.is_valid():
                user = form.cleaned_data.get('username')
                if re.search('[a-zA-Z0-9]{7}', user):
                    form.save()
                    user = form.cleaned_data.get('username')
                    messages.success(
                        request, 'Account was created for ' + user)
                    return redirect('login')
                else:
                    messages.info(
                        request, 'Username must contain 7 characters and Do not contain Special Characters')
        context = {'form': form}
        return render(request, "Trendz/signup.html", context)
    else:
        return redirect('home')


def devicelistpage(request, brand_name):

    page_obj = None
    Brand = None
    if brand_name == "latest-phone":
        Query = Mobile.objects.all().filter(status="latest").order_by('id')
        paginator = Paginator(Query, 20)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        print(Query)
        return render(request, "Trendz/devicelist.html", {'page_obj': page_obj, "Brand": Brand})
    elif brand_name == "popular-phone":
        Query = Mobile.objects.all().filter(status="popular").order_by('id')
        paginator = Paginator(Query, 20)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, "Trendz/devicelist.html", {'page_obj': page_obj, "Brand": Brand})
    elif Mobile.objects.filter(brand=brand_name):
        Query = Mobile.objects.all().filter(brand=brand_name).order_by('id')
        for Obj in Query[:1]:
            Brand = Obj
            print(Brand.brand)
        paginator = Paginator(Query, 20)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, "Trendz/devicelist.html", {'page_obj': page_obj, "Brand": Brand})
    else:
        return redirect('home')


def phonedetailpage(request, device_name):
    if Mobile.objects.filter(tag=device_name):
        context = scrapmobiledetail(device_name)
        mobile = Mobile.objects.get(tag=device_name)
        price1 = priceoye(device_name)
        print(price1)
        mobileGraph = runtime_productgraph(mobile.title)
        wishlist = Wishlist.objects.filter(mobile=mobile)
        comments = Mobilecomment.objects.filter(mobile=mobile, parent=None)
        replies = Mobilecomment.objects.filter(
            mobile=mobile).exclude(parent=None)
        context.update(
            {'comments': comments, 'mobile': mobile, 'replies': replies, "wishlist": wishlist, "mobileGraph": mobileGraph, "price1": price1})
        return render(request, "Trendz/phonedetail.html", context)
    else:
        return redirect('home')


def laptoplistpage(request, brand_name):

    if Laptop.objects.filter(brand=brand_name):
        query = Laptop.objects.all().filter(brand=brand_name).order_by('id')
        for Obj in query[:1]:
            brandLap = Obj
            print(brandLap.brand)
        paginator = Paginator(query, 20)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, "Trendz/devicelist.html", {'page_obj1': page_obj, "brandLap": brandLap})
    else:
        return redirect('home')


def laptopdetailpage(request, device_name):
    if Laptop.objects.filter(tag1=device_name):
        laptop = Laptop.objects.get(tag1=device_name)
        title = laptop.title
        titleList = title.split()
        finalTitle = f"{titleList[0]} {titleList[1]} {titleList[2]}"
        laptopGraph = runtime_productgraph(finalTitle)
        if laptop.site == "Mega":
            context = scraplaptopdetailmega(device_name)
        elif laptop.site == "Paklap":
            context = scrapdetailPaklap(device_name)
        laptopSpecs = Specification.objects.get(tag=device_name)
        wishlist = Wishlist.objects.filter(laptop=laptop)
        comments = Laptopcomment.objects.filter(laptop=laptop, parent=None)
        replies = Laptopcomment.objects.filter(
            laptop=laptop).exclude(parent=None)
        context.update({"wishlist": wishlist, "laptop": laptop,
                        "comments": comments, "replies": replies, "laptopSpecs": laptopSpecs, "laptopGraph": laptopGraph})
        return render(request, 'Trendz/laptopdetail.html', context)
    else:
        return redirect('home')


def searchview(request):

    mobiles = None
    laptops = None
    search = request.GET.get('search')
    if search == "":
        mobiles = ""
        laptops = ''
    else:
        if "hp" in search:
            laptops = Laptop.objects.filter(
                Q(title__icontains=search))
        if re.search('[a-zA-Z0-9]{3}', search):
            if not search.isdigit():
                mobiles = Mobile.objects.filter(Q(title__icontains=search))
                laptops = Laptop.objects.filter(Q(title__icontains=search))
        if not mobiles:
            if not laptops:
                searchlist = search.split(" ")
                if len(searchlist) > 1:
                    for search1 in searchlist:
                        if "hp" in search1:
                            laptops = Laptop.objects.filter(
                                Q(title__icontains=search1))
                            continue
                        if re.search('[a-zA-Z0-9]{3}', search1):
                            if not search1.isdigit():
                                print(search1)
                                print(
                                    "-----------------------------------------------------------------------------------------------------------")
                                mobile1 = Mobile.objects.filter(
                                    Q(title__icontains=search1))
                                laptop1 = Laptop.objects.filter(
                                    Q(title__icontains=search1))
                                mobiles |= mobile1
                                laptops |= laptop1
                                print(mobiles)
                                print(laptops)
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


@login_required(login_url='login')
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
        context.update({"mobile": True})
        print(context)
    elif Name == "Laptop":
        searchTerm = ['#dell', 'lenovo laptop', 'macbook', '#hplaptop',
                      '#microsoft #laptop', 'acer laptop', 'asus laptop', 'Msi laptop']
        context = runtime(searchTerm)
        context.update({"laptop": True})
        print(context)

    return render(request, "Trendz/Report.html", context)


def email_notification(subject, body, to):
    msg = EmailMessage()
    msg.set_content(body)
    msg['subject'] = subject
    msg['to'] = to
    sender_email = "webtrendzone2021@gmail.com"
    msg['from'] = sender_email
    password = "skype97531"
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(sender_email, password)
    server.send_message(msg)

    server.quit()


def email():
    userList = User.objects.all()
    for user in userList:
        print("send Notification email to ", user.email)
        email_notification(
            "Notication!", f"hey {user.username}\nMarket Trendz on our Website are Updated Now.To check the latest Trendz Visit our Website Now\n", user.email)
