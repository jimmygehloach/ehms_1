# Generated by Django 4.2.1 on 2023-05-23 00:45

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import model_utils.fields


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("addresses", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="UserProfile",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                (
                    "created",
                    model_utils.fields.AutoCreatedField(
                        default=django.utils.timezone.now, editable=False, verbose_name="created"
                    ),
                ),
                (
                    "modified",
                    model_utils.fields.AutoLastModifiedField(
                        default=django.utils.timezone.now, editable=False, verbose_name="modified"
                    ),
                ),
                (
                    "status_changed",
                    model_utils.fields.MonitorField(
                        default=django.utils.timezone.now, monitor="status", verbose_name="status changed"
                    ),
                ),
                (
                    "status",
                    models.CharField(
                        choices=[("active", "active"), ("inactive", "inactive")], default="active", max_length=20
                    ),
                ),
                (
                    "gender",
                    models.CharField(
                        blank=True,
                        choices=[("Male", "Male"), ("Female", "Female"), ("Other", "Other")],
                        max_length=6,
                        verbose_name="Gender",
                    ),
                ),
                ("date_of_birth", models.DateField(blank=True, null=True, verbose_name="Date of Birth")),
                ("bio", models.TextField(blank=True, verbose_name="Bio")),
                ("designation", models.CharField(blank=True, max_length=100, verbose_name="Designation")),
                (
                    "address_line_1",
                    models.CharField(
                        blank=True,
                        help_text="e.g. Flat No or House No ...",
                        max_length=100,
                        verbose_name="Address Line 1",
                    ),
                ),
                (
                    "address_line_2",
                    models.CharField(
                        blank=True,
                        help_text="Extra information related to address e.g. landmark ...",
                        max_length=200,
                        verbose_name="Address Line 2",
                    ),
                ),
                ("phone", models.CharField(blank=True, max_length=10, verbose_name="Phone")),
                ("alternate_phone", models.CharField(blank=True, max_length=10, verbose_name="Alternative Phone")),
                (
                    "type_of_address",
                    models.CharField(
                        blank=True,
                        choices=[("Temporary", "Temporary"), ("Permanent", "Permanent")],
                        max_length=10,
                        verbose_name="Type of address",
                    ),
                ),
                ("remarks", models.TextField(blank=True, max_length=5000, verbose_name="Remarks")),
                ("user_unique_id", models.CharField(blank=True, max_length=20)),
                (
                    "country",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.RESTRICT,
                        related_name="users_country",
                        to="addresses.country",
                        verbose_name="Country",
                    ),
                ),
                (
                    "user",
                    models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
    ]
