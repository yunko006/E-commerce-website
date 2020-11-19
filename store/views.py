from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import *
from .forms import checkoutForm
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib import messages
# Create your views here.

def store(request):
    products = Product.objects.all()
    
    if request.user.is_authenticated:
        # get the current customer
        customer = request.user.customer
        # get the order or create one 
        order, created = Order.objects.get_or_create(customer=customer, complete=False)

    else:
        order = Order.objects.all()

    context = {
        'products': products,
        'order': order,
    }
    return render(request, 'store/store.html', context)


@login_required
def cart(request):
    cart = Cart.objects.all()

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        # a revoir pas tout compris : 
        items = order.cart_set.all()

    context = {
        'order': order,
        'items': items,
    }

    return render(request, 'store/cart.html', context)


@login_required
def checkout(request):

    cart = Cart.objects.all()
    customer = request.user.customer
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    # c'est ca qui permet d'afficher les items qui sont dans le cart. WHY ??
    items = order.cart_set.all()

    if request.method != 'POST':
        form = checkoutForm()
    else:
        form = checkoutForm(data=request.POST)

        if form.is_valid():
            # attribue les champs à leurs valeurs
            country = form.cleaned_data.get('country')
            address = form.cleaned_data.get('address')
            rest_address = form.cleaned_data.get('rest_address')
            city = form.cleaned_data.get('city')
            state = form.cleaned_data.get('state')
            postal_code = form.cleaned_data.get('postal_code')

            # met les données dans le model et l'enregistre dans la DB
            checkout_address = CheckoutAddress(
                user = request.user,
                country = country,
                address = address,
                rest_address = rest_address,
                city = city,
                state = state,
                postal_code = postal_code,
            )

            # save l'address du checkout mais va créer une nouvelle address a chaque fois (pas d'update)
            checkout_address.save()
            # fait passer complete to true ce qui va reset le cart car les deux sont liés.
            order.complete = True
            order.save()
            
            messages.success(request, "Votre commande a bien été prise en compte." )
            return redirect('store:store')
        
    context = {
        'form': form,
        'order': order,
        'items': items,
        'cart': cart,
    }

    return render(request, 'store/checkout.html', context)


def item(request, item_id):
    item = get_object_or_404(Product, id=item_id)

    if request.user.is_authenticated:
        # display le panier dans la navbar
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
    
    else:
        order = Order.objects.all()

    context = {"item": item, 'order': order}
    return render(request, 'store/item.html', context)


def search(request):
    # search bar settings :
    search = request.GET.get('search', None)
    if search is not None:
        products = Product.objects.filter(name__icontains=search)
    else:
        products = Product.objects.all()
    
    context = {'search': search, 'products': products}
    return render(request, 'store/search.html', context)


@login_required
def add_to_cart(request, product_id):
    # add an item to cart
    product = get_object_or_404(Product, id=product_id)
    # get the customer
    customer = request.user.customer 
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    # cette ligne add l'item dans mon cart mais pourquoi ?
    cart, created = Cart.objects.get_or_create(order=order, product=product)
    # update the quantity
    cart.quantity += 1
    #save le nouveau cart
    cart.save()
    #messages.success(request, "Cart updated!")
    return redirect('store:cart')


@login_required
def remove_from_cart(request, product_id):
    # add an item to cart
    product = get_object_or_404(Product, id=product_id)
    # get the customer
    customer = request.user.customer 
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    # add an item to the cart. If the cart doesnt exit create one.
    cart, created = Cart.objects.get_or_create(order=order, product=product)
    # update the quantity or delete the item in the cart if qty <= 0.
    if cart.quantity >= 1:
        cart.quantity -= 1
        cart.save()
        if cart.quantity <= 0:
            cart.delete()

    #messages.success(request, "Cart updated!")
    return redirect('store:cart')

    