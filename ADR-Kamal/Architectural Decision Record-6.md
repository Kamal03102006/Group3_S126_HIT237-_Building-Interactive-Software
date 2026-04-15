ADR: Implement Filtering in the Repair Request List

Status: Accepted

Context

Users need to identify urgent and pending repair requests efficiently.

Alternatives Considered

- Display All Records

Inefficient for large datasets
- Client-Side Filtering

Requires additional scripting
- Server-Side Filtering Using QuerySets

Efficient and scalable

Decision

Implemented server-side filtering using Django QuerySets and rendered results via templates.

Code References

- housing/views.py
- housing/templates/housing/repairrequest_list.html

Consequences

Pros:

- Improves usability and performance.
- Demonstrates Django QuerySet proficiency.

Cons:

Adds complexity to view logic.
