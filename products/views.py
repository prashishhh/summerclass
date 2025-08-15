from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404
from . models import Product, Category
from django.core.paginator import Paginator

# Create your views here.
# def products(request):
#     products = Product.objects.all()
#     return render(request, 'basic/products.html', {'products': products})

# def product_detail(request, id):
#     product = get_object_or_404(Product, id=id)
#     return render(request, 'basic/product_details.html', {'product': product})

def store(request, category_slug=None):
    products = None
    categories = None

    if category_slug != None:
        categories = get_object_or_404(Category, slug=category_slug)
        products = Product.objects.filter(category=categories, status=True)
        paginator = Paginator(products, 3)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)
        product_count = len(paged_products)
    else:
        products = Product.objects.all().filter(status=True).order_by('id')
        paginator = Paginator(products, 6)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)
        product_count = len(paged_products)  

    context = {
        'products': paged_products,
        'product_count': product_count,
    }  

    return render(request, 'products/products.html', context)

def product_detail(request, category_slug, product_slug):
    try:
        product = Product.objects.get(category__slug=category_slug, slug=product_slug)
    except Product.DoesNotExist:
        raise Http404("Product_not_found")
    
    context = {
        'product': product,
    }

    return render(request, 'products/details.html', context)

