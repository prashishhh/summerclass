from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required
from django.utils.text import slugify
from django.core.paginator import Paginator
from django.db import transaction
from django.db.models import F

from .forms import RegistrationForm, ProfileUpdateForm
from .models import Account
from products.forms import ProductForm
from products.models import Product
#from waitlist.models import StockRequest
#from message.models import Message

def user_login(request):
    if request.method == "POST":
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '')

        # Returns user object
        user = auth.authenticate(email=email, password=password)

        if user is not None:
            auth.login(request, user)
            messages.success(request, "You are now logged in.")

            # Redirect to next page if provided
            next_url = request.GET.get('next') or request.POST.get('next')
            if next_url:
                return redirect(next_url)
            return redirect('home')

        else:
            messages.error(request, "Invalid login credentials.")
            return redirect('user_login')

    # return render(request, 'accounts/login.html')
    return render(request, 'accounts/login.html', {'next': request.GET.get('next')})

def user_register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            phone_number = form.cleaned_data['phone_number']
            password = form.cleaned_data['password']
            username = email.split("@")[0]

            # We cannot add phone number here, as in the create_user method this is not there
            user = Account.objects.create_user(
                first_name=first_name,
                last_name=last_name,
                username=username,
                email=email,
                password=password,
            )

            # Updates the user object
            user.phone_number = phone_number
            user.save()
            messages.success(request, "Registration Successful")
            return redirect('user_register')
    else:
        form = RegistrationForm()

    context = {
        'form': form
    }
    return render(request, 'accounts/register.html', context)

@login_required(login_url='user_login')
def user_logout(request):
    auth.logout(request)
    messages.success(request, "You are logged out.")
    return redirect('home')

@login_required(login_url='user_login')
def user_dashboard(request):
    user = request.user
    # Products posted by this user
    my_products_qs = Product.objects.filter(owner=user)

    context = {
        # Product stats (seller side)
        "my_products_total": my_products_qs.count(),
        "my_products_approved": my_products_qs.filter(is_approved=True).count(),
        "my_products_pending": my_products_qs.filter(is_approved=False).count(),
        "my_products_active": my_products_qs.filter(status=True).count(),
        "my_products_inactive": my_products_qs.filter(status=False).count(),
    }

    return render(request, 'accounts/dashboard.html', context)

@login_required(login_url='user_login')
def my_products(request):
    qs = (
        Product.objects
        .filter(owner=request.user)
        .select_related('category')
        .order_by('-created_date')
    )

    # Quick stats
    stats = {
        "total": qs.count(),
        "approved": qs.filter(is_approved=True).count(),
        "pending": qs.filter(is_approved=False).count(),
        "inactive": qs.filter(status=False).count(),
    }

    paginator = Paginator(qs, 10)
    page = request.GET.get('page')
    products = paginator.get_page(page)

    return render(request, "accounts/my_products.html", {
        "products": products,
        "stats": stats,
    })

@login_required(login_url='user_login')
def delete_product(request, product_id):
    p = get_object_or_404(Product, id=product_id, owner=request.user)
    p.delete()
    messages.success(request, "Product deleted.")
    return redirect('my_products')


@login_required(login_url='user_login')
def edit_product(request, product_id):
    # p = get_object_or_404(Product, id=product_id, owner=request.user)
    product = get_object_or_404(Product, id=product_id, owner=request.user)
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, "Product updated.")
            return redirect("my_products")
    else:
        form = ProductForm(instance=product)
    return render(request, "accounts/add_product.html", {"form": form})

@login_required(login_url='user_login')
def add_product(request):
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            p = form.save(commit=False)
            p.owner = request.user
            p.is_approved = False  # pending by default

            # Auto slug (unique)
            base = slugify(p.product_name)
            slug = base or "product"
            i = 1
            while Product.objects.filter(slug=slug).exists():
                i += 1
                slug = f"{base}-{i}"
            p.slug = slug

            p.save()
            messages.success(request, "Submitted! Waiting for admin approval.")
            return redirect("my_products")
    else:
        form = ProductForm()

    return render(request, "accounts/add_product.html", {"form": form})

@login_required(login_url='user_login')
def edit_profile(request):
    if request.method == "POST":
        form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully.")
            return redirect('edit_profile')
    else:
        form = ProfileUpdateForm(instance=request.user)

    return render(request, 'accounts/edit_profile.html', {"form": form})

