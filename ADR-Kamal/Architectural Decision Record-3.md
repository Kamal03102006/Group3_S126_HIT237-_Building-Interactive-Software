ADR: Use Django Template Language (DTL) for Dynamic Rendering

Status: Accepted

Context

The application must display dynamic data such as repair requests, tenant details, and maintenance updates from the database.

Alternatives Considered
- Static HTML

Cannot display dynamic data
- Django Template Language

Secure and integrated with Django
- JavaScript Frameworks

Adds unnecessary complexity

Decision

Used Django Template Language to render dynamic content via context variables.

Code References

- housing/templates/housing/repairrequest_list.html
- housing/templates/housing/repairrequest_detail.html

Example

{% for request in repair_requests %}
    <h3>{{ request.title }}</h3>
{% endfor %}

Consequences

Pros:

- Secure and efficient rendering.
- Seamless integration with Django.

Cons:

Limited support for complex logic.
