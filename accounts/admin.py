from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth import get_user_model

User = get_user_model()
# Register your models here.

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = (
        'email',
        'first_name',
        'last_name',
        'is_active',
        'is_staff',
        'created',
        'updated',
    )
    readonly_fields = ('last_login', 'created', 'updated')

    search_fields = ('email', 'first_name', 'last_name')

    ordering = ('email',)

    fieldsets = (
        ("Login Credentials", {
            "fields": ("email", "password")
        }),
        ("Personal Info", {
            "fields": ("first_name", "last_name", "mobile_phone", "mobile_notification")
        }),
        ("Status", {
            "fields": ("is_active", "is_staff", "is_superuser", "deleted_at")
        }),
        ("Timestamps", {
            "fields": ("last_login", "last_password_reset", "created", "updated")
        }),
        ("Permissions", {
            "fields": ("groups", "user_permissions")
        }),
    )
