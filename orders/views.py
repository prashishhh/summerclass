import uuid
import hmac
import base64
import hashlib
import datetime
import random
import string
import json

from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.utils import timezone
from django.urls import reverse
from django.core.mail import EmailMessage
from django.db.models import F
from django.template.loader import render_to_string
from .models import Order, OrderProduct, Payment
from carts.models import CartItem
from store.models import Product
from accounts.models import Account

# --- helpers ---------------------------------------------------------------

def _order_amount(order):
    """Prefer order.order_total; else sum OrderProducts."""
    if hasattr(order, "order_total") and order.order_total:
        try:
            return int(round(float(order.order_total)))
        except Exception:
            pass
    return int(sum(op.product_price * op.quantity for op in order.orderproduct_set.all()))


def _abs(request, name, *args, **kwargs) -> str:
    """Build an absolute URL for callbacks (works on 127.0.0.1 / localhost, etc.)."""
    return request.build_absolute_uri(reverse(name, args=args, kwargs=kwargs))


def _make_signature(total_amount: int, transaction_uuid: str) -> str:
    """
    HMAC-SHA256 over the EXACT string:
      total_amount=<int>,transaction_uuid=<uuid>,product_code=<code>
    Then Base64-encode the MAC bytes (this is what eSewa expects).
    """
    msg = (
        f"total_amount={total_amount},"
        f"transaction_uuid={transaction_uuid},"
        f"product_code={settings.ESEWA_PRODUCT_CODE}"
    )
    mac = hmac.new(
        settings.ESEWA_SECRET_KEY.encode("utf-8"),
        msg=msg.encode("utf-8"),
        digestmod=hashlib.sha256,
    ).digest()
    return base64.b64encode(mac).decode("utf-8")


def generate_order_number():
    """Generate a unique order number"""
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))

@login_required(login_url='user_login')
def place_order(request, total=0, quantity=0):
    current_user = request.user

    # If cart count is 0 or less, redirect back to store
    cart_items = CartItem.objects.filter(user=current_user)
    cart_count = cart_items.count()
    if cart_count <= 0:
        return redirect('store')

    # Totals
    grand_total = 0
    tax = 0

    for cart_item in cart_items:
        total += (cart_item.product.price * cart_item.quantity)
        quantity += cart_item.quantity

    tax = (2 * total) / 100
    grand_total = total + tax

    if request.method == 'POST':
        # Store all billing information in Order table
        data = Order()
        data.user = current_user
        data.first_name = request.POST.get('first_name')
        data.last_name = request.POST.get('last_name')
        data.phone = request.POST.get('phone')
        data.email = request.POST.get('email')
        data.address_line_1 = request.POST.get('address_line_1')
        data.address_line_2 = request.POST.get('address_line_2', '')
        data.country = request.POST.get('country', 'Nepal')
        data.state = request.POST.get('state')
        data.city = request.POST.get('city')
        data.order_note = request.POST.get('order_note', '')
        data.order_total = grand_total
        data.tax = tax
        data.ip = request.META.get('REMOTE_ADDR')
        data.is_ordered = False
        data.save()

        # Generate order number (YYYYMMDD + DB id)
        yr = int(datetime.date.today().strftime('%Y'))
        dt = int(datetime.date.today().strftime('%d'))
        mt = int(datetime.date.today().strftime('%m'))
        d = datetime.date(yr, mt, dt)
        current_date = d.strftime('%Y%m%d')  # e.g. 20250204
        order_number = current_date + str(data.id)
        data.order_number = order_number
        data.save()

        # Fetch the newly created (unpaid) order and go to payments page
        order = Order.objects.get(
            user=current_user,
            is_ordered=False,
            order_number=order_number
        )

        # Create OrderProduct records for each cart item
        for cart_item in cart_items:
            OrderProduct.objects.create(
                order=order,
                user=current_user,
                product=cart_item.product,
                quantity=cart_item.quantity,
                product_price=cart_item.product.price,
                ordered=False  # Will be set to True when payment is completed
            )

        # Redirect to payments page with order ID
        return redirect('payments', order_id=order.id)

    # If not POST: return to checkout
    return redirect('checkout')

@login_required(login_url='user_login')
def payments(request, order_id):
    """Handle payment processing"""
    order = get_object_or_404(Order, id=order_id, user=request.user)
    
    if request.method == 'POST':
        # Handle payment processing here
        # For now, just mark as completed
        order.status = 'Completed'
        order.is_ordered = True
        order.save()
        
        # Mark all OrderProduct records as ordered
        OrderProduct.objects.filter(order=order).update(ordered=True)
        
        # Create payment record
        Payment.objects.create(
            user=request.user,
            payment_id=f"PAY-{order.order_number}",
            payment_method='Cash on Delivery',
            amount_paid=str(order.order_total),
            status='Completed'
        )
        
        return redirect('order_complete', order_id=order.id)
    
    # Calculate totals from order
    total = order.order_total - order.tax if order.tax else order.order_total
    tax = order.tax or 0
    grand_total = order.order_total
    
    # Get cart items for display (if needed)
    cart_items = CartItem.objects.filter(user=request.user, is_active=True)
    
    context = {
        'order': order,
        'total': total,
        'tax': tax,
        'grand_total': grand_total,
        'cart_items': cart_items,
    }
    return render(request, 'orders/payments.html', context)

def esewa_start(request, order_id):
    """
    Build a signed form and auto-submit to eSewa UAT/Prod (depending on your settings).
    Renders a tiny template that posts to settings.ESEWA_FORM_URL.
    """
    from .models import Order  # avoid circular imports if any

    # 1) Fetch order and compute payable amounts
    order = get_object_or_404(Order, id=order_id, user=request.user)

    # Use stored totals if present; fall back to 0
    total_amount = int(round(float(order.order_total or 0)))
    tax = int(round(float(order.tax or 0)))
    amount = total_amount - tax
    if amount < 0:
        amount = total_amount  # if tax hasn't been set yet

    # 2) Unique transaction UUID (letters/digits/hyphen only)
    txn_uuid = f"{order.order_number or order.id}-{uuid.uuid4().hex[:8]}"

    # 3) Prepare the form payload required by eSewa
    form = {
        "amount": int(amount),
        "tax_amount": int(tax),
        "total_amount": int(total_amount),
        "transaction_uuid": txn_uuid,
        "product_code": settings.ESEWA_PRODUCT_CODE,
        "product_service_charge": 0,
        "product_delivery_charge": 0,
        "success_url": _abs(request, "esewa_return", order_id=order.id),
        "failure_url": _abs(request, "esewa_return", order_id=order.id),
        "signed_field_names": "total_amount,transaction_uuid,product_code",
        "signature": _make_signature(total_amount, txn_uuid),
    }

    # 4) Render a form that auto-submits to eSewa
    return render(
        request,
        "orders/esewa_redirect.html",
        {
            "ESEWA_FORM_URL": settings.ESEWA_FORM_URL,  # e.g. UAT endpoint
            "form": form,
        },
    )

def esewa_return(request, order_id):
    """
    TEST/UAT handler:
    - Read Base64 'data'/'response' from eSewa.
    - If status == COMPLETE:
        * create Payment (or get existing)
        * link order.payment, set order.is_ordered = True (and optional status)
        * create OrderProducts from cart (once), copy variations, decrement stock
        * or, if already created, ensure they're linked & marked ordered
        * send order confirmation email
        * redirect to order_complete with ?order_number & ?payment_id
    - Else: show error and redirect home.
    """
    order = get_object_or_404(Order, id=order_id, user=request.user)

    # eSewa returns Base64-encoded JSON in ?data or ?response (GET/POST)
    encoded = (
        request.GET.get("data")
        or request.POST.get("data")
        or request.GET.get("response")
        or request.POST.get("response")
    )

    payload, status, txn_code = {}, "", ""
    if encoded:
        try:
            payload = json.loads(base64.b64decode(encoded).decode("utf-8"))
            status = str(payload.get("status", "")).upper()
            txn_code = payload.get("transaction_code", "")  # e.g., "000AWE0"
        except Exception:
            # keep status blank → will go to failure branch
            pass

    if status == "COMPLETE":
        # 1) Ensure Payment exists
        amount_paid = _order_amount(order)
        payment, _ = Payment.objects.get_or_create(
            user=order.user,
            payment_id=txn_code or f"esewa-{order.id}",
            defaults={
                "payment_method": "eSewa",
                "amount_paid": str(amount_paid),
                "status": "COMPLETED",
            },
        )

        # 2) Create OrderProducts from cart once (and decrement stock)
        if not order.orderproduct_set.exists() and CartItem:
            cart_items = (
                CartItem.objects.filter(user=order.user)
                .select_related("product")
            )
            for item in cart_items:
                op = OrderProduct.objects.create(
                    order=order,
                    payment=payment,
                    user=order.user,
                    product=item.product,
                    quantity=item.quantity,
                    product_price=item.product.price,
                    ordered=True,
                )
                # copy variations if present
                if hasattr(item, "variations"):
                    op.variations.set(item.variations.all())

                # atomic stock decrement
                Product.objects.filter(pk=item.product_id).update(
                    stock=F("stock") - item.quantity
                )

            # clear cart after migration
            cart_items.delete()
        else:
            # items already created earlier → ensure linked & ordered
            for op in order.orderproduct_set.all():
                if getattr(op, "payment_id", None) != payment.id:
                    op.payment = payment
                if not op.ordered:
                    op.ordered = True
                op.save(update_fields=["payment", "ordered"])

        # 3) Send order confirmation email (best-effort)
        items = order.orderproduct_set.select_related("product").prefetch_related("variations")
        amount_paid = _order_amount(order)  # recompute for email
        mail_subject = "Thank you for your order!"
        message = render_to_string(
            "orders/order_received_email.html",
            {
                "user": request.user,
                "order": order,
                "items": items,
                "amount_paid": amount_paid,
            },
        )
        to_email = request.user.email
        try:
            EmailMessage(mail_subject, message, to=[to_email]).send()
        except Exception:
            messages.warning(
                request,
                "Order received, but we couldn't send the email. Contact admin.",
            )

        # 4) Mark order completed
        order.payment = payment
        order.is_ordered = True
        if hasattr(order, "status"):
            order.status = "Accepted"  # optional: match your STATUS choices
        order.save()

        # 5) Redirect to order_complete (with expected query params)
        url = reverse("order_complete")
        return redirect(f"{url}?order_number={order.order_number}&payment_id={payment.payment_id}")

    # Failure / user canceled / invalid payload
    messages.error(request, "eSewa (TEST): Payment was not completed.")
    return redirect("home")

def order_complete(request):
    order_number = request.GET.get('order_number')
    transID = request.GET.get('payment_id')

    # 1) Fetch the order (must be completed)
    try:
        order = Order.objects.get(order_number=order_number, is_ordered=True)
    except Order.DoesNotExist:
        return redirect('home')

    # 2) Get the payment linked on the order (or try to resolve it)
    payment = getattr(order, "payment", None)

    if payment is None:
        # try most specific: by payment_id for this user
        qs = Payment.objects.filter(
            payment_id=transID, user=order.user
        ).order_by('-created_at')
        payment = qs.first()
        if payment:
            order.payment = payment
            order.save(update_fields=['payment'])
        else:
            # last resort: any payment with that id
            qs_any = Payment.objects.filter(payment_id=transID).order_by('-created_at')
            payment = qs.first()
            if payment:
                order.payment = payment
                order.save(update_fields=['payment'])
            else:
                return redirect('home')

    # 3) Fetch items and compute subtotal
    ordered_products = OrderProduct.objects.filter(order_id=order.id)

    subtotal = 0
    for i in ordered_products:
        subtotal += i.product_price * i.quantity

    # 4) Render receipt page
    context = {
        'order': order,
        'ordered_products': ordered_products,
        'order_number': order.order_number,
        'transID': payment.payment_id,
        'payment': payment,
        'subtotal': subtotal,
    }
    return render(request, 'orders/order_complete.html', context)
