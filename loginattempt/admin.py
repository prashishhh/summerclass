from django.contrib import admin
from .models import LoginAttempt

class LoginAttemptAdmin(admin.ModelAdmin):
    list_display = ("username", "ip_address", "attempted_at")
    search_fields = ("username", "ip_address", "user_agent")
    list_filter = ("attempted_at",)

admin.site.register(LoginAttempt, LoginAttemptAdmin)