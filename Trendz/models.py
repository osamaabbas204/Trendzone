from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now
# Create your models here.


class Contact(models.Model):

    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    message = models.TextField()


class Laptop(models.Model):
    title = models.CharField(max_length=250)
    price = models.CharField(max_length=50)
    image = models.CharField(max_length=200)
    tag1 = models.CharField(max_length=200)
    brand = models.CharField(max_length=50)
    site = models.CharField(max_length=50)
    status = models.CharField(max_length=50, null=True)

    def __str__(self):
        return self.title


class Specification(models.Model):
    laptop = models.OneToOneField(
        Laptop, on_delete=models.CASCADE, primary_key=True)
    tag = models.CharField(max_length=200)
    title = models.CharField(max_length=250)
    generation = models.CharField(max_length=200, null=True)
    processor = models.CharField(max_length=200, null=True)
    processor_speed = models.CharField(max_length=200, null=True)
    installed_ram = models.CharField(max_length=200, null=True)
    type_ofmemory = models.CharField(max_length=200, null=True)
    hard_drivesize = models.CharField(max_length=200, null=True)
    hard_drivespeed = models.CharField(max_length=200, null=True)
    optical_drive = models.CharField(max_length=200, null=True)
    type_ofopticaldrive = models.CharField(max_length=200, null=True)
    ssd = models.CharField(max_length=200, null=True)
    type_ofharddrive = models.CharField(max_length=200, null=True)
    dedicated_graphics = models.CharField(max_length=200, null=True)
    graphics_memory = models.CharField(max_length=200, null=True)
    type_ofgraphics_memory_shared = models.CharField(max_length=200, null=True)
    switchable_graphics = models.CharField(max_length=200, null=True)
    graphics_processor = models.CharField(max_length=200, null=True)
    backlight = models.CharField(max_length=200, null=True)
    screen_size = models.CharField(max_length=200, null=True)
    screen_surface = models.CharField(max_length=200, null=True)
    screen_resolution = models.CharField(max_length=200, null=True)
    touchscreen = models.CharField(max_length=200, null=True)
    color = models.CharField(max_length=200, null=True)
    fingerprint_reader = models.CharField(max_length=200, null=True)
    numeric_keyboard = models.CharField(max_length=200, null=True)
    backlit_keyboard = models.CharField(max_length=200, null=True)
    bluetooth = models.CharField(max_length=200, null=True)
    lan = models.CharField(max_length=200, null=True)
    speed = models.CharField(max_length=200, null=True)
    wireless_wifi = models.CharField(max_length=200, null=True)
    wifi_type = models.CharField(max_length=200, null=True)
    condition = models.CharField(max_length=200, null=True)
    usb = models.CharField(max_length=200, null=True)
    hdmi = models.CharField(max_length=200, null=True)
    camera = models.CharField(max_length=200, null=True)
    operating_system = models.CharField(max_length=200, null=True)
    manual = models.CharField(max_length=200, null=True)
    product_page = models.CharField(max_length=200, null=True)
    warranty = models.CharField(max_length=200, null=True)


class Mobile(models.Model):
    title = models.CharField(max_length=250)
    price = models.CharField(max_length=50)
    image = models.CharField(max_length=200)
    tag = models.CharField(max_length=200)
    brand = models.CharField(max_length=50)
    status = models.CharField(max_length=50)

    def __str__(self):
        return self.title


class Mobilespec(models.Model):
    mobile = models.OneToOneField(
        Mobile, on_delete=models.CASCADE, primary_key=True)
    title = models.CharField(max_length=250)
    tag = models.CharField(max_length=250)
    rating = models.IntegerField(null=True)
    camera = models.CharField(max_length=50, null=True)
    processor = models.CharField(max_length=50, null=True)
    internal_storage = models.CharField(max_length=50, null=True)
    battery = models.CharField(max_length=50, null=True)
    ram = models.CharField(max_length=50, null=True)
    display = models.CharField(max_length=50, null=True)
    color = models.CharField(max_length=50, null=True)


class Mobilecomment(models.Model):
    srno = models.AutoField(primary_key=True)
    comment = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    mobile = models.ForeignKey(Mobile, on_delete=models.CASCADE)
    parent = models.ForeignKey("self", on_delete=models.CASCADE, null=True)
    timestamp = models.DateTimeField(default=now)

    def __str__(self):
        return self.comment[0:15] + "..." + " by " + self.user.username


class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    mobile = models.ForeignKey(Mobile, on_delete=models.CASCADE, null=True)
    laptop = models.ForeignKey(Laptop, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.user.username + " Wished "


class MObiletrend(models.Model):

    brandName = models.CharField(max_length=50)
    status = models.CharField(max_length=50)
    positive = models.FloatField()
    negative = models.FloatField()
    neutral = models.FloatField()

    def __str__(self):
        return self.brandName + self.status + "Trends"


class Laptoptrend(models.Model):

    brandName = models.CharField(max_length=50)
    status = models.CharField(max_length=50)
    positive = models.FloatField()
    negative = models.FloatField()
    neutral = models.FloatField()

    def __str__(self):
        return self.brandName + self.status + "Trends"
