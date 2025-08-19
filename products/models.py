from django.db import models
from django.utils import timezone
from django.urls import reverse
from django.conf import settings

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    category_image = models.ImageField(upload_to="photos/categories/", blank=True)
    created_date = models.DateTimeField(default=timezone.now)
    updated_date = models.DateTimeField(default=timezone.now)
    status = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def get_url(self):
        return reverse('products_by_category', args=[self.slug])
    def __str__(self):
        return self.name 



    
class Product(models.Model):
    # who submitted it
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="products",
        null=True, blank=True,  # allow old admin-created rows
    )
    name = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    description = models.TextField(max_length=1000, blank=True)
    price = models.FloatField()
    product_image = models.ImageField(upload_to="photos/products/")
    stock = models.IntegerField()
    status = models.BooleanField(default=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    # single approval switch
    is_approved = models.BooleanField(default=False)

    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def get_url(self):
        # category.slug and self.slug
        return reverse("product_detail", args=[self.category.slug, self.slug])

    def __str__(self):
        return self.name