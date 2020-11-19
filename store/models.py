from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django_countries.fields import CountryField

# Create your models here.

class Customer(models.Model):
    # un customer est lié à un user
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=100)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    description = models.TextField(max_length=200)
    image = models.ImageField(null=True, blank = True)

    def __str__(self):
        return self.name


class Order(models.Model):
    # one to many relationship avec la class Customer
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True) # set null: set parent key to null to break the relationship
    dated_added = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False)
    transaction_id = models.CharField(max_length=80)

    def __str__(self):
        return str(self.id)
    
    @property
    def get_cart_items(self):
        orderitems = self.cart_set.all()
        total = sum([item.quantity for item in orderitems])
        return total

    @property
    def get_cart_total(self):
        orderitems = self.cart_set.all()
        total = sum([item.product_price_total for item in orderitems])
        return total

    def clear(self):
        pass

class Cart(models.Model):
    product = models.ForeignKey(Product, blank=True, null=True, on_delete=models.SET_NULL )
    order = models.ForeignKey(Order, blank=True, null=True, on_delete=models.SET_NULL)
    quantity = models.IntegerField(default=0)
    date_added = models.DateTimeField(auto_now_add=True)
    #slug = models.SlugField(unique=True)

    def __str__(self):
        return str(self.order)
 
    @property
    def product_price_total(self):
        total = self.quantity * self.product.price
        return total


class CheckoutAddress(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    country = CountryField(multiple=False)
    address = models.CharField(max_length=100)
    rest_address = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=100)

    def __str__(self):
        return self.user.username

