# Architectural Decision Record 10: Add Domain Exceptions for Repair Workflow Errors

## Date
17/05/2026

## Status
Proposed and partially implemented – exception classes added; service/view integration planned.

## Related Previous ADRs
- Assessment 2 ADR on ModelForms and validation
- Assessment 2 ADR on Class-Based Views
- Assessment 2 ADR on QuerySets and repair request workflows

---

## Context

In Assessment 2, the Remote Housing Crisis project used Django models, forms and Class-Based Views to manage repair requests. This was suitable for the earlier version of the application because the workflow was mainly focused on creating, listing and updating repair request records.

For Assessment 4, the same project is being extended with authentication, service-layer architecture, permission boundaries, exception handling and testing. These new requirements introduce more complex workflow situations, such as restricted access, invalid status changes and missing tenant-user relationships.

To prepare for this growth, the project needs a clearer way to represent domain-specific workflow errors.

---

## Assessment 2 Limitation

In Assessment 2, the project mostly relied on Django’s default validation and standard view behaviour.

This meant:
- there was no custom exception structure for housing workflow errors
- permission-related errors were not clearly represented
- repair workflow errors were not separated from general form validation
- future service-layer testing would be harder without specific exception classes

This was acceptable for Assessment 2, but it is not strong enough for the Assessment 4 requirements.

---

## Alternatives Considered

### Option 1: Continue using only Django default validation

This would require fewer changes. However, it would not clearly describe business-rule errors such as an unauthorised user trying to update a repair request.

### Option 2: Use generic try/except blocks inside views

This would allow errors to be caught, but the handling could become inconsistent across different views. It would also keep too much workflow logic inside the view layer.

### Option 3: Create domain-specific exception classes

This gives the project a clear and reusable structure for workflow errors. It also prepares the application for later service-layer integration and meaningful testing.

---

## Decision

The project will introduce a dedicated exception module:

`housing/exceptions.py`

The following exception classes have been added:

- `HousingDomainError`
- `TenantProfileMissing`
- `PermissionDeniedForRepair`
- `InvalidRepairStatus`
- `RepairRequestNotFound`

These exceptions represent business-rule and workflow errors in the housing repair system.

At this stage, the exception classes have been created first. Their integration into the service layer, views and tests is planned for the next development step.

---

## Code References

Implemented:
- `housing/exceptions.py`

Planned integration:
- `housing/services/repair_request_service.py`
- `housing/views.py`
- `housing/tests/test_services.py`
- `housing/tests/test_permissions.py`

---

## Consequences

### Positive

- The project now has a clear foundation for workflow error handling.
- Future service functions can raise meaningful domain-specific errors.
- Tests can later check specific exception behaviour.
- The design supports stronger architectural separation for Assessment 4.

### Negative

- The exception classes are not fully useful until integrated with services and views.
- Team members must use the same exception structure consistently.
- Additional tests will be needed once the service layer is connected.

---

## Testing Implications

Future tests should verify that:
- invalid repair statuses raise `InvalidRepairStatus`
- unauthorised repair updates raise `PermissionDeniedForRepair`
- users without tenant profiles raise `TenantProfileMissing`
- views handle service exceptions without causing unhandled server errors

These tests are planned for the testing stage after the service layer and authentication workflow are integrated.

---

## Assessment 4 Reflection

This decision extends the Assessment 2 architecture rather than replacing it.

Assessment 2 focused on basic Django model, form and view functionality. Assessment 4 requires a more mature architecture with authentication, permissions, service-layer logic and testable workflow behaviour.

Adding domain exceptions now creates a foundation for the next stage of development, where repair workflow rules will be moved into services and tested more directly.