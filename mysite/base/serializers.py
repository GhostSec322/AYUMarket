from rest_framework import serializers
from base.models import Example
from .models import Qna, Order
class ExampleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Example
        fields = ['id', 'created', 'title', 'price', 'photo', 'stock']

class QnaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Qna
        fields = ['id', 'question', 'answer']


class OrderPrcCntSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['price','count']