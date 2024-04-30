from rest_framework import serializers
from base.models import Example
from .models import Qna
class ExampleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Example
        fields = ['id', 'created', 'title', 'price', 'photo', 'stock']

class QnaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Qna
        fields = ['id', 'question', 'answer']