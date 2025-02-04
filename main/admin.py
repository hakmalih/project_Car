
from django.contrib import admin

from main.models import Car,Brand, CarImage

# Register your models here.
admin.site.register(Car)
admin.site.register(Brand)
admin.site.register(CarImage)