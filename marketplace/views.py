from django.shortcuts import render
from products.models import Product
from blog.models import Blog

# def home(request):
#     products = Product.objects.all()
#     blogs = Blog.objects.all()
#     return render(request, 'basic/home.html', {'products': products, 'blogs':blogs})

def home(request):
    products = Product.objects.all()
    blogs = Blog.objects.all()
    return render(request, 'home/home.html', {'products': products, 'blogs':blogs})