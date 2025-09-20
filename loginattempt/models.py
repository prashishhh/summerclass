from django.db import models


class LoginAttempt(models.Model):
    username = models.CharField(max_length=150, blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True)
    path = models.CharField(max_length=255)
    attempted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.username} @ {self.ip_address} on {self.attempted_at}"