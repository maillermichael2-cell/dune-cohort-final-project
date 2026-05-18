from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('list/', views.property_list, name='property_list'),
    path('list/category/<slug:slug>/', views.property_list, name='property_list_by_category'),
    path('list/<int:pk>/', views.property_detail, name='property_detail'),
    path('individual/', views.individual, name='individual_dashboard'),
    path('agent/', views.agent_dashboard, name='agent_dashboard'),
    path('agent/<int:pk>/edit/', views.property_edit, name='property_edit'),
    path('agent/<int:pk>/delete/', views.property_delete, name='property_delete'),
]