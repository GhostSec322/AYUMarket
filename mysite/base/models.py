from django.db import models
from django.contrib.auth.models import AbstractBaseUser, UserManager,BaseUserManager
from django.conf import settings
from django.utils import timezone
from django.contrib.auth.models import AbstractUser

# Create your models here.

class CustomUserManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None,**extra_fields):
        if not email:
            raise ValueError('이메일 필수입니다')
        email = self.normalize_email(email)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('슈퍼유저 생성시 is_staff는 필수입니다.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('슈퍼유저 생성시 is_superuser는 필수입니다.')

        return self.create_user(username, email, password, **extra_fields)
class SellerUserManager(BaseUserManager):
    def create_seller(self, username, email, name, phone, bank, account_number, password=None, **extra_fields):
        if not email:
            raise ValueError('이메일은 필수입니다.')
        if not username:
            raise ValueError('사용자 이름은 필수입니다.')
        if not name:
            raise ValueError('이름은 필수입니다.')
        if not phone:
            raise ValueError('전화번호는 필수입니다.')
        if not bank:
            raise ValueError('은행명은 필수입니다.')
        if not account_number:
            raise ValueError('계좌번호는 필수입니다.')

        email = self.normalize_email(email)
        seller = self.model(
            username=username,
            email=email,
            name=name,
            phone=phone,
            bank=bank,
            account_number=account_number,
            **extra_fields
        )
        seller.set_password(password)
        seller.save(using=self._db)
        return seller

    def create_superuser(self, username, email, name, phone, bank, account_number, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', False)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('슈퍼유저는 is_staff=True 이어야 합니다.')
        if extra_fields.get('is_superuser') is  True:
            raise ValueError('슈퍼유저는 is_superuser=False 이어야 합니다.')

        return self.create_seller(
            username, email, name, phone, bank, account_number, password, **extra_fields
        )

class SellerUserManager(BaseUserManager):
    def create_user(self, email, name, phone, bank, account_number, password=None):
        if not email:
            raise ValueError('이메일 주소는 필수 항목입니다.')
        user = self.model(
            email=self.normalize_email(email),
            name=name,
            phone=phone,
            bank=bank,
            account_number=account_number,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, phone, bank, account_number, password=None):
        user = self.create_user(
            email=email,
            name=name,
            phone=phone,
            bank=bank,
            account_number=account_number,
            password=password,
        )
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user
    
class Seller(AbstractBaseUser):
    BANK_CHOICES = [
        ('kb', '국민은행'),
        ('shinhan', '신한은행'),
        ('woori', '우리은행'),
        ('hana', '하나은행'),
        ('nh', '농협은행'),
        ('ibk', '기업은행'),
        ('keb', '외환은행'),
        ('sc', 'SC제일은행'),
        ('citi', '씨티은행'),
        ('kbank', '케이뱅크'),
        ('kakao', '카카오뱅크'),
    ]

    name = models.CharField(max_length=100, verbose_name='이름')
    email = models.EmailField(unique=True, verbose_name='이메일')
    phone = models.CharField(max_length=20, verbose_name='전화번호')
    bank = models.CharField(max_length=10, choices=BANK_CHOICES, verbose_name='은행명')
    account_number = models.CharField(max_length=20, verbose_name='계좌번호')
    username = models.CharField(max_length=150, unique=True, verbose_name='사용자 이름')
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)

    objects = SellerUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'phone', 'bank', 'account_number']

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '판매자'
        verbose_name_plural = '판매자들'

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True
    
class UserLogin(AbstractBaseUser):
    username = models.CharField(max_length=255, unique=True)
    email = models.EmailField(default='default@naver.com',unique=True)
    user_name = models.CharField(max_length=255)
    tel = models.CharField(max_length=20)
    is_staff = models.BooleanField(default=False)  
    is_superuser = models.BooleanField(default=False)
    last_login = None
    first_name = None
    last_name = None
    USERNAME_FIELD='username'
    REQUIRED_FIELDS = ['email']
    objects =  CustomUserManager()

    def has_perm(self, perm, obj=None):
        return self.is_superuser

    def has_module_perms(self, app_label):
        return self.is_superuser
    
    def __str__(self):
        return self.username
    
class Review(models.Model):
    item = models.ForeignKey('Item', on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    content = models.TextField()
    star = models.IntegerField()


class Item(models.Model):
    title = models.CharField(max_length=255) ## 상품제목
    content = models.CharField(max_length=255) ## 상세내용
    price = models.IntegerField() ## 가격
    photo = models.ImageField(upload_to='base/photos/')
    stock = models.IntegerField()## 재고량
    category = models.ForeignKey('Category', on_delete=models.CASCADE) ##카테고리

    # def price_display(self):
    #     return f"{self.price} 원"
    # price_display.short_description = 'price'

    def __str__(self):
        return self.title

class Qna(models.Model):
    question = models.CharField(max_length=255,null=True)
    answer = models.CharField(max_length=255 ,null=True)
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='qnas')

class Category(models.Model):
    name = models.CharField(max_length=255) ## 카테고리명 

    def __str__(self):
        return self.name

class Cart(models.Model):
    item = models.ForeignKey('Item', on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    count = models.PositiveBigIntegerField(default=1)

    class Meta:
        unique_together = ('item', 'user')

class Order(models.Model):
    item = models.ForeignKey('Item', on_delete=models.CASCADE)
    username = models.CharField(max_length=255) #주문자 명
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=1) #로그인 검증
    title = models.CharField(max_length=255)
    price = models.IntegerField()
    count = models.IntegerField()
    state = models.CharField(max_length=255)
    merchant_uid = models.CharField(max_length=255, unique=True,default='1234')
    address = models.CharField(max_length=255, default='No address provided')
    created_at = models.DateTimeField(default=timezone.now)#auto_now_add=True
    approve= models.BooleanField(default=False)
    def save(self, *args, **kwargs):
        if self.price <= 0:
            raise ValueError('가격은 양수여야 합니다.')
        
        if self.count <= 0:
            raise ValueError('수량은 양수여야 합니다.')

        super().save(*args, **kwargs)

'''
def get_item_title(self):
        return self.item.title

    def save(self, *args, **kwargs):
        self.title = self.item.title
        self.item.stock -= self.count
        self.item.save()
        self.price = self.item.price * self.count
        super(Order, self).save(*args, **kwargs)
'''
    

class RefundRequest(models.Model):
    order = models.ForeignKey('Order', on_delete=models.CASCADE)
    reason = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    state = models.CharField(null=True, blank=True, max_length=240)
    approved = models.BooleanField(default=False)  # 승인 여부

class Company(models.Model):
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=10)

    def __str__(self):
        return self.name