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
    path('agent_properties/', views.agent_properties_list, name='agent_properties'),
    path('favorite/<int:pk>/', views.toggle_favorite, name='toggle_favorite'),
    path('favorites/', views.favorites_list, name='favorites_list'),


    # api urls
    path('api/properties/', views.PropertyListAPIView.as_view(), name='api_property_list'),
    path('api/properties/<int:pk>/', views.PropertyDetail.as_view(), name='api_property_detail'),   
    path('api/categories/', views.PropertyCategoryListAPIView.as_view(), name='api_category_list'),
    path('api/property/create/', views.PropertyCreateAPIView.as_view(), name='api_property_create'),
]