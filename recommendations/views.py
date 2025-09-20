from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.utils.timezone import now, timedelta
from django.db.models import Count, Q
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from .models import UserActivity


@require_http_methods(["GET"])
def recently_viewed(request, user_id):
    """
    Return the last 5 products a user has viewed (ordered by timestamp).
    """
    try:
        recent_activities = UserActivity.objects.filter(
            user_id=user_id,
            action='view'
        ).select_related('product').order_by('-timestamp')[:5]
        
        products = []
        for activity in recent_activities:
            products.append({
                'id': activity.product.id,
                'name': activity.product.product_name,
                'image_url': request.build_absolute_uri(activity.product.images.url) if activity.product.images else None,
                'price': float(activity.product.price),
                'timestamp': activity.timestamp.isoformat()
            })
        
        return JsonResponse({
            'success': True,
            'products': products,
            'count': len(products)
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)


@require_http_methods(["GET"])
def also_bought(request, product_id):
    """
    Return the top 5 products that were also bought by users who bought this product.
    Excludes the current product.
    """
    try:
        # Get users who bought the current product
        users_who_bought = UserActivity.objects.filter(
            product_id=product_id,
            action='buy'
        ).values_list('user_id', flat=True)
        
        if not users_who_bought:
            return JsonResponse({
                'success': True,
                'products': [],
                'count': 0,
                'message': 'No purchase history found for this product'
            })
        
        # Find products bought by the same users (excluding current product)
        also_bought_products = UserActivity.objects.filter(
            user_id__in=users_who_bought,
            action='buy'
        ).exclude(
            product_id=product_id
        ).values('product').annotate(
            buy_count=Count('product')
        ).order_by('-buy_count')[:5]
        
        products = []
        for item in also_bought_products:
            product = item['product']
            # Get the actual product object for additional details
            product_obj = UserActivity.objects.filter(
                product_id=product,
                action='buy'
            ).select_related('product').first().product
            
            products.append({
                'id': product_obj.id,
                'name': product_obj.product_name,
                'image_url': request.build_absolute_uri(product_obj.images.url) if product_obj.images else None,
                'price': float(product_obj.price),
                'buy_count': item['buy_count']
            })
        
        return JsonResponse({
            'success': True,
            'products': products,
            'count': len(products)
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)


@require_http_methods(["GET"])
def trending(request):
    """
    Return the top 5 most bought products in the last 7 days.
    """
    try:
        # Calculate date 7 days ago
        seven_days_ago = now() - timedelta(days=7)
        
        # Get products bought in the last 7 days, ordered by purchase count
        trending_products = UserActivity.objects.filter(
            action='buy',
            timestamp__gte=seven_days_ago
        ).values('product').annotate(
            buy_count=Count('product')
        ).order_by('-buy_count')[:5]
        
        products = []
        for item in trending_products:
            product_id = item['product']
            # Get the actual product object for additional details
            product_obj = UserActivity.objects.filter(
                product_id=product_id,
                action='buy'
            ).select_related('product').first().product
            
            products.append({
                'id': product_obj.id,
                'name': product_obj.product_name,
                'image_url': request.build_absolute_uri(product_obj.images.url) if product_obj.images else None,
                'price': float(product_obj.price),
                'buy_count': item['buy_count']
            })
        
        return JsonResponse({
            'success': True,
            'products': products,
            'count': len(products),
            'period': '7 days'
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)
