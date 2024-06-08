from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import *

# Register your models here.
class UserAdmin(BaseUserAdmin):
    list_display = ["id","username", "email", "is_admin"]
    list_filter = ["is_admin"]
    search_fields = ["email"]
    ordering = ["email"]
    filter_horizontal = []
    fieldsets = (
        (None, {'fields': ('email', 'password',)}),
        ('Personal info', {'fields': ('username',)}),
        ('Permissions', {'fields': ('is_active',"is_admin")}),
        ('Important dates', {'fields': ('last_login',)}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'password1', 'password2'),
        }),
    )
admin.site.register(User, UserAdmin)
admin.site.register(FriendRequest)