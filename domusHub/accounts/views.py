from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm
# Create your views here.

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = RegisterForm()
    return render(request, 'accounts/register.html', {'form':form})


@login_required
def dashboard(request):
    if request.user.is_authenticated:
        username = request.user.username
        email = request.user.email
        is_staff = request.user.is_staff
    return render(request, 'cloud/dashboard.html', {'user': request.user})