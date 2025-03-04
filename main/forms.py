from django import forms
from django.contrib.auth import get_user_model
from django.forms import HiddenInput, CheckboxInput

from .models import Brand, Color,Shop

class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True


class MultipleFileField(forms.ImageField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = single_file_clean(data, initial)
        return result

class EditCarForm(forms.Form):
    brand = forms.ModelChoiceField(queryset=Brand.objects.all())
    model = forms.CharField(max_length=50,initial='johan')
    price = forms.DecimalField(max_digits=8, decimal_places=2)
    image = forms.ImageField(required=False)
    color = forms.ModelMultipleChoiceField(queryset=Color.objects.all())
    description = forms.CharField(widget=forms.Textarea())
    annotation = forms.CharField(max_length=1000)
    shop = forms.ModelMultipleChoiceField(queryset=Shop.objects.all())


class AnotherImageForm(forms.Form):
    additional_img = forms.ImageField()
    id= forms.IntegerField(widget=HiddenInput(),required=False)

class AddCarForm(EditCarForm):
    additional_img = MultipleFileField(required=False)


class AddShopForm (forms.ModelForm):
    class Meta:
        model = Shop
        fields = '__all__'


AnotherImageFormset=forms.formset_factory(AnotherImageForm,can_delete=True)

class CatalogPageForm(forms.Form):
    brand = forms.ModelMultipleChoiceField(widget=forms.CheckboxSelectMultiple,queryset=Brand.objects.all(),required=False)
    color = forms.ModelMultipleChoiceField(widget=forms.CheckboxSelectMultiple,queryset=Color.objects.all(),required=False)


class RegistrationForm(forms.ModelForm):
    username = forms.CharField(label="Логин")
    password = forms.CharField(widget=forms.PasswordInput,label="Пароль")
    password2 = forms.CharField(widget=forms.PasswordInput,label="Повторите пароль")

    class Meta:
        model = get_user_model()
        fields = "username","password"

    def clean(self):
        cleaned_data = self.cleaned_data
        password = cleaned_data.get('password')
        password2 = cleaned_data.get('password2')
        if password!=password2:
            raise forms.ValidationError('Пароли не совпадают')


