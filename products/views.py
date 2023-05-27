
from django.shortcuts import render, get_object_or_404
from .models import Product, Category
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import Q
PRODUCTS_PER_PAGE = 1


def categories(request):
    return {
        'categories': Category.objects.all()
    }

def index(request):
    products = Product.objects.prefetch_related("product_image").filter(is_active=True)
    return render(request,'products/index.html',{'products' : products})

def contact(request):
    return render(request,'products/contact.html')


def listProducts(request):

    ordering = request.GET.get('ordering', "")     
    search = request.GET.get('search', "")
    price = request.GET.get('price', "")

    if search:
        products = Product.objects.filter(Q(title__icontains=search) | Q(brand__icontains=search)) 

    else:
        products = Product.objects.all()

    if ordering:
        products = products.order_by(ordering) 

    if price:
        products = products.filter(regular_price__lt = price)

    #Pagination
    page = request.GET.get('page',1)
    product_paginator = Paginator(products, PRODUCTS_PER_PAGE)
    try:
        products = product_paginator.page(page)
    except EmptyPage:
        products = product_paginator.page(product_paginator.num_pages)
    except:
        products = product_paginator.page(PRODUCTS_PER_PAGE)
    return render(request, "products/shop.html", {"products":products, 'page_obj':products, 'is_paginated':True, 'paginator':product_paginator})



def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, is_active=True)
    return render(request,'products/detail.html',{'product' : product})

def product_filter(request, slug=None):
    category = get_object_or_404(Category, slug=slug)
    products = Product.objects.filter(category = category)
    return render(request,'products/shop.html',{'category' : category, 'products' : products})


