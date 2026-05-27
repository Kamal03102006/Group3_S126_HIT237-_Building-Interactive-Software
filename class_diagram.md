# Class Diagram

> Assessment 4 — includes Models, Services, Exceptions, Forms, and Views

```mermaid
classDiagram

    %% ─── MODELS ───────────────────────────────────────────

    class User {
        +int id
        +string username
        +string email
        +string password
        +string role
        +is_authenticated()
    }

    class Tenant {
        +int id
        +User user
        +Dwelling dwelling
        +string first_name
        +string last_name
        +string phone
        +date lease_start
        +date lease_end
        +__str__()
    }

    class Community {
        +int id
        +string name
        +string address
        +__str__()
    }

    class Dwelling {
        +int id
        +Community community
        +string unit_number
        +string street_address
        +bool is_occupied
        +__str__()
    }

    class RepairRequest {
        +int id
        +Tenant tenant
        +Dwelling dwelling
        +string title
        +string description
        +string status
        +string priority
        +date date_submitted
        +date date_resolved
        +__str__()
    }

    class MaintenanceUpdate {
        +int id
        +RepairRequest repair_request
        +string update_note
        +string updated_by
        +datetime timestamp
        +__str__()
    }

    %% ─── SERVICES ─────────────────────────────────────────

    class permission_service {
        +check_can_submit(user)
        +check_can_update_repair(user, repair_id)
        +check_has_tenant_profile(user)
        +check_is_manager(user)
    }

    class repair_request_service {
        +create_repair_request(user, form_data)
        +update_repair_status(repair_id, new_status)
        +get_repair_by_id(repair_id)
        +get_repairs_for_tenant(user)
    }

    class dashboard_service {
        +get_tenant_repairs(user)
        +get_all_repairs()
        +get_staff_repairs(user)
        +get_repair_summary()
    }

    %% ─── EXCEPTIONS ───────────────────────────────────────

    class HousingDomainError {
        +string message
    }

    class TenantProfileMissing {
        +string message
    }

    class PermissionDeniedForRepair {
        +string message
        +int repair_id
    }

    class InvalidRepairStatus {
        +string message
        +string attempted_status
    }

    %% ─── FORMS ────────────────────────────────────────────

    class RepairRequestForm {
        +title
        +description
        +priority
        +clean()
        +save()
    }

    class RepairStatusUpdateForm {
        +status
        +update_note
        +clean()
    }

    %% ─── VIEWS ────────────────────────────────────────────

    class TenantDashboardView {
        +get(request)
        +uses: dashboard_service
        +uses: permission_service
    }

    class RepairRequestView {
        +get(request)
        +post(request)
        +uses: repair_request_service
        +uses: permission_service
    }

    class RepairUpdateView {
        +get(request, repair_id)
        +post(request, repair_id)
        +uses: repair_request_service
        +uses: permission_service
    }

    %% ─── RELATIONSHIPS ────────────────────────────────────

    User "1" --> "1" Tenant : has profile
    Community "1" --> "many" Dwelling : contains
    Dwelling "1" --> "many" Tenant : occupied by
    Tenant "1" --> "many" RepairRequest : submits
    Dwelling "1" --> "many" RepairRequest : has
    RepairRequest "1" --> "many" MaintenanceUpdate : receives

    HousingDomainError <|-- TenantProfileMissing : extends
    HousingDomainError <|-- PermissionDeniedForRepair : extends
    HousingDomainError <|-- InvalidRepairStatus : extends

    TenantDashboardView --> permission_service : uses
    TenantDashboardView --> dashboard_service : uses
    RepairRequestView --> permission_service : uses
    RepairRequestView --> repair_request_service : uses
    RepairUpdateView --> permission_service : uses
    RepairUpdateView --> repair_request_service : uses

    repair_request_service --> RepairRequest : manages
    dashboard_service --> RepairRequest : queries
    permission_service --> Tenant : checks
```

## Class Summary

### Models
| Class | Purpose |
|---|---|
| User | Django auth user — linked to Tenant for login |
| Tenant | Resident profile linked to a User and Dwelling |
| Community | A housing community containing multiple dwellings |
| Dwelling | A single unit within a community |
| RepairRequest | A repair job submitted by a Tenant |
| MaintenanceUpdate | A status update on a RepairRequest |

### Services
| Class | Purpose |
|---|---|
| permission_service | Checks user rights before any action |
| repair_request_service | Handles repair creation and status updates |
| dashboard_service | Fetches data for role-specific dashboards |

### Exceptions
| Class | Purpose |
|---|---|
| HousingDomainError | Base exception for all domain errors |
| TenantProfileMissing | Raised when logged-in user has no Tenant profile |
| PermissionDeniedForRepair | Raised when user tries to access a repair they cannot |
| InvalidRepairStatus | Raised when a status change is not allowed |
