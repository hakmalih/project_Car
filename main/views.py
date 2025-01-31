from django.shortcuts import render

from main.models import Car, Brand


# Create your views here.
def get_main_page(request):
    cars =Car.objects.all()
    brands=Brand.objects.all()
    data=request.GET.get('options')
    if data:
        cars = Car.objects.filter(brand=data)
    bmw=brands[1]
    context = {
        'cars': cars,
        'brands':brands,
    }
    return render(request,'main.html', context)


def car_detail(request,id):
    cars =Car.objects.get(id=id)
    context = {
        'cars': cars
    }
    return render(request,'car_detail.html', context)



