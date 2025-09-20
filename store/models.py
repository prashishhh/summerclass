# store/models.py
from django.db import models
from django.db.models import Avg, Count
from django.conf import settings
from django.urls import reverse
from category.models import Category

class Product(models.Model):
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="products",
        null=True, blank=True,
    )
    product_name = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    description = models.TextField(max_length=1000, blank=True)
    price = models.IntegerField()
    images = models.ImageField(upload_to='photos/products/', blank=True, null=True)
    stock = models.IntegerField()
    status = models.BooleanField(default=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    old_price = models.IntegerField(null=True, blank=True)

    # approvals / merchandising
    is_approved = models.BooleanField(default=False)
    is_featured = models.BooleanField(default=False)   # <- keep this here

    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def get_url(self):
        return reverse('product_detail', args=[self.category.slug, self.slug])

    def __str__(self):
        return self.product_name
    
    @property
    def average_review(self):
        """Calculate average rating from reviews"""
        reviews = self.review_set.filter(status=True)
        if reviews.exists():
            result = reviews.aggregate(avg_rating=Avg('rating'))
            avg = result['avg_rating']
            if avg is not None:
                return round(float(avg), 1)
        return 0
    
    @property
    def count_review(self):
        """Count total reviews"""
        return self.review_set.filter(status=True).count()


# Use a tuple of tuples (stable ordering) – not a set
VARIATION_CATEGORY_CHOICES = (
    ('color', 'Color'),
    ('size', 'Size'),
)

class VariationManager(models.Manager):
    def colors(self):
        return super().filter(variation_category='color', is_active=True)
    def sizes(self):
        return super().filter(variation_category='size', is_active=True)

class Variation(models.Model):
    product = models.ForeignKey(
        'store.Product',                # string avoids import cycles
        on_delete=models.CASCADE,
        related_name='variations'
    )
    variation_category = models.CharField(max_length=100, choices=VARIATION_CATEGORY_CHOICES)
    variation_value = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now_add=True)

    objects = VariationManager()

    def __str__(self):
        return self.variation_value

class ProductGallery(models.Model):
    product = models.ForeignKey(Product, default=None, on_delete=models.CASCADE, related_name='gallery_images')
    image = models.ImageField(upload_to='photos/products/', max_length=255)

    def __str__(self):
        return self.product.product_name

    class Meta:
        verbose_name = "product gallery"
        verbose_name_plural = "product gallery"

class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    subject = models.CharField(max_length=100, blank=True)
    description = models.TextField(max_length=500, blank=True)
    rating = models.FloatField()
    ip = models.CharField(max_length=20, blank=True)
    status = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.subject
