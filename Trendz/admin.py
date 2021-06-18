from django.contrib import admin
from .models import Contact
from Trendz.models import Laptop, Specification, Mobile, Mobilespec, Mobilecomment, Wishlist
# Register your models here.
admin.site.register(Laptop)
admin.site.register(Specification)
admin.site.register((Mobile, Mobilecomment))
admin.site.register(Mobilespec)
admin.site.register(Wishlist)


@admin.register(Contact)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'email', 'message')
