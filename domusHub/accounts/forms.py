from django import forms 
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile, AgentProfile

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    role = forms.ChoiceField(
        choices=Profile.ROLE_CHOICES,
        required=True,
        widget=forms.Select(attrs={'class': 'role-select'})
    )
    phone_number = forms.CharField(required=False, max_length=20)
    license_number = forms.CharField(required=False, max_length=50)
    agency_name = forms.CharField(required=False, max_length=100)

    class Meta:
        model = User
        fields = ['username', 'email']
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'Username'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Email'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'password1' in self.fields:
            self.fields['password1'].widget = forms.PasswordInput(attrs={'placeholder': 'Password'})
        if 'password2' in self.fields:
            self.fields['password2'].widget = forms.PasswordInput(attrs={'placeholder': 'Confirm Password'})

    def clean(self):
        cleaned_data = super().clean()
        role = cleaned_data.get('role')
        license_number = cleaned_data.get('license_number')

        if role == 'ESTATE AGENT' and not license_number:
            self.add_error('license_number', 'License number is required for estate agents.')

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=commit)
        if commit:
            role_selected = self.cleaned_data.get('role')
            phone_number = self.cleaned_data.get('phone_number', '')
            license_number = self.cleaned_data.get('license_number', '')
            agency_name = self.cleaned_data.get('agency_name', '')

            profile = Profile.objects.create(
                user=user,
                role=role_selected,
                phone_number=phone_number,
            )

            if role_selected == 'ESTATE AGENT':
                AgentProfile.objects.create(
                    profile=profile,
                    license_number=license_number,
                    agency_name=agency_name,
                )

        return user