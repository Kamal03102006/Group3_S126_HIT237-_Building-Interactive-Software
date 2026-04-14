ADR: Implement Custom CSS for User Interface Design

Status: Accepted

Context

The system is designed for tenants in remote communities, requiring a clear and accessible interface.

Alternatives Considered
- Default Django Styling

  Basic and unattractive-No
- Bootstrap Framework

  Responsive but adds dependency- yes
- Custom CSS

  Lightweight and tailored- yes

Decision

Implemented custom CSS within base.html to provide a clean and responsive interface.

Code References

housing/templates/housing/base.html

Consequences

Pros:

- Enhances usability and accessibility.
- Keeps the application lightweight.

Cons:

Requires manual styling updates.
