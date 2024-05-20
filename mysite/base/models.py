from django.db import models
from django.contrib.auth.models import AbstractBaseUser, UserManager,BaseUserManager

# Create your models here.
class Example(models.Model):
    created = models.DateTimeField(auto_now_add=True) #등록날짜
    title = models.CharField(max_length=100, blank=True, default='') #품목명
    price = models.DecimalField(max_digits=10, decimal_places=0) #가격
    photo = models.ImageField(upload_to='photos/')  #상품이미지
    stock = models.DecimalField(max_digits=10, decimal_places=0)  #재고량

    class Meta:
        ordering = ['created']


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
    user = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    content = models.CharField(max_length=255)
    star = models.IntegerField()

class Qna(models.Model):
    question = models.CharField(max_length=255)
    answer = models.CharField(max_length=255)

class Item(models.Model):
    title = models.CharField(max_length=255)
    content = models.CharField(max_length=255)
    price = models.IntegerField()
    photo = models.CharField(max_length=255)
    stock = models.IntegerField()
    category = models.ForeignKey('Category', on_delete=models.CASCADE)

class Category(models.Model):
    name = models.CharField(max_length=255)

class Cart(models.Model):
    item = models.ForeignKey('Item', on_delete=models.CASCADE)
    username = models.CharField(max_length=255)
    count = models.IntegerField()

class Order(models.Model):
    item = models.ForeignKey('Item', on_delete=models.CASCADE)
    username = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    price = models.IntegerField()
    count = models.IntegerField()
    state = models.CharField(max_length=255)