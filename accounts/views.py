from django.shortcuts import render
from .forms import RegistrationForm
from . models import Account
from django.shortcuts import redirect, get_object_or_404, HttpResponse
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required
from .forms import ProfileUpdateForm
from store.forms import ProductForm
from django.utils.text import slugify
from store.models import Product
from orders.models import Order, OrderProduct
from django.core.paginator import Paginator
from django.db import transaction
from django.db.models import F
from carts.models import Cart, CartItem
# Password change
from . forms import CustomPasswordChangeForm, CustomPasswordResetForm, CustomSetPasswordForm
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.views import PasswordResetView, PasswordResetConfirmView

# Email verification
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage

from carts.views import _cart_id

def user_login(request):
    if request.method == "POST":
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '')
        
        # Returns user object
        user = auth.authenticate(email=email, password=password)
        
        if user is not None:
            try:
                cart = Cart.objects.get(cart_id=_cart_id(request))
                is_cart_item_exists = CartItem.objects.filter(cart=cart).exists()
                if is_cart_item_exists:
                    cart_item = CartItem.objects.filter(cart=cart)
                    
                    # Getting product variation by cart id
                    product_variation = []
                    for item in cart_item:
                        variation = item.variations.all()
                        product_variation.append(list(variation))
                    
                    # Get the cart items from the user to access his product variations
                    cart_item = CartItem.objects.filter(user=user)
            
                    # existing variations, current variation, item id needed
                    # If the current variation is inside the existing variations, then increase
                    
                    ex_var_list = []
                    id = []
                    for item in cart_item:
                        existing_variation = item.variations.all()
                        ex_var_list.append(list(existing_variation))
                        id.append(item.id)
                    
                    # product_variation = [1, 2, 3, 4, 6]
                    # ex_var_list = [4, 5, 3, 5]
                    for pr in product_variation:
                        if pr in ex_var_list:
                            index = ex_var_list.index(pr)
                            item_id = id[index]
                            item = CartItem.objects.get(id=item_id)
                            item.quantity += 1
                            item.user = user
                            item.save()
                        else:
                            cart_item = CartItem.objects.filter(cart=cart)
                            for item in cart_item:
                                item.user = user
                                item.save()
            except:
                pass
            auth.login(request, user)
            messages.success(request, "You are now logged in.")
            # Redirect to next page if provided
            next_url = request.GET.get('next') or request.POST.get('next')
            if next_url:
                return redirect(next_url)
            return redirect('user_dashboard')
        
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
            
            # User Activation
            current_site = get_current_site(request)
            mail_subject = 'Please Activate your account'
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = default_token_generator.make_token(user)
            message = render_to_string('accounts/verification/account_verification.html', {
                'user': user,
                'domain': current_site,
                # Encoding user id with url safe base 64 encode so noone can see the pk
                'uid': uid,
                # Creates token for this user, later we check token upon verification
                'token': token
            })
            to_email = email
            try:
                send_email = EmailMessage(
                    mail_subject, message, to=[to_email]
                )
                send_email.send()
                # messages.success(request, "Account created. Check your email to activate your account.")
            except Exception:
                messages.warning(request, "Account created, but we couldn't send the email. Ask admin to activate you.")
            
            return redirect("/accounts/login/?command=verification&email="+email)
            
    else:
        form = RegistrationForm()
    
    context = {
        'form': form
    }
    return render(request, 'accounts/register.html', context)


@login_required(login_url = 'user_login')
def user_logout(request):
    auth.logout(request)
    messages.success(request, "You are logged out.")
    return redirect('home')

def account_activate(request, uidb64, token):
    try:
        # Decodes the uidb and stores in uid, gives pk of user
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None
    
    # Checks the token
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, "Congratulations! Your  account is activated.")
        return redirect('user_login')
    else:
        messages.error(request, "Invalid Activation Link")
        return redirect('user_register')


@login_required(login_url = 'user_login')
def user_dashboard(request):
    user = request.user
    
    # Products posted by this user
    my_products_qs = Product.objects.filter(owner=user)
    
    # Orders received by this user (buyer)
    my_orders_qs = Order.objects.filter(user=user, is_ordered=True)
    
    # Sales made by this user (seller)
    my_sales_qs = OrderProduct.objects.filter(
        product__owner=user, 
        order__is_ordered=True
    )
    
    # Calculate total sales amount
    total_sales_amount = sum(
        sale.product_price * sale.quantity 
        for sale in my_sales_qs
    )
    
    context = {
        # Product stats (seller side)
        "my_products_total": my_products_qs.count(),
        "my_products_approved": my_products_qs.filter(is_approved=True).count(),
        "my_products_pending": my_products_qs.filter(is_approved=False).count(),
        "my_products_active": my_products_qs.filter(status=True).count(),
        "my_products_inactive": my_products_qs.filter(status=False).count(),
        
        # Order stats (buyer side)
        "received_orders_total": my_orders_qs.count(),
        "total_orders": my_orders_qs.count(),
        "recent_orders": my_orders_qs.order_by('-created_at')[:5],
        
        # Sales stats (seller side)
        "total_sales": my_sales_qs.count(),
        "total_sales_amount": total_sales_amount,
        "recent_sales": my_sales_qs.order_by('-created_at')[:5],
        
    }
    return render(request, 'accounts/dashboard.html', context)


@login_required(login_url='user_login')
def my_products(request):
    qs = (
        Product.objects.filter(
        owner=request.user
        ).select_related('category')
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
def my_orders(request):
    orders = Order.objects.filter(user=request.user, is_ordered=True).order_by('-created_at')
    context = {
        'orders': orders
    }
    return render(request, 'accounts/my_orders.html', context)

@login_required(login_url='user_login')
def my_sales(request):
    data = (
        OrderProduct.objects
        .filter(product__owner=request.user, order__is_ordered=True)   # items for my products
        .select_related('order', 'product', 'user')                   # optimize queries
        .prefetch_related('variations')                               # load variations
        .order_by('-created_at')
    )
    context = {
        'data': data,
        'order_status_choices': OrderProduct.DELIVERY_CHOICES
    }
    return render(request, 'orders/my_sales.html', context)

@login_required(login_url='user_login')
def update_delivery_status(request, order_product_id):
    item = get_object_or_404(
        OrderProduct,
        id=order_product_id,
        product__owner=request.user
    )

    if request.method == "POST":
        new_status = request.POST.get("status")
        valid = dict(OrderProduct.DELIVERY_CHOICES)

        if new_status not in valid:
            messages.error(request, "Invalid status.")
            return redirect("my_sales")

        if item.delivery_status == new_status:
            messages.info(request, f"Status already {valid[new_status]}.")
            return redirect("my_sales")

        item.delivery_status = new_status
        item.save(update_fields=["delivery_status",])
        
        # notify buyer
        order = item.order
        buyer = order.user
        status_label = valid[new_status]  # e.g. "Shipped"

        mail_subject = f"Your order {order.order_number} is now {status_label}"

        email_body = render_to_string("emails/delivery_status.html", {
            "user": buyer,
            "order": order,
            "item": item,
            "status": new_status,
            "status_label": status_label,
        })

        try:
            msg = EmailMessage(mail_subject, email_body, to=[buyer.email])
            msg.content_subtype = "html"  # Sends as HTML
            msg.send()
        except Exception:
            messages.warning(
                request,
                "Status updated, but we couldn't send the email notification."
            )

        messages.success(request, f"Updated to {valid[new_status]}.")
        return redirect("my_sales")
    
    # If not POST, redirect to my_sales
    return redirect("my_sales")

@login_required(login_url='user_login')
def order_detail(request, order_id):
    user = request.user

    # buyer's orders
    buyer_qs = Order.objects.filter(order_number=order_id, user=user)

    # seller's orders (any product they own)
    seller_qs = Order.objects.filter(
        order_number=order_id,
        orderproduct__product__owner=user
    )

    order = (buyer_qs | seller_qs).distinct().first()

    if not order:
        return render(request, 'master/404.html', status=404)

    # fetch order products
    order_detail = OrderProduct.objects.filter(order=order)
    subtotal = 0
    for i in order_detail:
        subtotal += i.product_price * i.quantity

    context = {
        'order_detail': order_detail,
        'order': order,
        'subtotal': subtotal,
    }
    return render(request, 'orders/order_detail.html', context)

@login_required(login_url = 'user_login')
def add_product(request):
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            p = form.save(commit=False)
            p.owner = request.user
            p.is_approved = False     # pending by default
            
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


@login_required(login_url = 'user_login')
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

@login_required(login_url = 'user_login')
def change_password(request):
    if request.method == "POST":
        form = CustomPasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            # Keep the user logged in after password change
            update_session_auth_hash(request, user)
            messages.success(request, "Your password was updated successfully.")
            return redirect("user_dashboard")
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = CustomPasswordChangeForm(request.user)
    return render(request, 'accounts/change_password.html', {'form': form})


# Password Reset Views
class CustomPasswordResetView(PasswordResetView):
    """
    Custom password reset view with professional styling
    """
    template_name = 'accounts/password_reset.html'
    form_class = CustomPasswordResetForm
    email_template_name = 'accounts/password_reset_email.txt'
    subject_template_name = 'accounts/password_reset_subject.txt'
    success_url = '/accounts/password-reset/done/'
    html_email_template_name = 'accounts/password_reset_email.html'
    
    def form_valid(self, form):
        # Send HTML email manually
        from django.template.loader import render_to_string
        from django.core.mail import EmailMultiAlternatives
        from django.contrib.sites.shortcuts import get_current_site
        
        email = form.cleaned_data['email']
        try:
            user = Account.objects.get(email=email, is_active=True)
        except Account.DoesNotExist:
            # Don't reveal if email exists
            pass
        else:
            # Send HTML email
            current_site = get_current_site(self.request)
            context = {
                'user': user,
                'domain': current_site.domain,
                'site_name': current_site.name,
                'protocol': 'https' if self.request.is_secure() else 'http',
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            }
            
            subject = 'Password Reset Request - ' + current_site.name
            html_content = render_to_string('accounts/password_reset_email.html', context)
            text_content = render_to_string('accounts/password_reset_email.txt', context)
            
            email_msg = EmailMultiAlternatives(subject, html_content, None, [email])
            email_msg.content_subtype = "html"
            email_msg.attach_alternative(text_content, "text/plain")
            email_msg.send()
        
        # Add success message
        messages.success(
            self.request, 
            "Password reset instructions have been sent to your email address."
        )
        return redirect(self.success_url)
    
    def form_invalid(self, form):
        # Even for invalid forms, don't reveal if email exists
        messages.success(
            self.request, 
            "Password reset instructions have been sent to your email address."
        )
        return redirect(self.success_url)
    
    def send_mail(self, subject_template_name, email_template_name, context, from_email, to_email, html_email_template_name=None, extra_email_context=None):
        """
        Send a django.core.mail.EmailMultiAlternatives to `to_email`.
        """
        from django.template.loader import render_to_string
        from django.core.mail import EmailMultiAlternatives
        
        subject = render_to_string(subject_template_name, context)
        # Email subject *must not* contain newlines
        subject = ''.join(subject.splitlines())
        
        # Render both HTML and text versions
        html_content = render_to_string('accounts/password_reset_email.html', context)
        text_content = render_to_string('accounts/password_reset_email.txt', context)
        
        # Create the email with HTML as primary content
        email = EmailMultiAlternatives(subject, html_content, from_email, [to_email])
        email.content_subtype = "html"  # Set content type to HTML
        email.attach_alternative(text_content, "text/plain")
        email.send()


class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    """
    Custom password reset confirmation view
    """
    template_name = 'accounts/password_reset_confirm.html'
    form_class = CustomSetPasswordForm
    success_url = '/accounts/password-reset/complete/'
    
    def form_valid(self, form):
        # Add success message
        messages.success(
            self.request, 
            "Your password has been successfully reset. You can now log in with your new password."
        )
        return super().form_valid(form)