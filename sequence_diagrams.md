# Sequence Diagrams

> Assessment 4 — shows how requests flow through Views → Services → Models → Database

---

## Diagram 1: Tenant Submits a Repair Request

```mermaid
sequenceDiagram
    actor Tenant
    participant View as RepairRequestView
    participant Service as repair_request_service
    participant Permission as permission_service
    participant Model as RepairRequest
    participant DB as Database

    Tenant->>View: POST /repair/submit (form data)
    View->>Permission: check_can_submit(user)
    Permission-->>View: OK (user is Tenant)
    View->>Service: create_repair_request(user, form_data)
    Service->>Model: RepairRequest(tenant, dwelling, title, description)
    Model->>DB: INSERT repair request
    DB-->>Model: saved (id=X)
    Model-->>Service: RepairRequest object
    Service-->>View: success
    View-->>Tenant: Redirect to dashboard (success message)
```

---

## Diagram 2: Staff Updates Repair Status

```mermaid
sequenceDiagram
    actor Staff as Maintenance Staff
    participant View as RepairUpdateView
    participant Service as repair_request_service
    participant Permission as permission_service
    participant Model as RepairRequest
    participant DB as Database

    Staff->>View: POST /repair/update (repair_id, new_status)
    View->>Permission: check_can_update_repair(user, repair_id)
    alt Permission Denied
        Permission-->>View: PermissionDeniedForRepair
        View-->>Staff: 403 Forbidden
    else Permission OK
        Permission-->>View: OK
        View->>Service: update_repair_status(repair_id, new_status)
        Service->>Model: validate status transition
        alt Invalid Status
            Model-->>Service: InvalidRepairStatus exception
            Service-->>View: error
            View-->>Staff: Show error message
        else Valid Status
            Model->>DB: UPDATE repair status
            DB-->>Model: updated
            Model-->>Service: updated RepairRequest
            Service-->>View: success
            View-->>Staff: Redirect to dashboard
        end
    end
```

---

## Diagram 3: Tenant Views Own Repairs

```mermaid
sequenceDiagram
    actor Tenant
    participant View as TenantDashboardView
    participant Service as dashboard_service
    participant Permission as permission_service
    participant Model as RepairRequest
    participant DB as Database

    Tenant->>View: GET /dashboard
    View->>Permission: check_has_tenant_profile(user)
    alt No Tenant Profile
        Permission-->>View: TenantProfileMissing
        View-->>Tenant: Redirect to error page
    else Profile Found
        Permission-->>View: OK
        View->>Service: get_tenant_repairs(user)
        Service->>Model: filter(tenant__user=user)
        Model->>DB: SELECT repairs WHERE tenant=X
        DB-->>Model: list of repairs
        Model-->>Service: QuerySet
        Service-->>View: repairs list
        View-->>Tenant: Render dashboard with repairs
    end
```

---

## Summary

| Diagram | What it shows |
|---|---|
| Diagram 1 | How a repair request is created through the service layer |
| Diagram 2 | How permission and status validation work during an update |
| Diagram 3 | How a tenant's dashboard loads with permission checking |

All three diagrams follow the same pattern:
**User → View → Service → Model → Database**

This confirms the service layer architecture separates HTTP logic (views) from business logic (services).
