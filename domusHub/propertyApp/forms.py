from django import forms
from .models import Property, PropertyCategory

class PropertyForm(forms.ModelForm):
    class Meta:
        model = Property
        # Included all the new fields we added to the model
        fields = [
            "title", "category", "price", "property_address", "description", "image", "status", 
            "construction_status", "registered_survey", "deed_of_assignment", 
            "building_plan_approval", "c_of_o", "governors_consent", 
            "land_size", "sq_meters", "unit_size", "number_of_bedrooms", "number_of_bathrooms"
        ]
        
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Property Title (e.g., Luxury 4 Bedroom Terrace)'}),
            'price': forms.NumberInput(attrs={'min': '0', 'placeholder': 'Price (e.g., 85000000)'}),
            'property_address': forms.TextInput(attrs={'placeholder': 'Full Property Address / Location'}),
            'description': forms.Textarea(attrs={
                'rows': 10, 
                'placeholder': 'Write a very detailed note about the property... (Mention neighborhood, topography, security, electricity, proximity to roads, etc.)'
            }),
            'land_size': forms.TextInput(attrs={'placeholder': 'e.g., 600 sqm, 1 Plot, or 2 Acres'}),
            'sq_meters': forms.NumberInput(attrs={'placeholder': 'Numeric sqm only (e.g., 600)'}),
            'unit_size': forms.TextInput(attrs={'placeholder': 'Built-up area (e.g., 350 sqm). Leave blank for bare land'}),
            'number_of_bedrooms': forms.NumberInput(attrs={'min': '0', 'placeholder': 'Number of Bedrooms'}),
            'number_of_bathrooms': forms.NumberInput(attrs={'min': '0', 'placeholder': 'Number of Bathrooms'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # This smart loop automatically adds placeholders to choice/dropdown fields 
        # and injects a 'form-control' class to make styling with Bootstrap/Tailwind easy.
        for field_name, field in self.fields.items():
            # Add Bootstrap class to all fields if you use it
            existing_class = field.widget.attrs.get('class', '')
            field.widget.attrs['class'] = f"{existing_class} form-control".strip()
            
            # Auto-generate placeholder for dropdowns if not already set
            if isinstance(field.widget, forms.Select) and 'placeholder' not in field.widget.attrs:
                field.widget.attrs['placeholder'] = f"Select {field.label}"


class PropertyCategoryForm(forms.ModelForm):
    class Meta:
        model = PropertyCategory
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Category Name (e.g., Land, Duplex, Flat)'}),
            'slug': forms.TextInput(attrs={'placeholder': 'slug-format-name'}),
        }
