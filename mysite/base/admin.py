from django.contrib import admin
from .models import Order, Item, Category
# Register your models here.

@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'price', 'stock', 'category')
    search_fields = ('title', 'content')

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('title', 'price', 'count', 'username')
    search_fields = ('title', 'username')

# admin.site.register(Category)
# admin.site.register(Item)
# admin.site.register(Order)