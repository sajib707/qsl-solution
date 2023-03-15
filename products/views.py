from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from .models import Product, Service, Category, Items


def categories(request):
    return {
        'categories': Category.objects.all()
    }

def index(request):
    products = Product.objects.all()
    return render(request,'index.html',{'products' : products})

def contact(request):
    return render(request,'contact.html')


def shop(request):
    products = Product.objects.all()
    return render(request,'shop.html',{'products' : products})

def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    return render(request,'detail.html',{'product' : product})

def product_filter(request, cat_slug=None):
    category = get_object_or_404(Category, cat_slug=cat_slug)
    products = Product.objects.filter(category = category)
    return render(request,'shop.html',{'category' : category, 'products' : products})


