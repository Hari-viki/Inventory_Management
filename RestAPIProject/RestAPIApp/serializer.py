from rest_framework import serializers
from .models import Inventory_Management

class Inventory_Management_Serializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=100)
    description=serializers.CharField()
    quality = serializers.IntegerField()

    def create(self,validation_data):
        return Inventory_Management.objects.create(**validation_data)
    
    def update(self, instance, validated_data):
        # Here you define how each field will be updated
        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get('description', instance.description)
        instance.quality = validated_data.get('quality', instance.quality)
        instance.save()
        return instance