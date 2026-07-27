from django import forms
from .models import Listing,ListingImage,Inquiry

class ListingForm(forms.ModelForm):
    class Meta:
        model = Listing
        fields = ['title', 'description', 'price', 'bedrooms', 'bathrooms', 'square_feet', 'address', 'city', 'state', 'zip_code', 'property_type']
        
class ListingImageForm(forms.ModelForm):
    class Meta:
        model = ListingImage
        fields = ['image']
        
class InquiryForm(forms.ModelForm):
    class Meta:
        model = Inquiry
        fields = ['message']