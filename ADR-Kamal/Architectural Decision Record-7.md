# Architectural Decision Record 07: Add Domain Exceptions for Repair Workflow Errors

## Date
17/05/2026

## Status
Partially implemented – exception classes integrated with service-layer workflows and authenticated repair handling; final testing pending.

## Related Previous ADRs
- Assessment 2 ADR on ModelForms and validation
- Assessment 2 ADR on Class-Based Views
- Assessment 2 ADR on QuerySets and repair request workflows


## Context

In Assessment 2, the Remote Housing Crisis project used Django models, forms and Class-Based Views to manage repair requests. This was suitable for the earlier version of the application because the workflow was mainly focused on creating, listing and updating repair request records.

For Assessment 4, the same project is being extended with authentication, service-layer architecture, permission boundaries, exception handling and testing. These new requirements introduce more complex workflow situations, such as restricted access, invalid status changes and missing tenant-user relationships.

To support this growth, the project required a clearer way to represent domain-specific workflow errors.


## Assessment 2 Limitation

In Assessment 2, the project mostly relied on Django’s default validation and standard view behaviour.

This meant:
- there was no custom exception structure for housing workflow errors
- permission-related errors were not clearly represented
- repair workflow errors were not separated from general form validation
- future service-layer testing would be harder without specific exception classes

This was acceptable for Assessment 2, but it is not strong enough for the Assessment 4 requirements.


## Alternatives Considered

### Option 1: Continue using only Django default validation

This would require fewer changes. However, it would not clearly describe business-rule errors such as an unauthorised user trying to update a repair request.

### Option 2: Use generic try/except blocks inside views

This would allow errors to be caught, but the handling could become inconsistent across different views. It would also keep too much workflow logic inside the view layer.

### Option 3: Create domain-specific exception classes

This gives the project a clear and reusable structure for workflow errors. It also prepares the application for service-layer integration and meaningful testing.


## Decision

The project introduced a dedicated exception module:

`housing/exceptions.py`

The following exception classes were implemented:
- `HousingDomainError`
- `TenantProfileMissing`
- `PermissionDeniedForRepair`
- `InvalidRepairStatus`
- `RepairRequestNotFound`

These exceptions represent business-rule and workflow errors in the housing repair system.

The exception classes are now integrated with service-layer workflow functions and authenticated repair handling. Service functions raise domain-specific exceptions when invalid repair statuses, missing tenant profiles or permission violations occur. Views catch these exceptions and return user-facing feedback through Django messages.

## Code References

Implemented:
- `housing/exceptions.py`
- `housing/services/repair_request_service.py`
- `housing/views.py`

Planned testing:
- `housing/tests/test_services.py`
- `housing/tests/test_permissions.py`


## Consequences

### Positive

- The project now has a clear foundation for workflow error handling.
- Future service functions can raise meaningful domain-specific errors.
- Workflow errors are now separated from generic form validation.
- Service-layer functions can now raise domain-specific exceptions consistently.
- Tests can check specific exception behaviour.
- The design supports stronger architectural separation for Assessment 4.

### Negative

- Team members must use the same exception structure consistently.
- Additional tests are required to verify exception handling behaviour.
- Some exceptions depend on authentication-aware workflows being configured correctly.


## Testing Implications

Future tests should verify that:
- invalid repair statuses raise `InvalidRepairStatus`
- unauthorised repair updates raise `PermissionDeniedForRepair`
- users without tenant profiles raise `TenantProfileMissing`
- views handle service exceptions without causing unhandled server errors


## Assessment 4 Reflection

This decision extends the Assessment 2 architecture rather than replacing it.

Assessment 2 focused on basic Django model, form and view functionality. Assessment 4 requires a more mature architecture with authentication, permissions, service-layer logic and testable workflow behaviour.

Adding domain exceptions improved the separation between workflow logic and presentation logic while preparing the application for more meaningful automated testing.