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