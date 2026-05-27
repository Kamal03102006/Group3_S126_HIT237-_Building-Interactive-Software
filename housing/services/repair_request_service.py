from django.db import transaction
from django.shortcuts import get_object_or_404

from housing.exceptions import (
    HousingDomainError,
    InvalidRepairStatus,
    PermissionDeniedForRepair,
    TenantProfileMissing,
)
from housing.models import RepairRequest, MaintenanceUpdate
from housing.services.permission_service import (
    user_can_update_repair,
    user_is_staff_or_manager,
    user_is_tenant,
)


def get_visible_repair_requests(user):
    """
    Returns repair requests visible to the logged-in user.
    Staff/managers see all repairs.
    Tenants only see their own repairs.
    """
    queryset = RepairRequest.objects.select_related(
        "dwelling",
        "tenant",
        "dwelling__community",
    )

    if user_is_staff_or_manager(user):
        return queryset

    if user_is_tenant(user):
        return queryset.filter(tenant=user.tenant_profile)

    return RepairRequest.objects.none()


def get_filtered_repair_requests(user, status=None, priority=None):
    """
    Applies status and priority filters to the repairs visible to the user.
    """
    queryset = get_visible_repair_requests(user)

    if status:
        queryset = queryset.filter(status=status)

    if priority:
        queryset = queryset.filter(priority=priority)

    return queryset.order_by("-reported_at")


def get_repair_for_user(user, pk):
    """
    Retrieves one repair request only if the user is allowed to see it.
    """
    queryset = get_visible_repair_requests(user).prefetch_related("updates")
    return get_object_or_404(queryset, pk=pk)


@transaction.atomic
def create_repair_request_for_user(user, form):
    """
    Creates a repair request for the logged-in tenant.
    The tenant and dwelling are assigned from the tenant profile.
    """
    if not user_is_tenant(user):
        raise TenantProfileMissing(
            "Only users with a linked tenant profile can create repair requests."
        )

    repair_request = form.save(commit=False)
    repair_request.tenant = user.tenant_profile
    repair_request.dwelling = user.tenant_profile.dwelling
    repair_request.status = "reported"
    repair_request.save()

    MaintenanceUpdate.objects.create(
        repair_request=repair_request,
        note="Repair request submitted.",
        status_snapshot=repair_request.status,
        updated_by=user.get_full_name() or user.username,
    )

    return repair_request


@transaction.atomic
def update_repair_status(user, repair_request, new_status, note=""):
    """
    Updates a repair status and records a maintenance update.
    Only staff/managers can do this.
    """
    if not user_can_update_repair(user):
        raise PermissionDeniedForRepair(
            "Only maintenance staff or housing managers can update repair requests."
        )

    valid_statuses = [choice[0] for choice in RepairRequest.STATUS_CHOICES]

    if new_status not in valid_statuses:
        raise InvalidRepairStatus("Invalid repair status selected.")

    repair_request.status = new_status
    repair_request.save(update_fields=["status", "updated_at"])

    MaintenanceUpdate.objects.create(
        repair_request=repair_request,
        note=note or f"Status changed to {new_status}.",
        status_snapshot=new_status,
        updated_by=user.get_full_name() or user.username,
    )

    return repair_request