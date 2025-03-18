from django.contrib import admin
from .models import Service, Client, Booking, Testimonial


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ("name", "duration", "price", "is_active")
    list_filter = ("is_active",)
    search_fields = ("name", "description")


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ("first_name", "last_name", "email", "phone", "created_at")
    list_filter = ("created_at",)
    search_fields = ("first_name", "last_name", "email", "phone")


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ("client", "service", "date", "time", "status")
    list_filter = ("status", "date", "service")
    search_fields = ("client__first_name", "client__last_name", "service__name")
    date_hierarchy = "date"


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ("client", "rating", "created_at", "is_approved")
    list_filter = ("rating", "is_approved", "created_at")
    search_fields = ("client__first_name", "client__last_name", "content")
