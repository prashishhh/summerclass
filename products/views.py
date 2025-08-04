from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from . models import Product

# Create your views here.
# def products(request):
#     products = Product.objects.all()
#     return render(request, 'basic/products.html', {'products': products})

# def product_detail(request, id):
#     product = get_object_or_404(Product, id=id)
#     return render(request, 'basic/product_details.html', {'product': product})

def products(request):
    products = Product.objects.all()
    return render(request, 'products/products.html', {'products': products})

def product_detail(request, id):
    product = get_object_or_404(Product, id=id)
    return render(request, 'products/details.html', {'product': product})
