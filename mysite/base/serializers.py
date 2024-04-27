from rest_framework import serializers
from base.models import Example

class ExampleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Example
        fields = ['id', 'created', 'title', 'price', 'photo', 'stock']
