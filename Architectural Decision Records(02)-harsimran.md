#Architectural Decision Record 05 (ADR-05)

#Title  
Use of URL Routing to Connect Class-Based Views in Housing Application

#Status  
Accepted

#Context  
After implementing models (ADR-02, ADR-03) and views using Django class-based views (ADR-04), the application required a clear and structured way to connect URLs to the corresponding views.

The system needed:
-Navigation between pages
-Clean and readable URLs
-Support for CRUD operations (Create, Read, Update)
-Integration with Django reverse URL resolution



#Decision  

We decided to use Django’s URL routing system (path) to map URLs to class-based views in housing/urls.py.



#1. Mapping Views to URLs  

Each class-based view was connected to a specific URL:

- RepairRequestListView → `/`
- RepairRequestDetailView → `/repairs/<id>/`
- RepairRequestCreateView → `/repairs/new/`
- RepairRequestUpdateView → `/repairs/<id>/edit/`
- MaintenanceUpdateCreateView → `/repairs/<id>/updates/new/`

This provides a clear structure for navigation and user interaction.



#2. Use of Named URLs  

Each URL pattern was assigned a name:

-repairrequest-list
-repairrequest-detail
-repairrequest-create
-repairrequest-update
-maintenanceupdate-create

These names are used in:
-get_absolute_url() in models
-templates for navigation

This supports Django’s reverse URL resolution and improves maintainability.



#3. REST-like URL Design  

The URL structure follows a logical and REST-like pattern:

- `/repairs/` → list  
- `/repairs/<id>/` → detail  
- `/repairs/new/` → create  
- `/repairs/<id>/edit/` → update  

This makes the application intuitive and user-friendly.



#4. Integration with Django Architecture  

The URL configuration connects:
-Views (business logic)
-Templates (presentation)
-Models (data layer)

This supports Django’s Model–View–Template (MVT) architecture.



#Code Reference  

-housing/urls.py
  - All path() definitions
-config/urls.py
  - include("housing.urls")



#Consequences  

#Positive  

-Clear and maintainable navigation structure  
-Easy integration with templates and models  
-Supports reverse URL lookup  
-Scalable for adding new features  


#Negative  

-Requires consistency in naming across models, views, and templates  
-Incorrect naming can lead to runtime errors  


#Conclusion  

Using Django URL routing provides a clean and structured way to connect views with user-facing routes. This decision ensures consistency, scalability, and alignment with Django best practices.