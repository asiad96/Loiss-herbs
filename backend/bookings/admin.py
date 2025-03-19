from django.contrib import admin
from .models import Service, Booking, BusinessHours


@admin.register(BusinessHours)
class BusinessHoursAdmin(admin.ModelAdmin):
    list_display = ("get_day_display", "start_time", "end_time", "is_available")
    list_filter = ("is_available", "day")
    ordering = ["day"]


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ("name", "duration", "price", "is_active")
    list_filter = ("is_active",)
    search_fields = ("name", "description")


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ("client", "service", "date", "time", "status", "created_by_admin")
    list_filter = ("status", "date", "service", "created_by_admin")
    search_fields = ("client__first_name", "client__last_name", "service__name")
    date_hierarchy = "date"

    def save_model(self, request, obj, form, change):
        """Set created_by_admin when booking is created in admin"""
        if not change:  # Only for new bookings
            obj.created_by_admin = True
        super().save_model(request, obj, form, change)
