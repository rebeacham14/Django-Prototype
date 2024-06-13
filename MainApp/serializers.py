from .models import Order, Members, MenuItems
from rest_framework import serializers


class MemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Members
        fields = ['id','username', 'password', 'role', 'city']

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['id','name', 'category', 'price', 'city']

class MenuItemsSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuItems
        fields = ['id','title', 'price', 'category', 'featured']
