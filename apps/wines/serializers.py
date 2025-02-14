from rest_framework import serializers
from apps.wines.models import Wine
from apps.managers.models import Manager

class WineSerializer(serializers.ModelSerializer):
    manager_id = serializers.UUIDField(source='manager.dl91_id') 

    class Meta:
        model = Wine
        fields = ['dl91_id', 'manager_id', 'wine_name', 'wine_price', 'wine_type', 'alcohol_content', 'wine_qty_ml']

    def create(self, validated_data):
        manager_id = validated_data.pop('manager')['dl91_id']  
        manager = Manager.objects.get(dl91_id=manager_id)
        wine = Wine.objects.create(manager=manager, **validated_data)
        return wine

    def update(self, instance, validated_data):
        # Extract manager_id and update manager if it exists in the validated data
        manager_id = validated_data.pop('manager_id', None)
        if manager_id:
            manager = Manager.objects.get(dl91_id=manager_id)
            instance.manager = manager

        # Update other fields as normal
        instance.wine_name = validated_data.get('wine_name', instance.wine_name)
        instance.wine_price = validated_data.get('wine_price', instance.wine_price)
        instance.wine_type = validated_data.get('wine_type', instance.wine_type)
        instance.alcohol_content = validated_data.get('alcohol_content', instance.alcohol_content)
        instance.wine_qty_ml = validated_data.get('wine_qty_ml', instance.wine_qty_ml)

        instance.save()
        return instance