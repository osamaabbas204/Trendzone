from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home",),
    path("compare-mobile", views.compareMobile, name="compareMobile"),
    path("compare-laptop", views.compareLaptop, name="compareLaptop"),
    path("trend-mobile", views.trendMobile, name="trend"),
    path("trend-laptop", views.trendLaptop, name="trendlaptop"),
    path("contact", views.contact, name="contact"),
    path('login', views.loginpage, name='login'),
    path('signup', views.signuppage, name='signup'),
    path('logout', views.logoutuser, name='logout'),
    path('mobile-detail/<device_name>',
         views.phonedetailpage, name='phonedetail'),
    path('phone/<brand_name>', views.devicelistpage, name='devicelist'),
    path('laptop/<brand_name>', views.laptoplistpage, name='laptoplist'),
    path('laptop-detail/<device_name>',
         views.laptopdetailpage, name='laptopdetail'),
    path("search/", views.searchview, name="search"),
    path('postcomment', views.postcomment, name="comment"),
    path('wishlistdata', views.wishlistdata, name="wishlistdata"),
    path('wishlist', views.wishlist, name="wishlist"),
    path('report/<Name>', views.Report, name="Report"),
]
