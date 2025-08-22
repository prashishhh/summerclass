from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from store.models import Product, Variation
from .models import Cart, CartItem
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# Create your views here.

# private helper: get/create session cart id
def _cart_id(request):
    cart = request.session.session_key
    
    # If there is no session, create a new session and return the cart id
    if not cart:
        cart = request.session.create()
    return cart

def add_cart(request, product_id):
    current_user = request.user
    product = get_object_or_404(Product, id=product_id, is_approved=True)
    # If user is authenticated
    if current_user.is_authenticated:
        product_variation = []
        if request.method == 'POST':
            for item in request.POST:
                # If the color is black, the name color will be stored in key
                key = item
                # And the name black will be stored inside value
                value = request.POST[key]

                try:
                    # iexact also ignores small or capital
                    variation = Variation.objects.get(product=product,variation_category__iexact=key, variation_value__iexact=value)
                    product_variation.append(variation)
                except:
                    pass

        # Block owner adding their own product
        if request.user.is_authenticated and getattr(product, "owner_id", None) == request.user.id:
            messages.error(request, "You cannot add your own product to the cart.")
            return redirect(product.get_url())
        
        # Check Out of stock
        if product.stock <= 0:
            messages.info(request, "This item is currently out of stock.")
            return redirect(product.get_url())
        
        # Cart Item
        is_cart_item_exists = CartItem.objects.filter(product=product, user=current_user).exists()
        
        if is_cart_item_exists:
            cart_item = CartItem.objects.filter(product=product, user=current_user)
            
            # existing variations, current variation, item id needed
            # If the current variation is inside the existing variations, then increase
            
            ex_var_list = []
            id = []
            for item in cart_item:
                existing_variation = item.variations.all()
                ex_var_list.append(list(existing_variation))
                id.append(item.id)
                
            if product_variation in ex_var_list:
                # Increase
                index = ex_var_list.index(product_variation)
                item_id = id[index]
                item = CartItem.objects.get(product=product, id=item_id)
                item.quantity += 1
                item.save()
            else:
                item = CartItem.objects.create(product=product, quantity=1, user=current_user)
                if len(product_variation) > 0:
                    item.variations.clear()
                    item.variations.add(*product_variation)
                item.save()
            
            # if cart_item.quantity >= product.stock:
            #     messages.warning(request, "You've reached the available stock for this item.")
            #     return redirect('cart')
        else:
            cart_item = CartItem.objects.create(
                product = product,
                quantity = 1,
                user = current_user
            )
            if len(product_variation) > 0:
                cart_item.variations.clear()
                cart_item.variations.add(*product_variation)
            cart_item.save()
        
        return redirect('cart')
        
    # If user is not authenticated
    
    else:
        product_variation = []
        if request.method == 'POST':
            for item in request.POST:
                # If the color is black, the name color will be stored in key
                key = item
                # And the name black will be stored inside value
                value = request.POST[key]

                try:
                    # iexact also ignores small or capital
                    variation = Variation.objects.get(product=product,variation_category__iexact=key, variation_value__iexact=value)
                    product_variation.append(variation)
                except:
                    pass

        # Block owner adding their own product
        if request.user.is_authenticated and getattr(product, "owner_id", None) == request.user.id:
            messages.error(request, "You cannot add your own product to the cart.")
            return redirect(product.get_url())
        
        # Check Out of stock
        if product.stock <= 0:
            messages.info(request, "This item is currently out of stock.")
            return redirect(product.get_url())
        
        # Cart
        try:
            # Get the cart using the cart_id present in the session
            cart = Cart.objects.get(cart_id=_cart_id(request))
        except Cart.DoesNotExist:
            cart = Cart.objects.create(
                cart_id = _cart_id(request)
            )
        cart.save()
        
        # Cart Item
        is_cart_item_exists = CartItem.objects.filter(product=product, cart=cart).exists()
        if is_cart_item_exists:
            cart_item = CartItem.objects.filter(product=product, cart=cart)
            
            # existing variations, current variation, item id needed
            # If the current variation is inside the existing variations, then increase
            
            ex_var_list = []
            id = []
            for item in cart_item:
                existing_variation = item.variations.all()
                ex_var_list.append(list(existing_variation))
                id.append(item.id)
            if product_variation in ex_var_list:
                # Increase
                index = ex_var_list.index(product_variation)
                item_id = id[index]
                item = CartItem.objects.get(product=product, id=item_id)
                item.quantity += 1
                item.save()
            else:
                item = CartItem.objects.create(product=product, quantity=1, cart=cart)
                if len(product_variation) > 0:
                    item.variations.clear()
                    item.variations.add(*product_variation)
                item.save()
            
            # if cart_item.quantity >= product.stock:
            #     messages.warning(request, "You've reached the available stock for this item.")
            #     return redirect('cart')
        else:
            cart_item = CartItem.objects.create(
                product = product,
                quantity = 1,
                cart = cart #Just saved cart
            )
            if len(product_variation) > 0:
                cart_item.variations.clear()
                cart_item.variations.add(*product_variation)
            cart_item.save()
        
        return redirect('cart')

def remove_cart(request, product_id, cart_item_id):
    # cart = Cart.objects.get(cart_id=_cart_id(request))
    product = get_object_or_404(Product, id=product_id)
    
    try:
        if request.user.is_authenticated:
            cart_item = CartItem.objects.get(product=product, user=request.user, id=cart_item_id)
        else:
            cart = get_object_or_404(Cart, cart_id=_cart_id(request))
            cart_item = CartItem.objects.get(product=product, cart=cart, id=cart_item_id)
    
    except CartItem.DoesNotExist:
        messages.warning(request, "This item is not in your cart.")
        return redirect('cart')
    
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
        
    else:
        cart_item.delete()
        
    return redirect('cart')

def remove_cart_item(request, product_id, cart_item_id):
    product = get_object_or_404(Product, id=product_id)
    
    if request.user.is_authenticated:
        deleted_count, _ = CartItem.objects.filter(product=product, user=request.user, id=cart_item_id).delete()
    
    else:
        cart = get_object_or_404(Cart, cart_id=_cart_id(request))
        deleted_count, _ = CartItem.objects.filter(product=product, cart=cart, id=cart_item_id).delete()
    
    if not deleted_count:
        messages.warning(request, "This item was not in your cart.")
   
    return redirect('cart')


def cart(request, total=0, quantity=0, cart_items = None):
    try:
        tax = 0
        grand_total = 0
        cart_items = []
        
        if request.user.is_authenticated:
            cart_items = CartItem.objects.filter(user=request.user, is_active=True).order_by('id')

        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_items = CartItem.objects.filter(cart=cart, is_active=True).order_by('id')
                
            # Loops through each cart_item
        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)
            quantity += cart_item.quantity
                
        tax = (2 * total)/100
        grand_total = total + tax
                
    except ObjectDoesNotExist:
        pass #Just ignore
    
    context = {
        'total': total,
        'quantity': quantity,
        'cart_items': cart_items,
        'tax': tax,
        'grand_total': grand_total
    }
    return render(request, 'cart/cart.html', context)


@login_required(login_url="user_login")
def checkout(request, total=0, quantity=0, cart_items = None):
    tax = 0
    grand_total = 0
    cart_items = []
    
    try:
        if request.user.is_authenticated:
            cart_items = CartItem.objects.filter(user=request.user, is_active=True).order_by('id')

        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_items = CartItem.objects.filter(cart=cart, is_active=True).order_by('id')
        
        # Loops through each cart_item
        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)
            quantity += cart_item.quantity
        
        tax = (2 * total)/100
        grand_total = total + tax
            
    except ObjectDoesNotExist:
        pass #Just ignore
    
    context = {
        'total': total,
        'quantity': quantity,
        'cart_items': cart_items,
        'tax': tax,
        'grand_total': grand_total
    }
    return render(request, 'cart/checkout.html', context)