from django.shortcuts import render

from main.models import Car, Brand, CarImage

from .forms import AddCarForm


# Create your views here.
def get_main_page(request):
    cars =Car.objects.all()
    context = {
        'cards': cars,
    }
    return render(request,'main.html', context)


def car_detail(request,id):
    cars =Car.objects.get(id=id)
    picture = CarImage.objects.filter(car=id)
    print(cars)
    print(picture)
    context = {
        'cars': cars,
        'picture':picture,
    }
    return render(request,'car_detail.html', context)



def add_car(request):
    form = AddCarForm()
    print(form.is_bound,'32')
    if request.method=="POST":
        form = AddCarForm(request.POST,request.FILES)
        if form.is_valid():
            print('ok')
            print(form.cleaned_data)
        else:
            print('ne ok')
            print(form.errors)
    context={
        'form':form,
    }
    return render(request,'add_car.html', context)