# store/models.py
from django.db import models
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
