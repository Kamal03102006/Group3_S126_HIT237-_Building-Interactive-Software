# Entity Relationship Diagram (ERD)

> Updated for Assessment 4 — includes User ↔ Tenant authentication relationship

```mermaid
erDiagram

    USER {
        int id PK
        string username
        string email
        string password
        string role
    }

    TENANT {
        int id PK
        int user_id FK
        int dwelling_id FK
        string first_name
        string last_name
        string phone
        date lease_start
        date lease_end
    }

    COMMUNITY {
        int id PK
        string name
        string address
        string description
    }

    DWELLING {
        int id PK
        int community_id FK
        string unit_number
        string street_address
        string dwelling_type
        bool is_occupied
    }

    REPAIR_REQUEST {
        int id PK
        int tenant_id FK
        int dwelling_id FK
        string title
        string description
        string status
        string priority
        date date_submitted
        date date_resolved
    }

    MAINTENANCE_UPDATE {
        int id PK
        int repair_request_id FK
        string update_note
        string updated_by
        datetime timestamp
    }

    USER ||--|| TENANT : "has profile"
    COMMUNITY ||--o{ DWELLING : "contains"
    DWELLING ||--o{ TENANT : "occupied by"
    TENANT ||--o{ REPAIR_REQUEST : "submits"
    DWELLING ||--o{ REPAIR_REQUEST : "has"
    REPAIR_REQUEST ||--o{ MAINTENANCE_UPDATE : "receives"
```

## Relationships Explained

| Relationship | Type | Description |
|---|---|---|
| User → Tenant | One-to-One | Every tenant has exactly one Django user login account |
| Community → Dwelling | One-to-Many | A community contains multiple dwellings |
| Dwelling → Tenant | One-to-Many | A dwelling can have multiple tenants over time |
| Tenant → RepairRequest | One-to-Many | A tenant can submit many repair requests |
| Dwelling → RepairRequest | One-to-Many | A dwelling can have many repair requests |
| RepairRequest → MaintenanceUpdate | One-to-Many | Each repair request receives multiple status updates |

## Key Change from Assessment 2

The most important new relationship added in Assessment 4 is **User → Tenant (1:1)**.

In Assessment 2, there was no authentication — tenants existed as data only.
In Assessment 4, every Tenant is linked to a Django User account, enabling login and role-based access control.
