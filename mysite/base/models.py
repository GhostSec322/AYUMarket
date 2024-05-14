from django.db import models

# Create your models here.
class Example(models.Model):
    created = models.DateTimeField(auto_now_add=True) #등록날짜
    title = models.CharField(max_length=100, blank=True, default='') #품목명
    price = models.DecimalField(max_digits=10, decimal_places=0) #가격
    photo = models.ImageField(upload_to='photos/')  #상품이미지
    stock = models.DecimalField(max_digits=10, decimal_places=0)  #재고량

    class Meta:
        ordering = ['created']
class SellerLogin(models.Model):
    username= models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    user_name= models.CharField(max_length=255)
    tel = models.CharField(max_length=20)
    email =models.EmailField(max_length=255)
class UserLogin(models.Model):
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    user_name = models.CharField(max_length=255)
    tel = models.CharField(max_length=20)
    email = models.EmailField(max_length=255)

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