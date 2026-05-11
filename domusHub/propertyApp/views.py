from django.shortcuts import render

# Create your views here.


def property(request):
    return render(request, 'propertyApp/PropertyDashboard.html')