ADR: Use Reusable Form Templates

Status: Accepted

Context

Users need to submit and update repair requests and maintenance updates. Consistent form design improves usability and maintainability.

Alternatives Considered

- Separate templates for each form

Repetitive and inconsistent
- Reusable form templates

Maintainable and consistent

Decision

Implemented reusable templates integrated with Django ModelForm.

Code References

housing/templates/housing/repairrequest_form.html
housing/templates/housing/maintenanceupdate_form.html
housing/forms.py

Consequences

Pros:

- Ensures consistency across forms.
- Improves maintainability and user experience.

Cons:

Requires coordination with backend development.