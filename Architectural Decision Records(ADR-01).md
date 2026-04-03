ADR-01: USE DJANGO MVT ARCHITECTURE

STATUS:
Accepted

CONTEXT:
This project requires to build a scalable and maintainable Django web application for managing housing resources in remote communities. The system must clearly separated from data handling, user interface, and business logic.

ALTERNATIVES CONSIDERED:

1. Function-based structure
Advantages : Simple to implement
Disadvantages : Hard to scale and maintain for larger applications.

2. Custom architecture without Django standards
Pros: Flexible design
Cons: Not aligned with Django best practices

DECISION:
We chose to use Django’s MVT (Model-View-Template) architecture.

Data structure and database relationships will be handled by the Models.
Templates will manage the user interface.
Application logic and data flow will be controled by Views

The approach follows Django design philosophies, and supports scalability and maintainability.

CODE REFERENCE:
-models.py
-views.py
-templates/

CONSEQUENCES:

Positive:
Clear separation of concerns.
Easier to maintain and extend.
Aligns with Django best practices.
Negative:
It requires understanding of Django structure.
Slightly more complex than simple scripts.



