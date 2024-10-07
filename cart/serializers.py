from rest_framework import serializers
from .models import Cart, CartItem


class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = '__all__'

class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ['cart', 'product', 'quantity', 'price']

    
    def validate_quantity(self, value):
        if value <= 0 :
            raise serializers.ValidationError('Quantity must be greater than zero.')
        return value