ADR-02: Use Related Domain Models with ForeignKey Relationships

Status
Accepted

Context
The remote housing crisis application must allow tenants in remote communities to report housing repair issues, track the status of those requests, and view the maintenance history for their dwelling.
To support these requirements, the system needs a structured and scalable data model that accurately represents real-world entities such as communities, dwellings, tenants, repair requests, and maintenance updates. The design must also support future querying, reporting, and extension of features.

Alternatives Considered

1. Single Large Model (Monolithic Design)
Store all data (tenant, dwelling, repair, and maintenance information) in one large `RepairRequest` model.

Advantages:
- Simple to implement initially  
- Fewer models and relationships  

Disadvantages:
- Data duplication (e.g., dwelling and tenant info repeated)  
- Poor normalization  
- Difficult to maintain and extend  
- Hard to track maintenance history separately  
- Limited flexibility for future features  

2. Multiple Related Models with ForeignKey Relationships
Separate the system into multiple domain-specific models and connect them using Django `ForeignKey` relationships.

Advantages:
- Clear separation of concerns  
- Better object-oriented design  
- Improved data consistency and normalization  
- Easier to extend and maintain  
- Supports efficient QuerySet operations and class-based views  
- Accurately represents real-world relationships  

Disadvantages:
- More complex initial setup  
- Requires understanding of Django model relationships  

Decision
We chose to implement multiple related domain models (Community, Dwelling, Tenant, RepairRequest, and MaintenanceUpdate) connected using 'ForeignKey' relationships.

This design reflects the real-world structure of remote housing systems:
- A Community contains multiple dwellings  
- A Dwelling contains tenants and repair requests  
- A RepairRequest is associated with a dwelling (and optionally a tenant)  
- A MaintenanceUpdate tracks the history of actions taken on a repair request  

This approach aligns with Django’s object-oriented design principles and supports scalability, maintainability, and efficient querying. It also enables future enhancements such as reporting, filtering, and audit history without restructuring the database.

Code Reference
- housing/models.py 5-12 (Community model)
- housing/models.py 15-39 (Dwelling model)
- housing/models.py 42-55 (Tenant model)
- housing/models.py 58-104 (RepairRequest model)
- housing/models.py 107-119 (MaintenanceUpdate model)



Consequences

Positive:
- Strong object-oriented decomposition  
- Clear and maintainable relationships  
- Eliminates data duplication  
- Enables efficient use of Django QuerySets  
- Supports future scalability and feature expansion  

Negative:
- Increased number of models to manage  
- Requires careful handling of migrations  
- Slightly more complex than a single-table approach  
