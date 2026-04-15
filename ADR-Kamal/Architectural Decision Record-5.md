ADR 5: Implement Navigation and Feedback in Templates

Status: Accepted

Context

Users require intuitive navigation and clear feedback to interact effectively with the system.

Alternatives Considered

- Minimal navigation

  Simple but Poor usability
- Structured navigation and feedback

  Improves accessibility and experience but	requires additional design effort

Decision

Navigation links and feedback sections were included within base.html to enhance usability and accessibility.

Code References

- housing/templates/housing/base.html

Example
<nav>
    <a href="{% url 'repairrequest-list' %}">All Requests</a>
    <a href="{% url 'repairrequest-create' %}">Submit Request</a>
</nav>

Consequences

Positive:

- Enhances user experience and accessibility.
- Improves system usability.

Negative:

Requires updates if routes change.
