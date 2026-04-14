ADR: Use Django Messages Framework for User Feedback

Status: Accepted

Context

Users require confirmation messages when submitting or updating repair requests.

Alternatives Considered

- No Feedback

Poor user experience
- JavaScript Alerts

Less integrated with Django
- Django Messages Framework

Secure and built-in

Decision

Implemented Django Messages Framework for success notifications.

Code References

housing/templates/housing/base.html
housing/views.py

Example

{% if messages %}
    {% for message in messages %}
        <div class="message">{{ message }}</div>
    {% endfor %}
{% endif %}

Consequences

Pros:

- Improves usability and user satisfaction.
- Provides immediate feedback.

Cons:

Requires proper configuration.