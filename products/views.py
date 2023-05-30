
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from .models import Product, Category
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import Q
PRODUCTS_PER_PAGE = 12


def categories(request):
    return {
        'categories': Category.objects.all()
    }

def index(request):
    products = Product.objects.prefetch_related("product_image").filter(is_active=True)
    return render(request,'products/index.html',{'products' : products})

def contact(request):
    return render(request,'products/contact.html')


def list_products(request, slug=None):

    ordering = request.GET.get('ordering', "")
    search = request.GET.get('search', "")
    brands = set(Product.objects.values_list('brand', flat=True))
    colors = Product.objects.values_list('color', flat=True).distinct()

    selected_brands = request.GET.getlist('brand')
    selected_colors = request.GET.getlist('color')

    filtered_products = Product.objects.all()

    if slug:
        # Handle filtered listing
        filtered_products = filtered_products.filter(category__slug=slug)


    if selected_brands:
        q_objects = Q()
        for brand in selected_brands:
            q_objects |= Q(brand=brand)
        filtered_products = filtered_products.filter(q_objects)

    if selected_colors:
        q_objects = Q()
        for color in selected_colors:
            q_objects |= Q(color=color)
        filtered_products = filtered_products.filter(q_objects)
    
    if search:
        filtered_products = filtered_products.filter(Q(title__icontains=search) | Q(brand__icontains=search))

    if ordering:
        products = products.order_by(ordering)


    context = {
        'brands': brands,
        'colors': colors,
        'selected_brands': selected_brands,
        'selected_colors': selected_colors,
        'products': filtered_products,
    }


    # Pagination
    #page = request.GET.get('page', 1)
    # product_paginator = Paginator(products, PRODUCTS_PER_PAGE)
    #try:
     #   products = product_paginator.page(page)
    #except EmptyPage:
     #   products = product_paginator.page(product_paginator.num_pages)
    #except:
     #   products = product_paginator.page(PRODUCTS_PER_PAGE)

    return render(request, "products/listproducts.html", context)
    #{
     #   "products": products,
      #  'page_obj': products,
       # 'is_paginated': True,
        #'paginator': product_paginator
    #})




def suggestionApi(request):
    if 'term' in request.GET:
        search = request.GET.get('term')
        qs = Product.objects.filter(Q(product_name__icontains=search))[0:10]
        # print(list(qs.values()))
        # print(json.dumps(list(qs.values()), cls = DjangoJSONEncoder))
        titles = list()
        for product in qs:
            titles.append(product.product_name)
        #print(titles)
        if len(qs)<10:
            length = 10 - len(qs)
            qs2 = Product.objects.filter(Q(brand__icontains=search))[0:length]
            for product in qs2:
                titles.append(product.brand)
        return JsonResponse(titles, safe=False)


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, is_active=True)
    return render(request,'products/detail.html',{'product' : product})

def product_filter(request, slug=None):
    category = get_object_or_404(Category, slug=slug)
    products = Product.objects.filter(category = category)
    return render(request,'products/listproducts.html',{'category' : category, 'products' : products})


