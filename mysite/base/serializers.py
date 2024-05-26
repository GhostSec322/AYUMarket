from rest_framework import serializers
from base.models import Example
from .models import *
class ExampleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Example
        fields = ['id', 'created', 'title', 'price', 'photo', 'stock']


class QnaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Qna
        fields = '__all__'
class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model= Review
        fields= '__all__'
class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        models=Item
        fields= '__all__'
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        models= Category
        fields= '__all__'
class Cart(serializers.ModelSerializer):
    class Meta:
        models=Cart
        fields ='__all__'
class RefundRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = RefundRequest
        fields = ['order', 'reason', 'created_at', 'approved']