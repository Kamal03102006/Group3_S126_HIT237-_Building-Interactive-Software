ADR: Use Template Inheritance with base.html

Status: Accepted
Date: 10 April 2026

Context

The application requires multiple web pages, including repair request lists, details, submission forms, and maintenance updates. Maintaining consistency across these pages while avoiding repetitive HTML code is essential for scalability and maintainability.

Alternatives Considered
Option	Description	Pros	Cons
Duplicate HTML in every template	Each page contains full layout code	Simple to implement	Difficult to maintain and inconsistent
Use Django template inheritance	Shared layout with reusable blocks	Reduces redundancy and ensures consistency	Requires initial setup
Decision

Django template inheritance was implemented using a shared base.html file, which defines the global layout and styling.

Code Reference
housing/templates/housing/base.html
housing/templates/housing/repairrequest_list.html  # gonna commit soon
housing/templates/housing/repairrequest_detail.html # gonna commit soon
housing/templates/housing/repairrequest_form.html # gonna commit soon
housing/templates/housing/maintenanceupdate_form.html # gonna commit soon
Consequences

Positive:

Ensures consistent UI across the application.
Reduces code duplication.
Simplifies future enhancements.

Negative:

Changes to base.html affect all templates
