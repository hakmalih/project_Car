from django.shortcuts import render,redirect, get_object_or_404

from main.models import Car, Brand, CarImage,Shop
from django.contrib.auth import get_user_model, authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.models import User

from .forms import AddCarForm, AnotherImageForm, EditCarForm, AnotherImageFormset, CatalogPageForm, AddShopForm, \
    RegistrationForm, LoginForm, ChangeUserCredentialForm, ChangePasswordForm

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
            user=form.save(commit=False)
            # user=User(username=form.cleaned_data.get('username'))
            user.set_password(form.cleaned_data.get('password'))
            user.save()
            return redirect('main')
    context={
        'form':form,
    }
    return render(request,'registration.html',context)




def enter_account(request):
    form = RegistrationForm()
    User = get_user_model()
    if request.method=='POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = User.objects.filter(username=form.cleaned_data.get('username')).first()
            print(user)
            if not user:
                context={
                    'error_message':'Такого пользователя нет',
                }
                return render(request, 'account_error.html', context)
            else:
                return render(request, 'main.html', {'user':user,})
    context = {
        'form': form,
    }
    return render(request, 'enter_account.html', context)


def get_login_page(request):
    form = LoginForm()
    context={
        'form':form,
    }
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(request,username=form.cleaned_data.get('username'),
                                password=form.cleaned_data.get('password'))
            if user:
                login(request,user)
                return redirect('main')
            else:
                error_message = 'Пользователь с такими данными не найден'
                form.add_error(None,error_message)
                context = {
                    'form': form,
                }
    return render(request,'login.html',context)



def user_logout(request):
    logout(request)
    return redirect('main')

def get_profile_page(request):
    if request.user.is_authenticated:
        user = request.user
        form = ChangeUserCredentialForm(instance=user)
        password_form = ChangePasswordForm()

        if request.method == "POST":
            if 'edit_profile_data' in request.POST:
                form = ChangeUserCredentialForm(request.POST,instance=user)
                if form.is_valid():
                    form.save()
                    return redirect('profile')
            elif 'edit_password' in request.POST:
                password_form = ChangePasswordForm(request.POST)
                if password_form.is_valid():
                    current_password = password_form.cleaned_data.get('password')
                    if user.check_password(current_password):
                        user.set_password(password_form.cleaned_data.get('new_password'))
                        user.save()
                        update_session_auth_hash(request,user)
                        password_form.add_error(None,'Пароль успешно изменён')
                    else:
                        password_form.add_error(None,'Неверный текущий пароль')

        context = {
            'form': form,
            'password_form':password_form,
        }
        return render(request, 'profile.html', context)
    else:
        return redirect('login')









def account_page(request):
    context={

    }
    return render(request,'account_page.html',context)