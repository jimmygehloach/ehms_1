# Generated by Django 4.2.1 on 2023-05-23 00:45

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import model_utils.fields


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("hospitals", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("patients", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="FamilyTree",
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
                (
                    "relation",
                    models.CharField(
                        choices=[
                            ("Great Grand Father", "Great Grand Father"),
                            ("Grand Father", "Grand Father"),
                            ("Father", "Father"),
                            ("Step-Father", "Step-Father"),
                            ("Great Grand Mother", "Great Grand Mother"),
                            ("Grand Mother", "Grand Mother"),
                            ("Mother", "Mother"),
                            ("Step-Mother", "Step-Mother"),
                            ("Daughter", "Daughter"),
                            ("Son", "Son"),
                            ("Wife", "Wife"),
                            ("Husband", "Husband"),
                            ("Child", "Child"),
                            ("Brother", "Brother"),
                            ("Sister", "Sister"),
                            ("Grand Son", "Grand Son"),
                            ("Grand Daughter", "Grand Daughter"),
                            ("Step-Child", "Step-Child"),
                            ("Adopted Child", "Adopted Child"),
                            ("Mother-in-law", "Mother-in-law"),
                            ("Father-in-law", "Father-in-law"),
                            ("Daughter-in-law", "Daughter-in-law"),
                            ("Brother-in-law", "Brother-in-law"),
                            ("Sister-in-law", "Sister-in-law"),
                            ("Uncle", "Uncle"),
                            ("Aunt", "Aunt"),
                            ("Nephew", "Nephew"),
                            ("Niece", "Niece"),
                            ("Other", "Other"),
                        ],
                        max_length=100,
                        verbose_name="Select the relation",
                    ),
                ),
                (
                    "creator_user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.RESTRICT,
                        related_name="family_tree_creator_user",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Logged in user",
                    ),
                ),
                (
                    "first_patient",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.RESTRICT,
                        related_name="relation_first_patient",
                        to="patients.patient",
                        verbose_name="First Patient",
                    ),
                ),
                (
                    "hospital",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.RESTRICT,
                        related_name="relation_hospital",
                        to="hospitals.hospital",
                        verbose_name="Hospital",
                    ),
                ),
                (
                    "second_patient",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.RESTRICT,
                        related_name="relation_second_patient",
                        to="patients.patient",
                        verbose_name="Second Patient",
                    ),
                ),
            ],
            options={
                "verbose_name": "Family Tree",
                "verbose_name_plural": "Family Tree",
            },
        ),
    ]
