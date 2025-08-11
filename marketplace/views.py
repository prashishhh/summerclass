from django.shortcuts import render
from products.models import Product
from blog.models import Blog

# def home(request):
#     products = Product.objects.all()
#     blogs = Blog.objects.all()
#     return render(request, 'basic/home.html', {'products': products, 'blogs':blogs})

from django.shortcuts import render
from products.models import Product
from blog.models import Blog

# def home(request):
#     products = Product.objects.all()
#     blogs = Blog.objects.all()
#     return render(request, 'basic/home.html', {'products': products, 'blogs':blogs})

def home(request):
    products = Product.objects.all().filter(is_available=True)

    context = {
        'products': products,
    }
    return render(request, 'home/home.html', context)

def user_login(request):
    return render(request, 'user/login.html')

def user_register(request):
    return render(request, 'user/register.html')

def user_dashboard(request):
    return render(request, 'user/dashboard.html')

def cart(request):
    return render(request, 'cart/cart.html')
def checkout(request):
    return render(request, 'cart/checkout.html')

def dashboard(request):
    return render(request, 'user/dashboard.html')

def place_order(request):
    return render(request, 'cart/place_order.html')

def order_complete(request):
    return render(request, 'cart/order_complete.html')

def my_orders(request):
    return render(request, 'user/my_orders.html')

def edit_profile(request):
    return render(request, 'user/edit_profile.html')

def change_password(request):
    return render(request, 'user/change_password.html')
    blogs = Blog.objects.all()
    return render(request, 'home/home.html', {'products': products, 'blogs':blogs})