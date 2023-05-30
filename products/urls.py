from django.urls import path
from . import views

app_name = 'products'

urlpatterns = [
    path('', views.index),
    path('index', views.index),
    path('listproducts/', views.list_products, name='list_products'),
    path('contact', views.contact),
    path('details-<slug:slug>/', views.product_detail, name='product_detail'),
    path('listproducts/filter-<slug:slug>/', views.list_products, name='product_filter'),
    path('api/suggestionapi/', views.suggestionApi, name='suggestionapi'),
]