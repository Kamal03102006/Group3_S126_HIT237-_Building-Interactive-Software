class HousingDomainError(Exception):
    """
    Base exception for housing application workflow errors.
    These are domain errors, not system/server errors.
    """


class TenantProfileMissing(HousingDomainError):
    """
    Raised when an authenticated user does not have a linked tenant profile.
    """


class PermissionDeniedForRepair(HousingDomainError):
    """
    Raised when a user tries to access or update a repair request
    without the required permission.
    """


class InvalidRepairStatus(HousingDomainError):
    """
    Raised when an invalid status is used in the repair workflow.
    """


class RepairRequestNotFound(HousingDomainError):
    """
    Raised when a repair request cannot be found in the allowed user scope.
    """