from django import forms
from .models import Listing, ListingImage, Inquiry


class ListingForm(forms.ModelForm):
    class Meta:
        model = Listing
        fields = ['title', 'description', 'price', 'bedrooms', 'bathrooms', 'square_feet', 'address', 'city', 'state', 'zip_code', 'property_type']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Modern Family Home with Pool'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Describe your property...'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'e.g. 750000'}),
            'bedrooms': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'e.g. 3'}),
            'bathrooms': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'e.g. 2'}),
            'square_feet': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'e.g. 1800'}),
            'address': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '123 Main Street'}),
            'city': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Austin'}),
            'state': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. TX'}),
            'zip_code': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. 78701'}),
            'property_type': forms.Select(attrs={'class': 'form-select'}),
        }


class ListingImageForm(forms.ModelForm):
    class Meta:
        model = ListingImage
        fields = ['image']


class InquiryForm(forms.ModelForm):
    class Meta:
        model = Inquiry
        fields = ['message']
        widgets = {
            'message': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'Hi, I am interested in this property...'}),
        }