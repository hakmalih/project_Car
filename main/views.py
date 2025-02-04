from django.shortcuts import render

from main.models import Car, Brand, CarImage


# Create your views here.
def get_main_page(request):
    cars =Car.objects.all()
    brands=Brand.objects.all()
    context = {
        'cards': cars,
        'brands':brands,
    }
    return render(request,'main.html', context)


def car_detail(request,id):
    cars =Car.objects.get(id=id)
    picture = CarImage.objects.filter(car=id)
    context = {
        'cars': cars,
        'picture':picture,
    }
    return render(request,'car_detail.html', context)



