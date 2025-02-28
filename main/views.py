from django.shortcuts import render,redirect, get_object_or_404

from main.models import Car, Brand, CarImage,Shop

from .forms import AddCarForm, AnotherImageForm, EditCarForm, AnotherImageFormset, CatalogPageForm,AddShopForm, RegistrationForm

from django.forms import modelformset_factory

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
    context = {
        'cars': cars,
        'picture': picture,
    }
    return render(request, 'car_detail.html', context)


def add_car(request):
    form = AddCarForm()
    if request.method == "POST":
        form = AddCarForm(request.POST, request.FILES)
        if form.is_valid():
            new_car = Car(brand=form.cleaned_data.get('brand'),
                          model=form.cleaned_data.get('model'),
                          price=form.cleaned_data.get('price'),
                          image=form.cleaned_data.get('image'),

                          description=form.cleaned_data.get('description'),
                          annotation=form.cleaned_data.get('annotation'))
            new_car.save()
            color = form.cleaned_data.get('color')
            print(color)
            new_car.color.set(color)
            for image in form.cleaned_data.get('additional_img'):
                additional_img=CarImage(picture=image,car_id=new_car.id)
                additional_img.save()
    context = {
        'form': form,
    }
    return render(request, 'add_car.html', context)



def edit_car(request,id):
    form = EditCarForm()
    car = Car.objects.get(id=id)
    another_image = CarImage.objects.filter(car_id=id)
    form.fields.get('brand').initial = car.brand
    form.fields.get('model').initial=car.model
    form.fields.get('price').initial=car.price
    form.fields.get('image').initial=car.image
    form.fields.get('color').initial=car.color.all()
    form.fields.get('shop').initial=car.shop.all()
    form.fields.get('description').initial=car.description
    form.fields.get('annotation').initial=car.annotation


    another_image_list=[]
    for i in another_image:
        a={'additional_img':i.picture,'id':i.id}
        another_image_list.append(a)
    formset=AnotherImageFormset(initial=[{"additional_img": i.picture, "id": i.id} for i in another_image])


    if request.method == "POST":
        form = EditCarForm(request.POST, request.FILES)
        if form.is_valid():
            color = form.cleaned_data.pop('color')
            shop = form.cleaned_data.pop('shop')
            for i in form.cleaned_data:
                if form.cleaned_data.get(i) and not form.cleaned_data.get(i)==getattr(car, i) :
                   setattr(car,i,form.cleaned_data.get(i))
            car.save()
            car.color.set(color)
            car.shop.set(shop)
            formset = AnotherImageFormset(request.POST, request.FILES,initial=[{"additional_img": i.picture, "id": i.id} for i in another_image])
            if formset.is_valid():
                for image_form in formset:
                    if image_form.has_changed():
                        if image_form.cleaned_data.get('id') in [i.id for i in another_image]:
                            instance_img=another_image.get(id=image_form.cleaned_data.get('id'))
                            instance_img.picture=image_form.cleaned_data.get('additional_img')
                            instance_img.save()
                        else:
                            instance_img = CarImage(car_id=id, picture=image_form.cleaned_data.get('additional_img'))
                            instance_img.save()
                for f in formset.deleted_forms:
                    CarImage.objects.get(id=f.cleaned_data.get('id')).delete()
                return redirect('car_detail',id=id)

    context={
        'form':form,
        'formset':formset
    }
    return render(request,'edit_car.html',context)




def edit_car_formset(request,id):
    EditCarFormSet= modelformset_factory(Car,fields=('brand','model','price','image','color','description','annotation'),extra=0)
    car_instance = get_object_or_404(Car, id=id)
    formset = EditCarFormSet(queryset=Car.objects.filter(id=id))
    if request.method=="POST":
        formset=EditCarFormSet(request.POST,queryset=Car.objects.filter(id=id))
        if formset.is_valid():
            formset.save()
            return redirect('car_detail',id=id)
        else:
            formset = EditCarFormSet(queryset=Car.objects.filter(id=id))
    context = {
        'formset': formset
    }
    return render (request,'edit_car_formset.html',context)



def catalog_page(request):
    cars = Car.objects.all()
    catalog=CatalogPageForm()
    if request.GET.get('brand') or request.GET.get('color'):
        catalog=CatalogPageForm(request.GET)
        if catalog.is_valid():
            d={}
            if catalog.cleaned_data.get('brand'):
                d['brand_id__in']=catalog.cleaned_data.get('brand')
            if catalog.cleaned_data.get('color'):
                d['color__in']=catalog.cleaned_data.get('color')
            cars=Car.objects.filter(**d)
    context = {
        'cars': cars,
        'catalog':catalog,
    }
    return render(request,'catalog_page.html',context)

def shop_list(request):
    shops = Shop.objects.all()
    form = AddShopForm()
    if request.method=='POST':
        form=AddShopForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('shop_list')
    context ={
        'shops':shops,
        'form':form,
    }
    return render(request,'shop_list.html',context)


def get_registration_page(request):
    form = RegistrationForm()
    if request.method=="POST":
        form  = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
    context={
        'form':form,
    }
    return render(request,'registration.html',context)