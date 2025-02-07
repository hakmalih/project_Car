from django.shortcuts import render

from main.models import Car, Brand, CarImage


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
    new =Car.objects.all()
    brands=Brand.objects.all()
    context = {
        'new': new,
        'brands':brands,
    }
    if request.method == 'POST':
        data = request.POST
        model = data.get('model')
        color= data.get('color')
        annotation= data.get('annotation')
        description= data.get('description')
        price = data.get('price')
        image = data.get('image')
        if model and color and annotation and description and image:
            if price.isdigit() :
                new_car_instance = Car(model=model,color=color,annotation=annotation,description=description,price=price,image=image)
                new_car_instance.save()
            else:
                context['error_age'] = 'неправильный тип данных '
        else:
            context['error'] = 'заполните все поля'
    return render(request,'add_car.html', context)