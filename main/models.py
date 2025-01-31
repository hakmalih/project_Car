from django.db import models

# Create your models here.

class Brand (models.Model):
    title =models.CharField(max_length=50)

    def __str__(self):
        return self.title


class Car (models.Model):
    brand = models.ForeignKey('Brand',on_delete=models.CASCADE)
    model = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    image = models.ImageField(upload_to='car')
    color = models.CharField(max_length=100)
    description = models.TextField()
    annotation = models.CharField(max_length=1000)

    def __str__(self):
        return f'{self.brand} {self.model}'