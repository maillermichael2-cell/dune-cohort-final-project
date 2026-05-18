from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm

# Create your views here.

def accounts_home(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    return redirect('login')


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
    else:
        form = RegisterForm()
    return render(request, 'accounts/register.html', {'form': form})


@login_required
def dashboard(request):
    user = request.user
    profile = getattr(user, 'profile', None)
    if profile:
        if profile.role == 'ESTATE AGENT':
            return redirect('agent_dashboard')
        if profile.role == 'INDIVIDUAL':
            return redirect('individual_dashboard')

    return redirect('property_list')
