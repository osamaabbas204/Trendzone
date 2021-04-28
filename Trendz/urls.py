from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home",),
    path("compare", views.compare, name="compare"),
    path("trend", views.trend, name="trend"),
    path("rated", views.rated, name="rated"),
    path("contact", views.contact, name="contact"),
    path('login', views.loginpage, name='login'),
    path('signup', views.signuppage, name='signup'),
    path('logout', views.logoutuser, name='logout'),
    path('detail/<device_name>', views.phonedetailpage, name='phonedetail'),
    path('phone/<brand_name>', views.devicelistpage, name='devicelist'),
]
