ADR-03: Employing Class-Based Views and QuerySets for Handling Repair Request Data

Status
Accepted

Context
The project involves displaying and managing repair requests in an efficient manner. There is a need to fetch associated data like the dwelling and tenant information from the database while adhering to software engineering best practices.

Decision
Class-based views from Django were adopted to build the listing and detail functionalities of repair requests.

Django QuerySet methods were utilized to achieve:
-select_related() for efficient retrieval of related objects' data
-order_by() for sorting repair requests based on reporting time in reverse chronological order

Code Reference
-views.py
-RepairRequestListView (lines 5–15)
-RepairRequestDetailView (lines 18–27)
-urls.py`

Consequences

 Benefits
-Minimal coding effort using Django's generic views
-Enhanced efficiency with the select_related()method
-Maintains proper encapsulation principles (MVT architecture)
-Allows for better scalability and reusability of views

 Drawbacks
-Requires comprehension of Django class-based views design
-Less adaptable compared to function-based views