# Generated by Django 5.1.7 on 2025-03-19 00:07

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="BusinessHours",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "day",
                    models.IntegerField(
                        choices=[
                            (0, "Monday"),
                            (1, "Tuesday"),
                            (2, "Wednesday"),
                            (3, "Thursday"),
                            (4, "Friday"),
                            (5, "Saturday"),
                            (6, "Sunday"),
                        ],
                        help_text="Day of the week",
                    ),
                ),
                (
                    "start_time",
                    models.TimeField(
                        help_text="Start time for appointments on this day"
                    ),
                ),
                (
                    "end_time",
                    models.TimeField(help_text="End time for appointments on this day"),
                ),
                (
                    "is_available",
                    models.BooleanField(
                        default=True,
                        help_text="Whether appointments can be booked on this day",
                    ),
                ),
            ],
            options={
                "verbose_name": "Business Hours",
                "verbose_name_plural": "Business Hours",
                "ordering": ["day"],
            },
        ),
        migrations.CreateModel(
            name="Service",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "name",
                    models.CharField(
                        help_text="Name of the service/treatment offered",
                        max_length=200,
                    ),
                ),
                (
                    "description",
                    models.TextField(
                        help_text="Detailed description of what the service entails"
                    ),
                ),
                (
                    "duration",
                    models.IntegerField(help_text="Duration of the service in minutes"),
                ),
                (
                    "price",
                    models.DecimalField(
                        decimal_places=2,
                        help_text="Cost of the service in dollars",
                        max_digits=6,
                    ),
                ),
                (
                    "is_active",
                    models.BooleanField(
                        default=True,
                        help_text="Whether this service is currently being offered",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Client",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "first_name",
                    models.CharField(help_text="Client's first name", max_length=100),
                ),
                (
                    "last_name",
                    models.CharField(help_text="Client's last name", max_length=100),
                ),
                (
                    "email",
                    models.EmailField(
                        help_text="Email address for confirmations and notifications",
                        max_length=254,
                    ),
                ),
                (
                    "phone",
                    models.CharField(help_text="Contact phone number", max_length=20),
                ),
                (
                    "date_of_birth",
                    models.DateField(
                        help_text="Client's date of birth for health records"
                    ),
                ),
                (
                    "medical_conditions",
                    models.TextField(
                        blank=True,
                        help_text="Any relevant medical conditions or health concerns",
                    ),
                ),
                (
                    "allergies",
                    models.TextField(
                        blank=True,
                        help_text="Any allergies to herbs, medicines, or other substances",
                    ),
                ),
                (
                    "current_medications",
                    models.TextField(
                        blank=True,
                        help_text="Current medications, supplements, or herbal remedies being taken",
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(
                        auto_now_add=True,
                        help_text="When the client record was created",
                    ),
                ),
                (
                    "user",
                    models.OneToOneField(
                        help_text="Link to user account for online access",
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Booking",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("date", models.DateField(help_text="Date of the appointment")),
                ("time", models.TimeField(help_text="Time of the appointment")),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("pending", "Pending"),
                            ("confirmed", "Confirmed"),
                            ("cancelled", "Cancelled"),
                            ("completed", "Completed"),
                        ],
                        default="pending",
                        help_text="Current status of the booking",
                        max_length=20,
                    ),
                ),
                (
                    "notes",
                    models.TextField(
                        blank=True,
                        help_text="Any special requests or notes about the appointment",
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(
                        auto_now_add=True, help_text="When the booking was created"
                    ),
                ),
                (
                    "updated_at",
                    models.DateTimeField(
                        auto_now=True, help_text="When the booking was last modified"
                    ),
                ),
                (
                    "client",
                    models.ForeignKey(
                        help_text="The client who booked the appointment",
                        on_delete=django.db.models.deletion.CASCADE,
                        to="bookings.client",
                    ),
                ),
                (
                    "service",
                    models.ForeignKey(
                        help_text="The service/treatment being booked",
                        on_delete=django.db.models.deletion.CASCADE,
                        to="bookings.service",
                    ),
                ),
            ],
            options={
                "ordering": ["-date", "-time"],
            },
        ),
    ]
