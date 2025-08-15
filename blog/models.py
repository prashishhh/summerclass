from django.db import models
from django.utils import timezone

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Blog(models.Model):
    title = models.CharField(max_length = 255)
    author = models.CharField(max_length = 255)
    content = models.TextField()
    category = models.ForeignKey(Category, on_delete = models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)
    blog_image = models.ImageField(upload_to='photos/blogs', blank=True)

    def __str__(self):
        return self.title