from rest_framework import serializers
from .models import *
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.hashers import check_password
from rest_framework.validators import UniqueValidator
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
class QnaCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Qna
        fields = ['question', 'item']
class SellerLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(style={'input_type': 'password'})

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        if email and password:
            # 이메일로 판매자 객체 가져오기
            seller = Seller.objects.filter(email=email).first()

            if seller:
                # 비밀번호 확인
                if not seller.check_password(password):
                    raise serializers.ValidationError('비밀번호가 일치하지 않습니다.')
            else:
                raise serializers.ValidationError('해당 이메일의 판매자가 존재하지 않습니다.')
        else:
            raise serializers.ValidationError('이메일과 비밀번호를 입력해주세요.')

        return data
class SellerSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = Seller
        fields = ['name', 'email', 'password', 'confirm_password', 'phone', 'bank', 'account_number']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        validated_data.pop('confirm_password', None)  # confirm_password 필드 제거
        return Seller.objects.create_user(**validated_data)

class QnaSerializer(serializers.ModelSerializer):
    item_title = serializers.CharField(source='item.title', read_only=True)
    class Meta:
        model = Qna
        fields = ['id', 'question', 'answer', 'item', 'item_title']

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'


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