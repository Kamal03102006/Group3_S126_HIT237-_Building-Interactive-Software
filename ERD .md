Entity Relationship Diagram(ERD)
The ERD illustrates the databasestructure of the Remote Housing Repair Tracker, a Django-based web application design to manage housing repare request in a remort Northern Territory communities. The ERD defines the relationship between key entities and ensure data intergrity, scalability, and normalization
This diagram directly reflects the Django models implemented in the application.

Visual ERD
The visual ERD provides a clear and professional representation of the system's database schema.

Mermaid ERD(Editable Version)
The Mermaid ERD offers a text-based, version-controlled representation that can be rendered directly within GitHub

Entity Descriptions

Entity              Description
Community           Represents remote communities in the Northern Territory.
Dwelling            Stores housing details located within a community.
Tenant              Contains information about residents living in dwellings
Repair Request      Records maintenance issues reported by tenants.
maintenance Update  Tracks updates and progress of repair requests.

Relationship Summary
Relationshiop                                 Type                                        Description
Community - Dwelling                        One-to-many                                   A community contains multiple dwellings.
Dwelling - Tenant                           one-to-many                                   A dwelling may house multiple tenants 
Dwelling -- RepairRequest                   one-to-many                                   Repair requests are associated with dwellings.
Tenant RepairRequest                        one-to-many(optional)                         A tenant can submit multiple repair requests.
RepairRequest- MaintenanceUpdate            one-to-many                                   Each repair request can have multiple updates 
  
Alignment with Django Models   
Django Model                                Datbase Table
Community                                   COMMUNITY
Dwelling                                    DWELLING
Tenant                                      TENANT
RepairRequest                               REPAIRREQUEST
MaintenceUpdate                             MAINTENANCEUPDATE

Academic Relevance

This ERD supports the assessment requirements by demonstrating:
Data modelling and normalization
Object-oriented system design
Accurate representation of Django model relationships
Industry-standard documentation practices

