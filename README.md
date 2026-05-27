# 🏠 Housing Repair Management System

> A Django web application for managing housing repair requests across community dwellings.
> Developed by Group 3 — HIT237 Building Interactive Software (Assessment 2 → Assessment 4).

---

## Table of Contents

- [Project Overview](#project-overview)
- [Evolution: Assessment 2 → Assessment 4](#evolution-assessment-2--assessment-4)
- [Architecture Summary](#architecture-summary)
- [Setup Instructions](#setup-instructions)
- [How to Run the Server](#how-to-run-the-server)
- [How to Run Tests](#how-to-run-tests)
- [User Roles](#user-roles)
- [Demo Accounts](#demo-accounts)
- [AI Usage Statement](#ai-usage-statement)
- [Team Contributions](#team-contributions)
- [File Structure](#file-structure)

---

## Project Overview

The Housing Repair Management System allows tenants to submit repair requests for their dwellings, maintenance staff to update repair statuses, and housing managers to oversee all activity across the community.

**Built with:**
- **Backend:** Django 4.2
- **Database:** SQLite (development)
- **Frontend:** Django templates
- **Authentication:** Django built-in auth extended with role-based permissions

**Core Features:**
- Tenants can submit and track repair requests
- Maintenance staff can view and update repair statuses
- Housing managers have full visibility and control
- Role-based access control enforced at the service layer
- Custom domain exception handling

---

## Evolution: Assessment 2 → Assessment 4

| Feature | Assessment 2 | Assessment 4 |
|---|---|---|
| Models | ✅ Dwelling, Tenant, RepairRequest | ✅ Extended with User ↔ Tenant (1:1) |
| Authentication | ❌ Not implemented | ✅ Login/logout, role-based groups |
| Service Layer | ❌ Logic mixed into views | ✅ Dedicated service modules |
| Exception Handling | ❌ Minimal | ✅ Custom domain exceptions |
| Testing | ❌ Not implemented | ✅ Models, services, views, permissions |
| ADR | ADR-01, 02, 03 | ✅ Updated with new entries, superseded entries marked |
| Diagrams | Basic ERD | ✅ Updated ERD, class diagram, sequence diagrams |

---

## Architecture Summary

```
Views  (HTTP layer — handles requests and responses)
  ↓
Services  (business logic — permissions, repair workflows, dashboard)
  ↓
Models  (data layer — Dwelling, Tenant, RepairRequest, MaintenanceUpdate)
  ↓
Database  (SQLite)
```

### Service Modules

| Module | Responsibility |
|---|---|
| `permission_service` | Checks whether a user has rights to perform an action |
| `repair_request_service` | Handles creation and status updates of repair requests |
| `dashboard_service` | Aggregates data for role-specific dashboard views |

### Custom Exceptions

| Exception | When Raised |
|---|---|
| `HousingDomainError` | Base class for all domain-level errors |
| `TenantProfileMissing` | Authenticated user has no linked Tenant profile |
| `PermissionDeniedForRepair` | User lacks permission to access or modify a repair |
| `InvalidRepairStatus` | A repair status transition is not allowed |

---

## Setup Instructions

### Requirements
- Python 3.10 or higher
- pip

### Steps

```bash
# 1. Clone the repository
git clone https://github.com/Kamal03102006/Group3_S126_HIT237-_Building-Interactive-Software.git
cd Group3_S126_HIT237-_Building-Interactive-Software

# 2. Create and activate a virtual environment
python -m venv venv

# Windows:
venv\Scripts\activate

# Mac/Linux:
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Apply database migrations
python manage.py migrate

# 5. Create demo users (if fixture available)
python manage.py loaddata demo_users.json

# OR create a superuser manually
python manage.py createsuperuser
```

---

## How to Run the Server

```bash
python manage.py runserver
```

Open browser: [http://127.0.0.1:8000](http://127.0.0.1:8000)

Django admin panel: [http://127.0.0.1:8000/admin](http://127.0.0.1:8000/admin)

---

## How to Run Tests

```bash
# Run all tests
python manage.py test

# Run with detailed output
python manage.py test --verbosity=2

# Run tests for housing app only
python manage.py test housing
```

The test suite covers:
- Model behaviour and validation
- Service layer logic (repair creation, status updates)
- View responses and redirects
- Permission boundary enforcement (e.g. tenant cannot edit another tenant's repair)

---

## User Roles

| Role | Description |
|---|---|
| **Tenant** | Submit repair requests, view own request history |
| **Maintenance Staff** | View assigned repairs, update repair status |
| **Housing Manager** | Full access — manage all repairs, tenants, and community |

Roles are managed via Django groups. Each user is assigned to one group on account creation.

---

## Demo Accounts

> ⚠️ For development and assessment demonstration only.

| Role | Username | Password |
|---|---|---|
| Tenant | tenantdemo | demo12345 |
| Maintenance Staff | staffdemo | demo12345 |
| Housing Manager | managerdemo | demo12345 |

Login page: [http://127.0.0.1:8000/login](http://127.0.0.1:8000/login)

---

## AI Usage Statement

AI tools (including GitHub Copilot, ChatGPT, and Claude) were used to support this project in the following ways:

- **Planning:** Generating initial outlines for service layer structure and ADR entries
- **Code assistance:** Suggesting boilerplate for authentication views, service functions, and test cases
- **Debugging:** Identifying issues in permission logic and exception handling
- **Documentation:** Drafting README sections and diagram descriptions

In all cases, generated output was critically reviewed, adapted, and tested by team members before inclusion in the final project. AI-generated test cases were evaluated to ensure they test meaningful behaviour rather than trivial implementation details.

---

## Team Contributions

| Member | Responsibility |
|---|---|
| Mehak (Member 1) | User authentication, login/logout views, role-based group setup, demo accounts |
| Kamal (Member 2) | Service layer (repair_request_service, permission_service, dashboard_service), custom exceptions |
| Harsimran (Member 3) | Test suite covering models, services, views, and permission boundaries |
| Tanu (Member 4) | README, ERD, class diagrams, sequence diagrams, project plan, final documentation |

---

## File Structure

```
Group3_S126_HIT237-_Building-Interactive-Software/
│
├── README.md                        ← This file
├── requirements.txt                 ← Python dependencies (Django 4.2)
├── manage.py                        ← Django management commands
├── .gitignore
│
├── config/                          ← Django project settings
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
├── housing/                         ← Main Django app
│   ├── models.py
│   ├── views.py
│   ├── forms.py
│   ├── urls.py
│   ├── admin.py
│   ├── exceptions.py
│   ├── services/
│   │   ├── permission_service.py
│   │   ├── repair_request_service.py
│   │   └── dashboard_service.py
│   └── tests/
│       ├── test_models.py
│       ├── test_services.py
│       ├── test_views.py
│       └── test_permissions.py
│
├── Architectural Decision Records(ADR-01).md
├── Architectural Decision Records(ADR-02).md
├── Architectural Decision Records(ADR-03).md
├── Architectural Decision Record-1-templates.md
└── GROUP-CONTRACT-GROUP-3.md
```

---

*Last updated: Assessment 4 — May 28, 2026*
