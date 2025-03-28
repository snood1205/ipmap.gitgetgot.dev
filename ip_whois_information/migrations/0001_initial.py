# Generated by Django 5.1.7 on 2025-03-18 19:01

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="IPInfo",
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
                ("handle", models.CharField(max_length=255, unique=True)),
                (
                    "whois_server",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                ("organization", models.CharField(max_length=255)),
                (
                    "network_type",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                ("status", models.CharField(blank=True, max_length=255, null=True)),
                ("registration_date", models.DateField(blank=True, null=True)),
                ("updated_date", models.DateField(blank=True, null=True)),
                ("country", models.CharField(blank=True, max_length=10, null=True)),
                ("ref_url", models.CharField(blank=True, max_length=255, null=True)),
                ("remarks", models.JSONField(blank=True, null=True)),
                ("address_information", models.JSONField(blank=True, null=True)),
                ("cidr_block", models.GenericIPAddressField(unique=True)),
            ],
        ),
    ]
