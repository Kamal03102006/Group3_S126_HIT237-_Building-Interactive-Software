#SArchitectural Decision Record 04 (ADR-04)

 Title  
Use of Django Class-Based Views with QuerySet Optimization and Filtering for Repair Request Management

 Status  
Accepted

 Context  
After defining the system architecture (ADR-01), modelling the domain entities (ADR-02), and refining the data models (ADR-03), the application required a structured way to:

-Display repair requests  
-View detailed repair information  
-Create and update repair requests  
-Track maintenance updates  
-Efficiently retrieve related data  
-Support filtering of repair requests by status and priority  

The system needed to follow Django best practices while ensuring performance, maintainability, and scalability.



 Decision  

We decided to implement Django generic class-based views (CBVs) combined with QuerySet API optimizations and dynamic filtering.

 1.Use of Class-Based Views  
The following CBVs were used:

-ListView → to display all repair requests  
-DetailView → to display a single repair request  
-CreateView → to create repair requests  
-UpdateView → to update repair requests  
-CreateView (MaintenanceUpdate) → to add maintenance updates  

This reduces boilerplate code and improves reusability.



 2.QuerySet Optimization  
We used:

-select_related("dwelling", "tenant", "dwelling__community")  
-prefetch_related("updates")  

This reduces database queries and improves performance by loading related data efficiently.



 3.Dynamic Filtering  
In RepairRequestListView, filtering was implemented using query parameters:

-status  
-priority  

This allows users to dynamically filter repair requests without requiring additional views.



 4.Context Data Customization  
We overrode get_context_data() to pass:

-status choices  
-priority choices  
-selected filter values  

This supports dynamic template rendering and improves user interaction.



 5.Form Handling and User Feedback  
We used Django’s messages framework in:

-RepairRequestCreateView  
-RepairRequestUpdateView  
-MaintenanceUpdateCreateView  

This provides feedback to users after actions such as creating or updating records.



 6.Maintenance Update Handling  
For MaintenanceUpdateCreateView:

-dispatch() was used to retrieve the related RepairRequest  
-form_valid() assigns the repair_request to the update  
-get_success_url() redirects back to the related repair request  

This ensures updates are correctly linked and navigation is consistent.


 Code Reference  

-housing/views.py  
  -RepairRequestListView  
  -RepairRequestDetailView  
  -RepairRequestCreateView  
  -RepairRequestUpdateView  
  MaintenanceUpdateCreateView  



Consequences  

 Positive  

 Reduced code duplication using class-based views  
 Improved performance through QuerySet optimization  
 Better user experience with filtering and messages  
 Clean separation of concerns (MVT architecture)  
 Scalable and maintainable design  



 Negative  

Requires understanding of class-based view structure  
Slightly more complex than function-based views  
 Custom logic (e.g., dispatch) adds complexity  



 Conclusion  

Using Django class-based views with QuerySet optimization and filtering provides a scalable and efficient solution for managing repair requests and maintenance updates. This approach aligns with Django design principles and improves both performance and usability.