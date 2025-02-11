from django.shortcuts import render

from main.models import Car, Brand, CarImage

from .forms import AddCarForm


# Create your views here.
def get_main_page(request):
    cars = Car.objects.all()
    context = {
        'cards': cars,
    }
    return render(request, 'main.html', context)


def car_detail(request, id):
    cars = Car.objects.get(id=id)
    picture = CarImage.objects.filter(car=id)
    print(cars)
    print(picture)
    context = {
        'cars': cars,
        'picture': picture,
    }
    return render(request, 'car_detail.html', context)


def add_car(request):
    form = AddCarForm()
    print(form.is_bound, '32')
    if request.method == "POST":
        form = AddCarForm(request.POST, request.FILES)
        if form.is_valid():
            print(form.cleaned_data)
            new_car = Car(brand=form.cleaned_data.get('brand'),
                          model=form.cleaned_data.get('model'),
                          price=form.cleaned_data.get('price'),
                          image=form.cleaned_data.get('image'),
                          color=form.cleaned_data.get('color'),
                          description=form.cleaned_data.get('description'),
                          annotation=form.cleaned_data.get('annotation'))
            new_car.save()
            for image in form.cleaned_data.get('additional_img'):
                additional_img=CarImage(picture=image,car_id=new_car.id)
                additional_img.save()
    context = {
        'form': form,
    }
    return render(request, 'add_car.html', context)
