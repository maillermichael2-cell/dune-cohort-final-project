from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='property_dashboard'),
    path('about/', views.about, name='about'),
    path('individual/', views.individual, name='individual_dashboard'),
    path('individual/category/<slug:slug>/', views.individual, name='individual_dashboard_by_category'),
    path('individual/<int:pk>/', views.property_detail, name='property_detail'),
    path('agent/', views.agent_dashboard, name='agent_dashboard'),
    path('agent/<int:pk>/edit/', views.property_edit, name='property_edit'),
    path('agent/<int:pk>/delete/', views.property_delete, name='property_delete'),
]