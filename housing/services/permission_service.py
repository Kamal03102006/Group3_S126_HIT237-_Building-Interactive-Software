def user_is_staff_or_manager(user):
    """
    Staff, Housing Managers and Django staff users can manage repairs.
    """
    if not user or not user.is_authenticated:
        return False

    return user.is_staff or user.groups.filter(
        name__in=["Maintenance Staff", "Housing Manager"]
    ).exists()


def user_is_tenant(user):
    """
    Tenant users have a linked tenant profile.
    """
    return bool(
        user
        and user.is_authenticated
        and hasattr(user, "tenant_profile")
    )


def user_can_update_repair(user):
    """
    Only staff or housing managers can update repair requests.
    """
    return user_is_staff_or_manager(user)


def user_can_view_repair(user, repair_request):
    """
    Object-level permission:
    - staff/managers can view all
    - tenants can only view their own repairs
    """
    if user_is_staff_or_manager(user):
        return True

    if user_is_tenant(user):
        return repair_request.tenant == user.tenant_profile

    return False