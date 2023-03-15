from django.contrib import admin
from .models import Product, Service, Category, Items

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name','price','in_stock', 'is_active')
    prepopulated_fields = {'slug': ('name',)}

admin.site.register(Product, ProductAdmin)

class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name','price')

admin.site.register(Service, ServiceAdmin)

class ItemAdmin(admin.ModelAdmin):
    list_display = ('name','price','slug')

admin.site.register(Items, ItemAdmin)

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name','cat_slug')
    prepopulated_fields = {'cat_slug': ('name',)}

admin.site.register(Category, CategoryAdmin)

