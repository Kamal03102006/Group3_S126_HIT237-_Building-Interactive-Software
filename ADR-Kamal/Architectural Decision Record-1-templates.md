ADR: Use Template Inheritance with base.html

Status: Accepted

Context

The application includes multiple pages such as repair request lists, details, and submission forms. A consistent and maintainable layout is required.

Alternatives Considered

- Duplicate HTML in each template

  Simple but Difficult to maintain
- Template inheritance using base.html

  Reusable and consistent but Requires initial setup

Decision

Implemented Django template inheritance using a shared base.html to define layout, navigation, and styling.

Code References

- housing/templates/housing/base.html
- housing/templates/housing/repairrequest_list.html  
- housing/templates/housing/repairrequest_detail.html 
- housing/templates/housing/repairrequest_form.html    
- housing/templates/housing/maintenanceupdate_form.html  

Consequences

Pros:

- Ensures consistent UI.
- Reduces code duplication.
- Simplifies future updates.

Cons:

Changes to base.html affect all templates.
