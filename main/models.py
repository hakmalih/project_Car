from django.db import models
from django.db.models import CharField


# Create your models here.

class Brand (models.Model):
    title =models.CharField(max_length=50)

    def __str__(self):
        return self.title


class CarImage(models.Model):
    picture = models.ImageField(upload_to='car')
    car = models.ForeignKey('Car',on_delete=models.CASCADE)

    def __str__(self):
        return self.car.model

class Color(models.Model):
    color = models.CharField(max_length=50)

    def __str__(self):
        return self.color

class Shop (models.Model):
    shop = models.CharField(max_length=500)

    def __str__(self):
        return self.shop


class Car (models.Model):
    brand = models.ForeignKey('Brand',on_delete=models.CASCADE)
    model = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    image = models.ImageField(upload_to='car')
    color = models.ManyToManyField('Color')
    description = models.TextField()
    annotation = models.CharField(max_length=1000)
    shop = models.ManyToManyField('Shop')

    def __str__(self):
        return f'{self.brand} {self.model}'


