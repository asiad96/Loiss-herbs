from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError
from django.utils import timezone
from datetime import datetime, timedelta
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string


class BusinessHours(models.Model):
    """
    Stores the herbalist's available hours for each day of the week.
    Allows for flexible scheduling.
    """

    DAYS_OF_WEEK = [
        (0, "Monday"),
        (1, "Tuesday"),
        (2, "Wednesday"),
        (3, "Thursday"),
        (4, "Friday"),
        (5, "Saturday"),
        (6, "Sunday"),
    ]

    day = models.IntegerField(choices=DAYS_OF_WEEK, help_text="Day of the week")
    start_time = models.TimeField(help_text="Start time for appointments on this day")
    end_time = models.TimeField(help_text="End time for appointments on this day")
    is_available = models.BooleanField(
        default=True, help_text="Whether appointments can be booked on this day"
    )

    class Meta:
        ordering = ["day"]
        verbose_name = "Business Hours"
        verbose_name_plural = "Business Hours"

    def __str__(self):
        return f"{self.get_day_display()}: {self.start_time} - {self.end_time}"

    @classmethod
    def is_time_available(cls, date, time):
        """Check if a given time is within business hours"""
        day_of_week = date.weekday()
        try:
            hours = cls.objects.get(day=day_of_week, is_available=True)
            return hours.start_time <= time <= hours.end_time
        except cls.DoesNotExist:
            return False


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

    def clean(self):
        """
        Validate the booking:
        1. Check if date is not in the past
        2. Check if time is within business hours
        3. Check for double bookings
        4. Ensure booking end time doesn't overlap with next booking
        """
        if not self.date or not self.time:
            return

        # Check if booking is in the past
        booking_datetime = datetime.combine(self.date, self.time)
        if booking_datetime < timezone.now():
            raise ValidationError("Cannot book appointments in the past")

        # Check if within business hours
        if not BusinessHours.is_time_available(self.date, self.time):
            raise ValidationError("This time is outside of available business hours")

        # Calculate booking end time
        duration = timedelta(minutes=self.service.duration)
        booking_end = (datetime.combine(self.date, self.time) + duration).time()

        # Also check if end time is within business hours
        if not BusinessHours.is_time_available(self.date, booking_end):
            raise ValidationError("The appointment would end outside business hours")

        # Check for overlapping bookings
        overlapping = Booking.objects.filter(
            date=self.date, status__in=["pending", "confirmed"]
        ).exclude(id=self.id)

        for booking in overlapping:
            other_start = booking.time
            other_end = (
                datetime.combine(booking.date, booking.time)
                + timedelta(minutes=booking.service.duration)
            ).time()

            if (
                (self.time <= other_start < booking_end)
                or (self.time < other_end <= booking_end)
                or (other_start <= self.time < other_end)
            ):
                raise ValidationError("This time slot overlaps with another booking")

    def save(self, *args, **kwargs):
        """Validate and handle notifications when saving"""
        is_new = not self.pk  # Check if this is a new booking
        old_status = None

        # If existing booking, get old status
        if not is_new:
            old_status = Booking.objects.get(pk=self.pk).status

        self.clean()
        super().save(*args, **kwargs)

        # Send notifications based on status changes
        if is_new:
            self.notify_new_booking()
        elif old_status != self.status:
            self.notify_status_change(old_status)

    def notify_new_booking(self):
        """Send notification for new booking request"""
        subject = "New Booking Request"
        message = render_to_string(
            "bookings/email/new_booking.txt",
            {
                "booking": self,
                "admin_url": f"/admin/bookings/booking/{self.pk}/change/",
            },
        )
        self._send_email_to_herbalist(subject, message)
        self._send_email_to_client(
            "Booking Request Received",
            "Thank you for your booking request. We will confirm your appointment soon.",
        )

    def notify_status_change(self, old_status):
        """Send notification when booking status changes"""
        subject = f"Booking Status Changed: {old_status} → {self.status}"
        message = f"Your booking for {self.service.name} on {self.date} at {self.time} has been {self.status}."
        self._send_email_to_client(subject, message)

    def _send_email_to_herbalist(self, subject, message):
        """Helper method to send email to the herbalist"""
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [settings.HERBALIST_EMAIL],
            fail_silently=True,
        )

    def _send_email_to_client(self, subject, message):
        """Helper method to send email to the client"""
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [self.client.email],
            fail_silently=True,
        )

    def __str__(self):
        """Returns a summary of the booking when the object is printed"""
        return f"{self.client} - {self.service} on {self.date} at {self.time}"
