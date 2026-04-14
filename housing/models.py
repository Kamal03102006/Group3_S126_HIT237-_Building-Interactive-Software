from django.db import models
from django.core.validators import MinValueValidator
from django.urls import reverse

class Community(models.Model):
    name = models.CharField(max_length=100)
    region = models.CharField(max_length=100)
    is_remote = models.BooleanField(default=True)
    notes = models.TextField(blank=True)

    def __str__(self):
        return self.name
    class Meta: 
        verbose_name_plural = "Communities"


class Dwelling(models.Model):
    CONDITION_CHOICES = [
        ("good", "Good"),
        ("fair", "Fair"),
        ("poor", "Poor"),
        ("critical", "Critical"),
    ]

    community = models.ForeignKey(
        Community,
        on_delete=models.CASCADE,
        related_name="dwellings"
    )
    house_code = models.CharField(max_length=30, unique=True)
    address = models.CharField(max_length=255)
    bedrooms = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    condition_status = models.CharField(
        max_length=20,
        choices=CONDITION_CHOICES,
        default="fair"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.house_code} - {self.address}"

    def active_repair_count(self):
        return self.repair_requests.exclude(status__in=["completed", "cancelled"]).count()

class Tenant(models.Model):
    dwelling = models.ForeignKey(
        Dwelling,
        on_delete=models.CASCADE,
        related_name="tenants"
    )
    full_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    is_primary_tenant = models.BooleanField(default=False)
    moved_in_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.full_name


class RepairRequest(models.Model):
    CATEGORY_CHOICES = [
        ("plumbing", "Plumbing"),
        ("electrical", "Electrical"),
        ("doors", "Doors"),
        ("aircon", "Air Conditioning"),
        ("roofing", "Roofing"),
        ("other", "Other"),
    ]

    PRIORITY_CHOICES = [
        ("low", "Low"),
        ("medium", "Medium"),
        ("high", "High"),
        ("urgent", "Urgent"),
    ]

    STATUS_CHOICES = [
        ("reported", "Reported"),
        ("in_progress", "In Progress"),
        ("on_hold", "On Hold"),
        ("completed", "Completed"),
        ("cancelled", "Cancelled"),
    ]

    dwelling = models.ForeignKey(
        Dwelling,
        on_delete=models.CASCADE,
        related_name="repair_requests"
    )
    tenant = models.ForeignKey(
        Tenant,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="repair_requests"
    )
    title = models.CharField(max_length=150)
    description = models.TextField()
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default="medium")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="reported")
    reported_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    class Meta:
        ordering = ["-reported_at"]

    def get_absolute_url(self):
        return reverse("repair_request_detail", kwargs={"pk": self.pk})
    
    def is_open(self):
        return self.status not in ["completed", "cancelled"]


class MaintenanceUpdate(models.Model):
    repair_request = models.ForeignKey(
        RepairRequest,
        on_delete=models.CASCADE,
        related_name="updates"
    )
    note = models.TextField()
    status_snapshot = models.CharField(
        max_length=20,
        choices=RepairRequest.STATUS_CHOICES
    )
    updated_by = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Update for {self.repair_request.title}"
    class Meta:
        ordering = ["-created_at"]