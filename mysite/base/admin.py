from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(UserLogin)
admin.site.register(Review)
admin.site.register(Qna)
admin.site.register(Item)
admin.site.register(Category)
admin.site.register(Cart)
admin.site.register(Order)
