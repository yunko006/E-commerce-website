from django.urls import path 
from . import views

app_name = 'store'

urlpatterns = [
    # Home page 
    path('', views.store, name='store'),
    # search page
    path('search/', views.search, name='search'),
    # Cart page
    path('cart/', views.cart, name='cart'),
    # Checkout page
    path('checkout/', views.checkout, name='checkout'),
    # Item page
    path('item/<int:item_id>/', views.item, name='item'),
    # slug product
    path('update_cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    # remove item
    path('remove_item/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),
]

