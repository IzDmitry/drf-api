from rest_framework import serializers
from .models import Parcel, Category


class ParcelSerializer(serializers.ModelSerializer):
    """
    Сериализатор для объектов Parcel.
    """
    id = serializers.IntegerField(read_only=True)
    price = serializers.FloatField(read_only=True)

    class Meta:
        model = Parcel
        fields = [
                'id',
                'name',
                'weight',
                'category',
                'worth',
                'price',
        ]
    
    def to_representation(self, instance):
        """
        Возвращаем словарное представление сериализованного объекта.
        """
        _dict = {
            'id': instance.id,
            'name': instance.name,
            'weight': instance.weight,
            'category': instance.category.name,
            'worth': instance.worth,
        }
        """
        if not instance.price:
            instance.price = "Не расчитано"
        """
        _dict['price'] = instance.price
        return _dict

class CategorySerializer(serializers.ModelSerializer):
    """
    Сериализатор для объектов Category.
    """
    class Meta:
        model = Category
        fields = [
                'id',
                'name',
        ]