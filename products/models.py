from django.db import models
from django.utils import timezone
from django.urls import reverse

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
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=100, unique=True)
    price = models.FloatField()
    description = models.TextField()
    stock = models.IntegerField(default=1)
    status = models.BooleanField(default=0)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)
    updated_date = models.DateTimeField(default=timezone.now)
    product_image = models.ImageField(upload_to='photos/products', blank=True)

    def __str__(self):
        return self.name 
    
    def get_url(self):
        return reverse('product_detail', args=[self.category.slug, self.slug])