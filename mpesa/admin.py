from re import A
from django.contrib import admin

from mpesa.models import AccessToken

# Register your models here.
class AccessTokenAdmin(admin.ModelAdmin):
    list_display = ["token", "created_at"]
    list_filter = ('created_at',)
    ordering = ["created_at"]
    
admin.site.register(AccessToken, AccessTokenAdmin)