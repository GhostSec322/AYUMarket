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

    def __str__(self):
        return self.title

class Category(models.Model):
    name = models.CharField(max_length=255)

# 카테고리 이름 보이게 하기
    def __str__(self):
        return self.name

class Cart(models.Model):
    item = models.ForeignKey('Item', on_delete=models.CASCADE)
    username = models.CharField(max_length=255)
    count = models.IntegerField()

class Order(models.Model):
    item = models.ForeignKey('Item', on_delete=models.CASCADE)
    username = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    price = models.IntegerField(editable= False)
    count = models.IntegerField()
    state = models.CharField(max_length=255) #나중에 사용

    def get_item_title(self):
        return self.item.title

    def save(self, *args, **kwargs):
        self.price = self.item.price * self.count
        super(Order, self).save(*args, **kwargs)