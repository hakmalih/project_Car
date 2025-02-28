
from django.contrib import admin

from main.models import Car,Brand, CarImage,Color,Shop

# Register your models here.
admin.site.register(Car)
admin.site.register(Brand)
admin.site.register(CarImage)
admin.site.register(Color)
admin.site.register(Shop)