from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import Client


class ClientInline(admin.StackedInline):
    model = Client
    can_delete = False
    verbose_name_plural = "Client Information"


class CustomUserAdmin(UserAdmin):
    inlines = (ClientInline,)
    list_display = ("username", "email", "first_name", "last_name", "is_staff")
    list_filter = ("is_staff", "is_superuser", "is_active")


# Unregister the default User admin and register our custom one
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
