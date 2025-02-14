from django import forms
from .models import Brand

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

class AddCarForm(forms.Form):
    brand = forms.ModelChoiceField(queryset=Brand.objects.all())
    model = forms.CharField(max_length=50,initial='johan')
    price = forms.DecimalField(max_digits=8, decimal_places=2)
    image = forms.ImageField()
    additional_img = MultipleFileField()
    color = forms.CharField(max_length=100)
    description = forms.CharField(widget=forms.Textarea())
    annotation = forms.CharField(max_length=1000)



class AnotherImageForm(forms.Form):
    additional_img = forms.ImageField()