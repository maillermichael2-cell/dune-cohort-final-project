from django.contrib.auth import views as auth_views
from django.contrib.auth.forms import AuthenticationForm
from django.urls import path
from . import views
CustomLoginForm = type('CustomLoginForm', (AuthenticationForm,), {})
CustomLoginForm.base_fields['username'].widget.attrs.update({'placeholder': 'Username'})
CustomLoginForm.base_fields['password'].widget.attrs.update({'placeholder': 'Password'})


urlpatterns = [
    path('', views.accounts_home, name='accounts_home'),
    path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html',form_class=CustomLoginForm), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', views.register, name='register'),
    path('dashboard/', views.dashboard, name='dashboard'),
]