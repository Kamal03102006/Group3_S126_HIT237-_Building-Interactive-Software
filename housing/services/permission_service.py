def user_is_staff_or_manager(user):
    """
    Returns True if the user can manage repair requests.
    This includes Django staff users and users in Maintenance Staff
    or Housing Manager groups.
    """
    if not user or not user.is_authenticated:
        return False

    return user.is_staff or user.groups.filter(
        name__in=["Maintenance Staff", "Housing Manager"]
    ).exists()


def user_can_update_repair(user):
    """
    Only staff or housing managers can update repair requests.
    """
    return user_is_staff_or_manager(user)