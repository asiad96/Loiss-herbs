# Generated by Django 5.1.7 on 2025-03-19 00:51

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0001_initial"),
        ("bookings", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="booking",
            name="client",
            field=models.ForeignKey(
                help_text="The client who booked the appointment",
                on_delete=django.db.models.deletion.CASCADE,
                to="accounts.client",
            ),
        ),
        migrations.AddField(
            model_name="booking",
            name="created_by_admin",
            field=models.BooleanField(
                default=False,
                help_text="Whether this booking was created by an admin (backup flow)",
            ),
        ),
        migrations.DeleteModel(
            name="Client",
        ),
    ]
