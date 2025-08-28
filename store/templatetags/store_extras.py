from django import template

register = template.Library()

@register.filter
def calculate_discount(old_price, current_price):
    """Calculate discount percentage"""
    try:
        if old_price and current_price and old_price > current_price:
            discount = ((old_price - current_price) / old_price) * 100
            return round(discount, 0)
        return 0
    except (ValueError, TypeError):
        return 0

@register.filter
def multiply(value, arg):
    """Multiply the value by the argument"""
    try:
        return float(value) * float(arg)
    except (ValueError, TypeError):
        return 0

@register.filter
def divide(value, arg):
    """Divide the value by the argument"""
    try:
        if float(arg) == 0:
            return 0
        return float(value) / float(arg)
    except (ValueError, TypeError):
        return 0

