from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from store.models import Customer
from store.models import Order
from .forms import RegisterForm
from django.contrib.auth.models import User

# Create your views here.

def register(request):

    if request.method != 'POST':
        form = RegisterForm()

    else:
        form = RegisterForm(data=request.POST)

        if form.is_valid():
            new_user = User.objects.create_user(
                username = form.cleaned_data.get('username'),
                email = form.cleaned_data.get('email'),
                password = form.cleaned_data.get('password1'),
            )

            customer = Customer.objects.create(
                user = new_user,
                name = form.cleaned_data.get('username'),
                email = form.cleaned_data.get('email'),
            )

            login(request, new_user)
            return redirect('store:store')

    context = {'form': form}
    return render(request, 'registration/register.html', context)


def account(request):
    customer = request.user.customer
    order, created = Order.objects.get_or_create(customer=customer, complete=False) 

    user = request.user

    context = {
        'user': user,
        'order': order,
    }

    return render(request, 'registration/account.html', context)