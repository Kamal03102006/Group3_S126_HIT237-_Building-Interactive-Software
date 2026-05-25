from django.db.models import Count

from housing.models import RepairRequest


def get_repair_status_summary():
    """
    Returns number of repair requests grouped by status.
    """
    return (
        RepairRequest.objects
        .values("status")
        .annotate(total=Count("id"))
        .order_by("status")
    )


def get_repair_priority_summary():
    """
    Returns number of repair requests grouped by priority.
    """
    return (
        RepairRequest.objects
        .values("priority")
        .annotate(total=Count("id"))
        .order_by("priority")
    )


def get_community_repair_summary():
    """
    Returns number of repair requests grouped by community.
    """
    return (
        RepairRequest.objects
        .values("dwelling__community__name")
        .annotate(total=Count("id"))
        .order_by("dwelling__community__name")
    )


def get_basic_dashboard_summary():
    """
    Returns basic dashboard metrics that do not depend on tenant-user linking.
    """
    return {
        "total_repairs": RepairRequest.objects.count(),
        "open_repairs": RepairRequest.objects.exclude(
            status__in=["completed", "cancelled"]
        ).count(),
        "urgent_repairs": RepairRequest.objects.filter(
            priority="urgent"
        ).count(),
        "status_summary": get_repair_status_summary(),
        "priority_summary": get_repair_priority_summary(),
        "community_summary": get_community_repair_summary(),
    }