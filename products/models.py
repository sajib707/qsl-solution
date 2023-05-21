from django.db import models
from django.urls import reverse
from django.conf import settings


'''class Products(models.Model):
    name = models.CharField(max_length=255)
    price = models.FloatField()
    stock = models.IntegerField()
    details = models.CharField(max_length=5000)
    image = models.ImageField(upload_to='static/img/')
'''

'''class Services(models.Model):
    name = models.CharField(max_length=255)
    price = models.FloatField()
    details = models.CharField(max_length=5000)
    image_url = models.CharField(max_length=2083)
'''
class Items(models.Model):
    name = models.CharField(max_length=255)
    price = models.FloatField()
    stock = models.IntegerField()
    details = models.CharField(max_length=5000)
    slug = models.SlugField(max_length=255)
    image = models.ImageField(upload_to='static/img/')

    class Meta:
        verbose_name_plural = 'Items'
        #ordering = ('-created',)

    def get_absolute_url(self):
        return reverse('products:item_details', args=[self.slug])

    def __str__(self):
        return self.name

class ProductManager(models.Manager):
    def get_queryset(self):
        return super(ProductManager, self).get_queryset().filter(is_active=True)


class ServiceManager(models.Manager):
    def get_queryset(self):
        return super(ServiceManager, self).get_queryset().filter(is_active=True)


class Category(models.Model):
    name = models.CharField(max_length=255, db_index=True)
    cat_slug = models.SlugField(max_length=255, unique=True)

    class Meta:
        verbose_name_plural = 'categories'

    def get_absolute_url(self):
        return reverse('products:product_filter', args=[self.cat_slug])

    def __str__(self):
        return self.name


class Product(models.Model):
    category = models.ForeignKey(Category, related_name='product', on_delete=models.CASCADE)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='product_creator')
    name = models.CharField(max_length=255)
    author = models.CharField(max_length=255, default='admin')
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='static/img/')
    slug = models.SlugField(max_length=255)
    price = models.DecimalField(max_digits=4, decimal_places=2)
    in_stock = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    objects = models.Manager()
    products = ProductManager()

    class Meta:
        verbose_name_plural = 'Products'
        ordering = ('-created',)
    def get_absolute_url(self):
        return reverse('products:product_detail', args=[self.slug])

    def __str__(self):
        return self.name

class Service(models.Model):
    category = models.ForeignKey(Category, related_name='service', on_delete=models.CASCADE)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='service_creator')
    name = models.CharField(max_length=255)
    author = models.CharField(max_length=255, default='admin')
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='static/img/')
    slug = models.SlugField(max_length=255)
    price = models.DecimalField(max_digits=4, decimal_places=2)
    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    objects = models.Manager()
    service = ServiceManager()

    class Meta:
        verbose_name_plural = 'Services'
        ordering = ('-created',)

    def get_absolute_url(self):
        return reverse('products:service_detail', args=[self.slug])

    def __str__(self):
        return self.name
