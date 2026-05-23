from rest_framework import serializers
from .models import Property, PropertyCategory 

class PropertySerializer(serializers.ModelSerializer):
    class Meta:
        model = Property
        fields = '__all__'
    def get_property_count(self, obj):
        return obj.properties.count()

class PropertyCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = PropertyCategory
        fields = '__all__'