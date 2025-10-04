from django.contrib import admin
from .models import Category, MainCategory, Product, ProductImage, Profile,Order,OrderItem


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1
    max_num = 5  
    ordering = ['order']

class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'price']
    inlines = [ProductImageInline]

admin.site.register(MainCategory)
admin.site.register(Category)
admin.site.register(Product,ProductAdmin)
admin.site.register(Profile)
admin.site.register(Order)
admin.site.register(OrderItem)
