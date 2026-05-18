from django.contrib import admin
from .models import Property, PropertyCategory


@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = ('title', 'property_address', 'category', 'status', 'owner', 'price', 'created_at')
    list_filter = ('category', 'status', 'owner')
    search_fields = ('title', 'description', 'property_address')


@admin.register(PropertyCategory)
class PropertyCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}
