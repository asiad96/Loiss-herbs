from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.utils import timezone


class Service(models.Model):
    """
    Represents a service/treatment offered by the herbalist.
    Used to define what services clients can book appointments for.
    """

    name = models.CharField(
        max_length=200, help_text="Name of the service/treatment offered"
    )
    description = models.TextField(
        help_text="Detailed description of what the service entails"
    )
    duration = models.IntegerField(help_text="Duration of the service in minutes")
    price = models.DecimalField(
        max_digits=6, decimal_places=2, help_text="Cost of the service in dollars"
    )
    is_active = models.BooleanField(
        default=True, help_text="Whether this service is currently being offered"
    )

    def __str__(self):
        """Returns the service name when the object is printed"""
        return self.name


class Client(models.Model):
    """
    Stores client/patient information.
    Each client needs a user account for online booking and management.
    Includes contact info and important medical information.
    """

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        help_text="Link to user account for online access",
    )
    first_name = models.CharField(max_length=100, help_text="Client's first name")
    last_name = models.CharField(max_length=100, help_text="Client's last name")
    email = models.EmailField(
        help_text="Email address for confirmations and notifications"
    )
    phone = models.CharField(max_length=20, help_text="Contact phone number")
    date_of_birth = models.DateField(
        help_text="Client's date of birth for health records"
    )
    medical_conditions = models.TextField(
        blank=True, help_text="Any relevant medical conditions or health concerns"
    )
    allergies = models.TextField(
        blank=True, help_text="Any allergies to herbs, medicines, or other substances"
    )
    current_medications = models.TextField(
        blank=True,
        help_text="Current medications, supplements, or herbal remedies being taken",
    )
    created_at = models.DateTimeField(
        auto_now_add=True, help_text="When the client record was created"
    )

    def __str__(self):
        """Returns the client's full name when the object is printed"""
        return f"{self.first_name} {self.last_name}"


class Booking(models.Model):
    """
    Represents an appointment booking.
    Links a client with a specific service at a specific time.
    Includes status tracking and notes about the appointment.
    """

    BOOKING_STATUS = [
        ("pending", "Pending"),  # Just created, needs confirmation
        ("confirmed", "Confirmed"),  # Confirmed by staff/system
        ("cancelled", "Cancelled"),  # Cancelled by either party
        ("completed", "Completed"),  # Service has been provided
    ]

    client = models.ForeignKey(
        Client,
        on_delete=models.CASCADE,
        help_text="The client who booked the appointment",
    )
    service = models.ForeignKey(
        Service,
        on_delete=models.CASCADE,
        help_text="The service/treatment being booked",
    )
    date = models.DateField(help_text="Date of the appointment")
    time = models.TimeField(help_text="Time of the appointment")
    status = models.CharField(
        max_length=20,
        choices=BOOKING_STATUS,
        default="pending",
        help_text="Current status of the booking",
    )
    notes = models.TextField(
        blank=True, help_text="Any special requests or notes about the appointment"
    )
    created_at = models.DateTimeField(
        auto_now_add=True, help_text="When the booking was created"
    )
    updated_at = models.DateTimeField(
        auto_now=True, help_text="When the booking was last modified"
    )

    class Meta:
        """
        Orders bookings by date and time (newest first)
        """

        ordering = ["-date", "-time"]

    def __str__(self):
        """Returns a summary of the booking when the object is printed"""
        return f"{self.client} - {self.service} on {self.date} at {self.time}"
