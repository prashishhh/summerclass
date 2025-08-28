from django import template

register = template.Library()

@register.filter
def multiply(value, arg):
    """Multiply the value by the argument"""
    try:
        return float(value) * float(arg)
    except (ValueError, TypeError):
        return 0

@register.filter
def cart_subtotal(price, quantity):
    """Calculate subtotal for cart item"""
    try:
        return float(price) * float(quantity)
    except (ValueError, TypeError):
        return 0

