from django.urls import path
from . import views

app_name = 'products'

urlpatterns = [
    path('', views.index),
    path('index', views.index),
    path('shop', views.listProducts, name='list_products'),
    path('contact', views.contact),
    path('details-<slug:slug>', views.product_detail, name='product_detail'),
    path('shop-<slug:slug>', views.product_filter, name='product_filter')
]