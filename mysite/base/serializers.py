from rest_framework import serializers
from base.models import Example
from .models import *
from django.contrib.auth.password_validation import validate_password
from rest_framework.validators import UniqueValidator
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from django.contrib.auth import authenticate

class ExampleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Example
        fields = ['id', 'title','content', 'price', 'photo', 'stock', 'category']


class QnaSerializer(serializers.ModelSerializer):
    item_title = serializers.CharField(source='item.title', read_only=True)
    class Meta:
        model = Qna
        fields = ['id', 'question', 'answer', 'item', 'item_title']







class RegisterSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        required=True,
        validators=[UniqueValidator(queryset=UserLogin.objects.all())] #중복점검
    )
    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password], # 비밀번호에 대한 검증
    )
    email = serializers.EmailField(
        required=True
    )
    user_name = serializers.CharField(
        required=True
    )
    tel = serializers.CharField(
        required=True
    )

    class Meta:
        model = UserLogin
        fields = ('username', 'password', 'email', 'user_name', 'tel')

    def create(self, validated_data): # 유저 생성과 토큰을 생성 하는 메서드
        user = UserLogin.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            user_name=validated_data['user_name'],
            tel=validated_data['tel'],
        )

        user.set_password(validated_data['password'])
        user.save()
        token = Token.objects.create(user=user)
        return user


class UserLoginSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=('user_name', 'tel')

class LoginSerializer(serializers.Serializer):
    username= serializers.CharField(
        required=True
    )
    password = serializers.CharField(
        required=True,
        write_only=True
    )

    def validate(self, data):
        user = authenticate(**data)
        if user:
            token = Token.objects.get(user = user)
            return token
        raise serializers.ValidationError({'Error':"유저 가입이 안되어 있습니다."})


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ['id','title','content', 'price', 'photo', 'stock', 'category']
    

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'

class OrderViewSerializer(serializers.ModelSerializer):
    item=ItemSerializer()
    class Meta:
        model = Order
        fields = '__all__'

class CarListtSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = "__all__"


class CartSerializer(serializers.ModelSerializer):
    item = serializers.PrimaryKeyRelatedField(queryset=Item.objects.all(), write_only=True)
    user = serializers.ReadOnlyField(source='user.username')
    count = serializers.IntegerField(required=True)

    class Meta:
        model = Cart
        fields = ['id', 'item', 'user','count']
        read_only_fields=['user']

    def create(self, validated_data):
        user = self.context['request'].user
        item = validated_data['item']
        count = validated_data.get('count', 1)


        cart, created = Cart.objects.update_or_create(  #메소드가 값을 주는 변수를 잘 저장하자
            item=item,
            user= user,
            defaults={'count': count}
        )
        return cart
    
class CartGetSerializer(serializers.ModelSerializer):
    item = serializers.PrimaryKeyRelatedField(queryset=Item.objects.all())
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model =Cart
        fields = ['id', 'item', 'user','count']
        read_only_fields=['user']
'''class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model= Review
        fields= '__all__'''
'''class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        models=Item
        fields= '__all__'
        '''
class CategorySerializer(serializers.ModelSerializer):
       class Meta:
        model = Category
        fields = '__all__'
#class Cart(serializers.ModelSerializer):
#    class Meta:
#        models=Cart
#        fields ='__all__'
class RefundRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = RefundRequest
        fields = '__all__'
class ReviewSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    item = serializers.ReadOnlyField(source='item.id')
    
    
    class Meta:
        model = Review
        fields = ['id', 'item', 'user', 'title', 'content', 'star']
        read_only_fields = ['user']