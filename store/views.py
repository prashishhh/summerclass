from django.shortcuts import render, get_object_or_404, redirect
from django.http import Http404
from . models import Product, ProductGallery
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
from . forms import ContactSellerForm, ReviewForm
from .models import Review

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
    
    # Apply price range filter
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    
    if min_price and min_price.isdigit():
        products = products.filter(price__gte=int(min_price))
    if max_price and max_price.isdigit():
        products = products.filter(price__lte=int(max_price))
    
    # Apply sorting
    sort_by = request.GET.get('sort', 'newest')
    
    if sort_by == 'price-low':
        products = products.order_by('price')
    elif sort_by == 'price-high':
        products = products.order_by('-price')
    elif sort_by == 'popular':
        # Order by most viewed/popular (you can customize this logic)
        products = products.order_by('-created_date')  # For now, using created_date as popularity
    else:  # newest first (default)
        products = products.order_by('-created_date')
    
    # Remove pagination - show all products
    # paginator = Paginator(products, 3) 
    # page = request.GET.get('page') 
    # paged_products = paginator.get_page(page)
    product_count = products.count()
    
    context = {
        'products': products,  # Use products directly instead of paged_products
        'product_count': product_count,
        'category_slug': category_slug,
        'min_price': min_price or '',
        'max_price': max_price or '',
        'sort_by': sort_by,
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

   
    # Get product gallery images
    product_gallery = ProductGallery.objects.filter(product_id=product.id)
    
    # Get order product info (if user has ordered this product)
    order_product = None
    if request.user.is_authenticated:
        from orders.models import OrderProduct
        order_product = OrderProduct.objects.filter(
            user=request.user,
            product=product
        ).first()
    
    # Get reviews for this product
    reviews = []
    try:
        reviews = Review.objects.filter(product=product, status=True).order_by('-created_date')
    except:
        # Reviews might not exist yet
        pass

    colors = product.variations.filter(
        variation_category__iexact='color', is_active=True
    ).order_by('id')

    sizes = product.variations.filter(
        variation_category__iexact='size', is_active=True
    ).order_by('id')

    context = {
        'product': product,
        'in_cart': in_cart,
        'order_product': order_product,
        'reviews': reviews,
        'product_gallery': product_gallery,
        'colors': colors,
        'sizes': sizes,
    }
    
    return render(request, 'store/product_detail.html', context)



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

@login_required(login_url="user_login")
def submit_review(request, product_id):
    url = request.META.get('HTTP_REFERER')

    if request.method != 'POST':
        return redirect(url)

    # If a review exists for this user+product, update it; otherwise create new
    existing = Review.objects.filter(user_id=request.user.id, product_id=product_id).order_by('-id').first()

    form = ReviewForm(request.POST, instance=existing) if existing else ReviewForm(request.POST)

    if form.is_valid():
        data = form.save(commit=False)
        data.user_id = request.user.id
        data.product_id = product_id
        data.ip = request.META.get('REMOTE_ADDR')
        data.save()
        messages.success(request, f"Thank you! Your review has been {'updated' if existing else 'submitted'}.")
    else:
        messages.error(request, "Please correct the errors in your review.")

    return redirect(url)