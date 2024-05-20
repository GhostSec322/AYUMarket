from rest_framework import serializers
from base.models import Example
from .models import Qna ,Review,Order
class ExampleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Example
        fields = ['id', 'created', 'title', 'price', 'photo', 'stock']


class QnaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Qna
        fields = ['id', 'question', 'answer']

class ReviewSerializer(serializers.ModelSerializer):  # ReviewSerializer 추가
    class Meta:
        model = Review
        fields = ['id', 'item', 'user', 'title', 'content','star']
class OrderSerialzer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields =['id','item','username','title','price','count','state']