# Architectural Decision Record 08: Introduce Service Layer for Repair Workflow Logic

## Date
25/05/2026

## Status
Partially implemented – service layer integrated with authentication-aware repair workflows; final demo-user testing pending.

## Related Previous ADRs
- Assessment 2 ADR on Django MVT structure
- Assessment 2 ADR on Class-Based Views and QuerySets
- Assessment 2 ADR on ModelForms and repair request workflows


## Context

In Assessment 2, the Remote Housing Crisis application used Django models, ModelForms, Class-Based Views and URL routing to manage housing repair requests. This structure worked for the first version because the workflow was relatively simple.

Assessment 4 requires the same application to grow by adding authentication, role-based permissions, exception handling, testing and more mature workflows. If this logic remains mostly inside views, the views will become harder to maintain and harder to test.

The Assessment 2 feedback also recommended stronger architectural traceability and deeper justification of design decisions. For this reason, the group decided to prepare a service-layer structure before fully integrating new workflows into the existing views.


## Assessment 2 Limitation

In Assessment 2, views handled most workflow responsibilities directly, including:
- retrieving repair requests
- filtering by status and priority
- handling form submission
- preparing context data

This was acceptable for the previous assessment, but it does not scale well when authentication, permissions and dashboard summaries are introduced.

The main limitation was that business logic was too closely connected to the view layer.


## Alternatives Considered

### Option 1: Keep workflow logic inside Class-Based Views

This would be faster and require fewer files. However, it would make the views harder to read, harder to test and more likely to duplicate permission logic across multiple views.

### Option 2: Move workflow logic into model methods

This would keep some logic close to the data model. However, the repair request workflow now involves users, permissions, form handling and maintenance updates, so putting all of this into models would make the models too responsible.

### Option 3: Introduce a service layer

This separates business workflow logic from views and models. Views remain responsible for HTTP request and response handling, while services manage workflow operations and reusable query helpers.


## Decision

The project introduced a service layer inside the housing app.

The implemented service structure includes:
- `housing/services/__init__.py`
- `housing/services/permission_service.py`
- `housing/services/dashboard_service.py`
- `housing/services/repair_request_service.py`

The repair workflow service has now been integrated with authentication-aware workflows. Tenant users access repair requests through service-layer filtering based on their linked tenant profile, while Maintenance Staff and Housing Manager users access broader repair workflows through role-based permissions.

Workflow-specific forms were also introduced:
- tenant repair creation form
- staff repair update form

This prevents tenants from manually selecting workflow-controlled fields such as tenant ownership, dwelling and repair status.


## Code References

Implemented:
- `housing/services/__init__.py`
- `housing/services/permission_service.py`
- `housing/services/dashboard_service.py`
- `housing/services/repair_request_service.py`
- `housing/forms.py`
- `housing/views.py`

Authentication integration:
- `housing/models.py`
- `housing/migrations/0006_tenant_user.py`


## Consequences

### Positive

- The project now has a clear location for workflow logic.
- Views became cleaner and more focused.
- Service functions can be tested separately.
- The structure supports authentication-aware workflows.
- Tenant and staff workflows are now separated through workflow-specific forms.
- Repair request visibility is now filtered through service-layer logic rather than direct view queries.
- The architecture better responds to Assessment 2 feedback.

### Negative

- The project now has more files.
- Team members need to understand the new separation between views and services.
- Additional integration testing is required across services, permissions and forms.


## Testing Implications

Future tests should verify:
- service functions return correct dashboard summaries
- staff permission helper works correctly
- tenant-specific repair visibility works correctly
- repair creation automatically assigns tenant and dwelling
- views correctly use service-layer functions
- tenant users cannot manually control workflow-only fields


## Assessment 4 Reflection

This decision extends the Assessment 2 architecture rather than replacing it.

Assessment 2 established the Django MVT foundation. Assessment 4 adds a service layer because the application now needs stronger workflow separation, authentication-aware logic and meaningful testing.

## Final Assessment 4 Update

The service layer was expanded after lecturer feedback that the application needed more meaningful workflow depth.

The final service structure includes:

- `repair_request_service.py` for tenant-aware repair creation and repair visibility
- `permission_service.py` for role-based workflow checks
- `dashboard_service.py` for repair summaries and aggregation logic
- `maintenance_service.py` for staff maintenance updates and repair lifecycle changes

The maintenance workflow now uses `transaction.atomic` so the repair status update and maintenance update record are saved as one safe operation. If one part of the workflow fails, Django rolls back the full operation to prevent inconsistent repair data.

This improves the application from a basic CRUD repair system into a more realistic housing repair-management workflow where tenants submit repair requests, staff update progress and managers/staff can view repair summaries.