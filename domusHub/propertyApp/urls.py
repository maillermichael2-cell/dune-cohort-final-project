from django.urls import path
from . import views


urlpatterns = [
    path('propertyDash/', views.property, name='dashboard'),
]