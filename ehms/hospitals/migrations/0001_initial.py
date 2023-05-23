# Generated by Django 4.2.1 on 2023-05-23 00:45

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import ehms.hospitals.models
import model_utils.fields


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("addresses", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Hospital",
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
                    "status",
                    model_utils.fields.StatusField(
                        choices=[("active", "active"), ("inactive", "inactive")],
                        default="active",
                        max_length=100,
                        no_check_for_status=True,
                        verbose_name="status",
                    ),
                ),
                (
                    "status_changed",
                    model_utils.fields.MonitorField(
                        default=django.utils.timezone.now, monitor="status", verbose_name="status changed"
                    ),
                ),
                ("uid", models.CharField(blank=True, max_length=255, unique=True, verbose_name="UID")),
                ("name", models.CharField(max_length=200, unique=True, verbose_name="Name")),
                ("email", models.EmailField(blank=True, max_length=100, verbose_name="Email")),
                ("phone", models.CharField(max_length=15, verbose_name="Phone")),
                ("alternate_phone", models.CharField(blank=True, max_length=15, verbose_name="Alternate phone")),
                ("address_line_1", models.CharField(max_length=200, verbose_name="Address Line 1")),
                ("address_line_2", models.CharField(blank=True, max_length=200, verbose_name="Address Line 2")),
                ("longitude", models.CharField(blank=True, max_length=200, verbose_name="Longitude")),
                ("latitude", models.CharField(blank=True, max_length=200, verbose_name="Latitude")),
                ("beds", models.PositiveIntegerField(default=0, verbose_name="Beds")),
                (
                    "image",
                    models.ImageField(
                        blank=True,
                        null=True,
                        upload_to=ehms.hospitals.models.hospital_image_upload,
                        verbose_name="Hospital Image",
                    ),
                ),
                ("remarks", models.TextField(blank=True, verbose_name="Remarks")),
                (
                    "country",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.RESTRICT,
                        related_name="hospital_country",
                        to="addresses.country",
                        verbose_name="Country",
                    ),
                ),
                (
                    "creator_user",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.RESTRICT,
                        related_name="hospital_creator_user",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Logged in user",
                    ),
                ),
                (
                    "district",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.RESTRICT,
                        related_name="hospital_district",
                        to="addresses.district",
                        verbose_name="District",
                    ),
                ),
                (
                    "postcode",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.RESTRICT,
                        related_name="hospital_postcode",
                        to="addresses.postcode",
                        verbose_name="PostalCode",
                    ),
                ),
                (
                    "region",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.RESTRICT,
                        related_name="hospital_region",
                        to="addresses.region",
                        verbose_name="Region",
                    ),
                ),
                (
                    "town",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.RESTRICT,
                        related_name="hospital_town",
                        to="addresses.town",
                        verbose_name="Town",
                    ),
                ),
            ],
            options={
                "verbose_name": "Hospital",
                "verbose_name_plural": "Hospitals",
            },
        ),
        migrations.CreateModel(
            name="HospitalRepresentative",
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
                    "status",
                    model_utils.fields.StatusField(
                        choices=[("active", "active"), ("inactive", "inactive")],
                        default="active",
                        max_length=100,
                        no_check_for_status=True,
                        verbose_name="status",
                    ),
                ),
                (
                    "status_changed",
                    model_utils.fields.MonitorField(
                        default=django.utils.timezone.now, monitor="status", verbose_name="status changed"
                    ),
                ),
                ("first_name", models.CharField(max_length=200, verbose_name="First name")),
                ("last_name", models.CharField(blank=True, max_length=200, verbose_name="Last name")),
                (
                    "gender",
                    models.CharField(
                        blank=True,
                        choices=[("Male", "Male"), ("Female", "Female")],
                        max_length=6,
                        verbose_name="Gender",
                    ),
                ),
                ("date_of_birth", models.DateField(blank=True, null=True, verbose_name="Date of Birth")),
                ("phone", models.CharField(max_length=15, verbose_name="Phone number")),
                ("alternate_phone", models.CharField(blank=True, max_length=15, verbose_name="Alternate phone")),
                ("email", models.EmailField(blank=True, max_length=100, verbose_name="Email")),
                ("designation", models.CharField(blank=True, max_length=200, verbose_name="Designation")),
                (
                    "image",
                    models.ImageField(
                        blank=True,
                        null=True,
                        upload_to=ehms.hospitals.models.hospital_rep_image_upload,
                        verbose_name="Representative Image",
                    ),
                ),
                ("remarks", models.TextField(blank=True, verbose_name="Remarks")),
                (
                    "creator_user",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.RESTRICT,
                        related_name="hospital_rep_creator_user",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Logged in user",
                    ),
                ),
                (
                    "hospital",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.RESTRICT,
                        related_name="hospital_rep_hospital",
                        to="hospitals.hospital",
                        verbose_name="Hospital",
                    ),
                ),
            ],
            options={
                "verbose_name": "Representative",
                "verbose_name_plural": "Representatives",
            },
        ),
    ]
