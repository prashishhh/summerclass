# Django Recommendation System

A production-ready recommendation system for Django that provides personalized product recommendations based on user behavior.

## Features

- **Recently Viewed Products**: Track and retrieve the last 5 products a user has viewed
- **Also Bought Recommendations**: Find products commonly bought together
- **Trending Products**: Identify the most popular products in the last 7 days
- **User Activity Tracking**: Monitor user interactions with products

## Installation

1. Add `'recommendations.apps.RecommendationsConfig'` to `INSTALLED_APPS` in `settings.py`
2. Add `path('recommend/', include('recommendations.urls'))` to your main `urls.py`
3. Run migrations: `python manage.py makemigrations recommendations && python manage.py migrate`

## API Endpoints

### 1. Recently Viewed Products
```
GET /recommend/recently-viewed/<user_id>/
```
Returns the last 5 products viewed by a specific user.

**Response:**
```json
{
    "success": true,
    "products": [
        {
            "id": 1,
            "name": "Product Name",
            "image_url": "http://example.com/image.jpg",
            "price": 99.99,
            "timestamp": "2024-01-01T12:00:00Z"
        }
    ],
    "count": 1
}
```

### 2. Also Bought Recommendations
```
GET /recommend/also-bought/<product_id>/
```
Returns products commonly bought by users who also bought the specified product.

**Response:**
```json
{
    "success": true,
    "products": [
        {
            "id": 2,
            "name": "Related Product",
            "image_url": "http://example.com/image2.jpg",
            "price": 149.99,
            "buy_count": 5
        }
    ],
    "count": 1
}
```

### 3. Trending Products
```
GET /recommend/trending/
```
Returns the top 5 most bought products in the last 7 days.

**Response:**
```json
{
    "success": true,
    "products": [
        {
            "id": 3,
            "name": "Trending Product",
            "image_url": "http://example.com/image3.jpg",
            "price": 199.99,
            "buy_count": 12
        }
    ],
    "count": 1,
    "period": "7 days"
}
```

## Usage

### Tracking User Activities

Use the utility functions to track user behavior:

```python
from recommendations.utils import track_product_view, track_product_purchase

# Track when a user views a product
track_product_view(request.user, product)

# Track when a user purchases a product
track_product_purchase(request.user, product)
```

### Getting Personalized Recommendations

```python
from recommendations.utils import get_user_recommendations

# Get recommendations for a user
recommendations = get_user_recommendations(user, limit=5)
```

## Models

### UserActivity
- `user`: ForeignKey to User model
- `product`: ForeignKey to Product model
- `action`: Choice field ('view' or 'buy')
- `timestamp`: DateTime field with auto-now

## Database Optimization

The system includes database indexes for optimal performance:
- Composite index on (user, action, timestamp)
- Composite index on (product, action, timestamp)

## Error Handling

All endpoints return consistent JSON responses with:
- `success`: Boolean indicating if the request was successful
- `error`: Error message if something went wrong
- Appropriate HTTP status codes

## Testing

Run tests with:
```bash
python manage.py test recommendations
```

## Extending the System

The modular design makes it easy to add new recommendation algorithms:
1. Add new methods to `views.py`
2. Update `urls.py` with new endpoints
3. Add corresponding tests in `tests.py`

## Performance Considerations

- Uses `select_related()` to minimize database queries
- Implements database indexes for common query patterns
- Limits results to prevent performance issues
- Uses Django ORM for database compatibility
