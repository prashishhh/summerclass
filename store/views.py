from django.shortcuts import render, get_object_or_404, redirect
from django.http import Http404
from . models import Product
from category.models import Category
from carts.models import CartItem
from carts.views import _cart_id
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import Q
from django.contrib.auth import get_user_model
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from . forms import ContactSellerForm

def store(request, category_slug=None):
    categories = None
    products = None
    
    # Using slug to find the category, if found filter according to the slug
    if category_slug:
        categories = get_object_or_404(Category, slug = category_slug)
        products = Product.objects.filter(category=categories, status=True, is_approved=True)
        
    # If no slug is passed, redirect to the normal store page
    else:
        # Fetch all products where status is true and order by id 
        products = Product.objects.all().filter(status=True, is_approved=True).order_by('id')
        
    paginator = Paginator(products, 3) 
    page = request.GET.get('page') 
    paged_products = paginator.get_page(page)
    product_count = products.count()
    
    context = {
        'products': paged_products,
        'product_count': product_count,
    }
    
    return render(request, 'store/store.html', context)
    

def product_detail(request, category_slug, product_slug):
    product = get_object_or_404(
        Product,
        category__slug=category_slug,
        slug=product_slug,
        status=True,
    )

    if not product.is_approved and not (request.user.is_staff or request.user == getattr(product, 'owner', None)):
        raise Http404("Product not found")

    in_cart = CartItem.objects.filter(
        cart__cart_id=_cart_id(request),
        product=product
    ).exists()

   
    colors = product.variations.filter(
        variation_category__iexact='color', is_active=True
    ).order_by('id')

    sizes = product.variations.filter(
        variation_category__iexact='size', is_active=True
    ).order_by('id')

    return render(request, 'store/product_detail.html', {
        'product': product,
        'in_cart': in_cart,
        'colors': colors,
        'sizes': sizes,
    })



def search(request):
    keyword = request.GET.get('keyword', '').strip()
    products = Product.objects.none()
    product_count = 0
    
    if not keyword:
        return redirect('home')  # or redirect('home')
    
    products = Product.objects.filter(
        status=True, 
        is_approved=True
        ).order_by('-created_date').filter(
        Q(description__icontains=keyword) | 
        Q (product_name__icontains=keyword)
        )
    product_count = products.count()
            
    context = {
        'products': products,
        'product_count': product_count,
        'keyword': keyword,
    }
    return render(request, 'store/store.html', context)

User = get_user_model()

def seller_profile(request, user_id):
    seller = get_object_or_404(User, pk=user_id)

    qs = Product.objects.filter(owner=seller, status=True, is_approved=True).order_by('-id')
    product_count = qs.count()

    # Optional pagination (12 per page)
    paginator = Paginator(qs, 4)
    page = request.GET.get('page')
    products = paginator.get_page(page)

    context = {
        "seller": seller,
        "products": products,
        "product_count": product_count,
        
        "keyword": "",
    }
    return render(request, "accounts/seller/seller_profile.html",context)

    
def _display_name(user):
    name = f"{getattr(user, 'first_name', '')} {getattr(user, 'last_name', '')}".strip()
    return name or getattr(user, 'email', 'User')
    
@login_required(login_url="user_login")
def message_seller(request, user_id):
    seller = get_object_or_404(User, pk=user_id)

    
    if request.user.pk == seller.pk:
        messages.error(request, "You can't message yourself.")
        return redirect("seller_profile", user_id=seller.pk)

    if request.method == "POST":
        form = ContactSellerForm(request.POST)
        if form.is_valid():
            subject = form.cleaned_data["subject"]
            body = form.cleaned_data["message"]
            buyer = request.user

            product = None
            product_id = request.GET.get("product")
            if product_id:
                from store.models import Product
                try:
                    product = Product.objects.get(pk=product_id)
                except Product.DoesNotExist:
                    product = None

            msg = Message.objects.create(
                sender=buyer,
                receiver=seller,
                subject=subject,
                body=body,
                product=product,   # field is optional on the model
            )

            # 2) Email notification (optional)
            email_subject = f"[Marketplace] {subject}"
            email_body = (
                f"From: {_display_name(buyer)}\n"
                f"Email: {buyer.email}\n\n"
                f"{body}"
            )
            send_mail(
                email_subject,
                email_body,
                getattr(settings, "DEFAULT_FROM_EMAIL", None),
                [seller.email],
                fail_silently=True,
            )

            messages.success(request, "Your message was sent to the seller.")
            # Redirect to messages app detail page (namespaced)
            return redirect("message:message_detail", pk=msg.pk)
    else:
        form = ContactSellerForm()

    return render(request, "messages/message_seller.html", {"seller": seller, "form": form})