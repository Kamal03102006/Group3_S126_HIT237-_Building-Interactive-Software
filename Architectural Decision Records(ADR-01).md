ADR-01: USE DJANGO MVT ARCHITECTURE

STATUS:
Accepted

CONTEXT:
The project requires building a Django web application that enables tenants in remote communities to report housing repair issues, track repair status, and view maintenance history.
The system must clearly separate data management (repair records, tenants, dwellings), user interface (forms and dashboards), and application logic (processing repair requests and updates).

ALTERNATIVES CONSIDERED:
1. Function-based structure
Advantages: Simple and quick to implement
Disadvantages:
 Difficult to scale for complex workflows like repair tracking
 Poor separation of concerns
 Hard to maintain as the system grows

2. Custom architecture without Django standards
Advantages: Flexible design
Disadvantages:
 Not aligned with Django best practices
 Increased development complexity
 Reduced maintainability

DECISION: 
We chose Django’s MVT (Model-View-Template) architecture.
Models handle domain entities such as Dwelling, Tenant, RepairRequest, and MaintenanceUpdate.
Views manage application logic, such as processing repair submissions and updating statuses.
Templates provide the user interface for tenants to log and track repairs.

This architecture ensures clear separation of concerns and supports maintainable, scalable development aligned with Django design philosophies.

CODE REFERENCE:
housing/models.py: 1-119
housing/views.py
housing/templates/



CONSEQUENCES:

Positive:
Clear separation of concerns.
Easier to maintain and extend.
Aligns with Django best practices.
Negative:
It requires understanding of Django structure.
Slightly more complex than simple scripts.



