from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()


class UserActivity(models.Model):
    ACTION_CHOICES = [
        ('view', 'View'),
        ('buy', 'Buy'),
    ]
    
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='activities'
    )
    product = models.ForeignKey(
        'store.Product',
        on_delete=models.CASCADE,
        related_name='user_activities'
    )
    action = models.CharField(
        max_length=10,
        choices=ACTION_CHOICES,
        default='view'
    )
    timestamp = models.DateTimeField(
        default=timezone.now
    )
    
    class Meta:
        verbose_name_plural = 'User Activities'
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['user', 'action', 'timestamp']),
            models.Index(fields=['product', 'action', 'timestamp']),
        ]
    
    def __str__(self):
        return f"{self.user.username} {self.action}ed {self.product.product_name} at {self.timestamp}"
