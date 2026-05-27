from django.db import transaction

from housing.exceptions import InvalidRepairStatus, PermissionDeniedForRepair
from housing.models import MaintenanceUpdate, RepairRequest
from housing.services.permission_service import user_can_update_repair


@transaction.atomic
def add_maintenance_update(user, repair_request, note, status_snapshot):
    """
    Adds a maintenance update and records who updated it.
    """
    if not user_can_update_repair(user):
        raise PermissionDeniedForRepair(
            "Only maintenance staff or housing managers can add maintenance updates."
        )

    valid_statuses = [choice[0] for choice in RepairRequest.STATUS_CHOICES]

    if status_snapshot not in valid_statuses:
        raise InvalidRepairStatus("Invalid repair status selected.")

    repair_request.status = status_snapshot
    repair_request.save(update_fields=["status", "updated_at"])

    return MaintenanceUpdate.objects.create(
        repair_request=repair_request,
        note=note,
        status_snapshot=status_snapshot,
        updated_by=user.get_full_name() or user.username,
    )


def get_recent_maintenance_updates(limit=5):
    """
    Returns recent maintenance updates for dashboard or detail display.
    """
    return MaintenanceUpdate.objects.select_related(
        "repair_request",
        "repair_request__dwelling",
        "repair_request__dwelling__community",
    ).order_by("-created_at")[:limit]