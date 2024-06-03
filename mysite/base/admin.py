from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(UserLogin)
admin.site.register(Review)
admin.site.register(Qna)
@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'price', 'stock', 'category')
    search_fields = ('title', 'content')
admin.site.register(Category)
admin.site.register(Cart)
# admin.site.register(Order)
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('title', 'price', 'count', 'username', 'created_at')
    search_fields = ('title', 'username')
