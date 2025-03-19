from django.db import models
from django.contrib.auth.models import User


class Client(models.Model):
    """
    Stores client/patient information.
    Each client needs a user account for online access.
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
        """Returns the client's full name"""
        return f"{self.first_name} {self.last_name}"
