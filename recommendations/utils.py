from django.utils import timezone
from .models import UserActivity
from django.db.models import Count


def track_product_view(user, product):
    """
    Track when a user views a product.
    """
    if user.is_authenticated:
        UserActivity.objects.create(
            user=user,
            product=product,
            action='view',
            timestamp=timezone.now()
        )


def track_product_purchase(user, product):
    """
    Track when a user purchases a product.
    """
    if user.is_authenticated:
        UserActivity.objects.create(
            user=user,
            product=product,
            action='buy',
            timestamp=timezone.now()
        )


def get_user_recommendations(user, limit=5):
    """
    Get personalized recommendations for a user based on their activity.
    """
    if not user.is_authenticated:
        return []
    
    # Get products the user has viewed or bought
    user_products = UserActivity.objects.filter(
        user=user
    ).values_list('product_id', flat=True).distinct()
    
    if not user_products:
        return []
    
    # Find similar users (users who interacted with the same products)
    similar_users = UserActivity.objects.filter(
        product_id__in=user_products
    ).exclude(
        user=user
    ).values_list('user_id', flat=True).distinct()
    
    if not similar_users:
        return []
    
    # Get products liked by similar users
    recommended_products = UserActivity.objects.filter(
        user_id__in=similar_users,
        action='buy'
    ).exclude(
        product_id__in=user_products
    ).values('product').annotate(
        score=Count('user')
    ).order_by('-score')[:limit]
    
    return recommended_products
