from django.contrib import admin
from . models import Category, Product
from django.utils.html import format_html

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'created_date', 'updated_date', 'status')
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ('created_date', 'updated_date') 

    # def image_preview(self, obj):
    #     if obj.product_image:
    #         return format_html('<img src="{}" width="80" height="80" style="object-fit:cover;" />', obj.category_image.url)
    #     return "No image"
    # image_preview.short_description = 'Image'
    

class ProductAdmin(admin.ModelAdmin):
    exclude = ['created_at',]
    list_display = ('name', 'slug', 'category', 'price', 'stock', 'status', 'image_preview')
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ('image_preview',)

    def image_preview(self, obj):
        if obj.product_image:
            return format_html('<img src="{}" width="80" height="80" style="object-fit:cover;" />', obj.product_image.url)
        return "No image"
    image_preview.short_description = 'Image'
    
# Register your models here.
admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)