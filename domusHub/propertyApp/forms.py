from django import forms
from .models import Property, PropertyCategory



class PropertyForm(forms.ModelForm):
    class Meta:
        model = Property
        fields = ["title", "description", "price", "category", "status", "image", "property_address"]
        widgets = { # lets you customize how each fields render in HTML.
            'title': forms.TextInput(attrs={'placeholder': 'Product name'}),
            'description': forms.Textarea(attrs={'placeholder': 'Description'}),
            'price': forms.NumberInput(attrs={'min': '0', 'placeholder': 'Price'}),
            'status': forms.Select(),
        }


class PropertyCategoryForm(forms.ModelForm):
    class Meta:
        model = PropertyCategory
        fields = '__all__'
