
from functools import reduce
import operator
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from .models import Product, Category, ProductType
from django.db.models import Q


def categories(request):
    return {
        'categories': Category.objects.all()
    }

def index(request):
    products = Product.objects.prefetch_related("product_image").filter(is_active=True)
    return render(request,'products/index.html',{'products' : products})

def contact(request):
    return render(request,'products/contact.html')


def list_products(request):
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        ordering = request.GET.get('ordering', "")
        search = request.GET.get('search', "")
        selected_brands = request.GET.getlist('brand')
        selected_warranties = request.GET.getlist('warranty')
        selected_sellers = request.GET.getlist('seller')
        selected_colors = request.GET.getlist('color')
        selected_product_types = request.GET.getlist('product_type')


        filtered_products = Product.objects.all()

        if selected_product_types:
            product_types = ProductType.objects.filter(name__in=selected_product_types)
            filtered_products = filtered_products.filter(product_type__in=product_types)


        if selected_brands:
            filtered_products = filtered_products.filter(brand__in=selected_brands)

        if selected_warranties:
            filtered_products = filtered_products.filter(warranty__in=selected_warranties)

        if selected_sellers:
            filtered_products = filtered_products.filter(seller__in=selected_sellers)

        if selected_colors:
            filtered_products = filtered_products.filter(color__in=selected_colors)

        if search:
            filtered_products = filtered_products.filter(Q(title__icontains=search) | Q(brand__icontains=search))

        if ordering:
            filtered_products = filtered_products.order_by(ordering)

        products_data = []
        for product in filtered_products:
            product_data = {
                'title': product.title,
                'brand': product.brand,
                'product_images': [image.image.url for image in product.product_image.all()],
                'discount_price': product.discount_price,
                'regular_price': product.regular_price,
                # Include other fields if needed
            }
            products_data.append(product_data)

        return JsonResponse({'products': products_data})

    else:
        ordering = request.GET.get('ordering', "")
        search = request.GET.get('search', "")
        brands = set(Product.objects.values_list('brand', flat=True))
        warranties = set(Product.objects.values_list('warranty', flat=True))
        sellers = set(Product.objects.values_list('seller', flat=True))
        colors = set(Product.objects.values_list('color', flat=True))
        selected_brands = request.GET.getlist('brand')
        selected_warranties = request.GET.getlist('warranty')
        selected_sellers = request.GET.getlist('seller')
        selected_colors = request.GET.getlist('color')
        selected_product_types = request.GET.getlist('product_type')


        filtered_products = Product.objects.all()

        if selected_product_types:
            product_types = ProductType.objects.filter(name__in=selected_product_types)
            filtered_products = filtered_products.filter(product_type__in=product_types)


        if selected_brands:
            filtered_products = filtered_products.filter(brand__in=selected_brands)

        if selected_warranties:
            filtered_products = filtered_products.filter(warranty__in=selected_warranties)

        if selected_sellers:
            filtered_products = filtered_products.filter(seller__in=selected_sellers)

        if selected_colors:
            filtered_products = filtered_products.filter(color__in=selected_colors)

        if search:
            filtered_products = filtered_products.filter(Q(title__icontains=search) | Q(brand__icontains=search))

        if ordering:
            filtered_products = filtered_products.order_by(ordering)

        context = {
            'brands': brands,
            'warranties': warranties,
            'sellers': sellers,
            'colors': colors,
            'selected_brands': selected_brands,
            'selected_warranties': selected_warranties,
            'selected_sellers': selected_sellers,
            'selected_colors': selected_colors,
            'selected_product_types': selected_product_types,
            'products': filtered_products,
            'product_types': ProductType.objects.all(),

        }

        return render(request, 'products/listproducts.html', context)

    

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

def product_filter(request, slug):
    category = get_object_or_404(Category, slug=slug)
    products = Product.objects.filter(category = category)
    return render(request,'products/listproducts.html',{'category' : category, 'products' : products})


