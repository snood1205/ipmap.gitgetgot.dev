from django.db import models

class IPInfo(models.Model):
    handle = models.CharField(max_length=255, unique=True)
    whois_server = models.CharField(max_length=255, null=True, blank=True)
    organization = models.CharField(max_length=255)
    network_type = models.CharField(max_length=255, null=True, blank=True)
    status = models.CharField(max_length=255, null=True, blank=True)
    registration_date = models.DateField(null=True, blank=True)
    updated_date = models.DateField(null=True, blank=True)
    country = models.CharField(max_length=10, null=True, blank=True)
    ref_url = models.CharField(max_length=255, null=True, blank=True)
    remarks = models.JSONField(null=True, blank=True)
    cidr_block = models.GenericIPAddressField(unique=True)

    def __str__(self):
        return f"{self.organization} ({self.handle})"