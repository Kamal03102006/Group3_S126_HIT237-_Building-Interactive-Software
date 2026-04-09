from django.contrib import admin
from .models import Community, Dwelling, Tenant, RepairRequest, MaintenanceUpdate


@admin.register(Community)
class CommunityAdmin(admin.ModelAdmin):
    list_display = ("name", "region", "is_remote")
    search_fields = ("name", "region")


@admin.register(Dwelling)
class DwellingAdmin(admin.ModelAdmin):
    list_display = ("house_code", "address", "community", "bedrooms", "condition_status")
    list_filter = ("condition_status", "community")
    search_fields = ("house_code", "address")


@admin.register(Tenant)
class TenantAdmin(admin.ModelAdmin):
    list_display = ("full_name", "dwelling", "is_primary_tenant", "phone")
    list_filter = ("is_primary_tenant",)
    search_fields = ("full_name", "phone", "email")


@admin.register(RepairRequest)
class RepairRequestAdmin(admin.ModelAdmin):
    list_display = ("title", "dwelling", "tenant", "category", "priority", "status", "reported_at")
    list_filter = ("status", "priority", "category")
    search_fields = ("title", "description")


@admin.register(MaintenanceUpdate)
class MaintenanceUpdateAdmin(admin.ModelAdmin):
    list_display = ("repair_request", "status_snapshot", "updated_by", "created_at")
    list_filter = ("status_snapshot",)
    search_fields = ("updated_by", "note")