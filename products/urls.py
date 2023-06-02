from django.urls import path
from . import views

app_name = 'products'


urlpatterns = [
    path('', views.index),
    path('list_products/', views.list_products, name='list_products'),
    path('details-<slug:slug>/', views.product_detail, name='product_detail'),
    path('listproducts/filter-<slug:slug>/', views.product_filter, name='product_filter'),
    path('api/suggestionapi/', views.suggestionApi, name='suggestionapi'),
]

