from django.contrib import admin
from . models import SiteSetting

class SiteSettingAdmin(admin.ModelAdmin):
    list_display = ['site_title',]

# Register your models here.
admin.site.register(SiteSetting, SiteSettingAdmin)