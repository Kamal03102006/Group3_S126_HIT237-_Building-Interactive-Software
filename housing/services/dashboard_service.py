from housing.services.repair_request_service import get_visible_repair_requests


def get_dashboard_summary_for_user(user):
    """
    Returns dashboard statistics based on repairs visible to the logged-in user.
    """
    queryset = get_visible_repair_requests(user)

    return {
        "total_repairs": queryset.count(),
        "open_repairs": queryset.open().count(),
        "urgent_repairs": queryset.urgent().count(),
        "completed_repairs": queryset.completed().count(),
        "in_progress_repairs": queryset.in_progress().count(),
        "status_summary": queryset.status_summary(),
        "priority_summary": queryset.priority_summary(),
        "community_summary": queryset.community_summary(),
    }