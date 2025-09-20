from django.contrib import admin
from .models import UserActivity


@admin.register(UserActivity)
class UserActivityAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'action', 'timestamp']
    list_filter = ['action', 'timestamp']
    search_fields = ['user__username', 'product__product_name']
    readonly_fields = ['timestamp']
    ordering = ['-timestamp']
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user', 'product')
