from django.db.models import Count

from housing.services.repair_request_service import get_visible_repair_requests


def get_dashboard_summary_for_user(user):
    """
    Returns dashboard statistics based on the repairs visible to the user.
    """
    queryset = get_visible_repair_requests(user)

    return {
        "total_repairs": queryset.count(),
        "open_repairs": queryset.exclude(
            status__in=["completed", "cancelled"]
        ).count(),
        "urgent_repairs": queryset.filter(priority="urgent").count(),
        "status_summary": queryset.values("status")
        .annotate(total=Count("id"))
        .order_by("status"),
        "priority_summary": queryset.values("priority")
        .annotate(total=Count("id"))
        .order_by("priority"),
        "community_summary": queryset.values("dwelling__community__name")
        .annotate(total=Count("id"))
        .order_by("dwelling__community__name"),
    }