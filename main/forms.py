from django import forms
from .models import Brand


class AddCarForm(forms.Form):
    brand = forms.ModelChoiceField(queryset=Brand.objects.all())
    model = forms.CharField(max_length=50)
    price = forms.DecimalField(max_digits=8, decimal_places=2)
    image = forms.ImageField()
    color = forms.CharField(max_length=100)
    description = forms.CharField(widget=forms.Textarea())
    annotation = forms.CharField(max_length=1000)
