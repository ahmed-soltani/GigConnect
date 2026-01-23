from django import forms
from .models import Product, ProductImage


class ProductForm(forms.ModelForm):

    class Meta:
        model = Product
        fields = ['name', 'description', 'price']
        widgets = {
            'myuser': forms.HiddenInput(),
        }


class ProductImageForm(forms.ModelForm):

    class Meta:
        model = ProductImage
        fields = ['image']


class ProductUpdateForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'price']