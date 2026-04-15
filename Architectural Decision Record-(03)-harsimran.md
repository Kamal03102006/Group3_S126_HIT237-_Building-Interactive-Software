#Architectural Decision Record 05 (ADR-05)

#Title  
Use Django ModelForms for Structured Input Validation and Data Entry

#Status  
Accepted

#Context  
The housing application requires users to create and manage repair requests and maintenance updates through structured forms. Because these forms interact directly with database models, the input process must be consistent, maintainable, and validated against the system’s data rules.

A design decision was needed on whether to:
-build forms manually using standard Django forms, or
-use Django ModelForm` classes connected directly to the application models.

The application also required validation to ensure that a selected tenant belongs to the selected dwelling when submitting a repair request.



#Decision  
We decided to use Django ModelForm classes for both RepairRequest` and MaintenanceUpdate.

Two forms were implemented:
-RepairRequestForm`
-MaintenanceUpdateForm`

The forms are directly linked to their corresponding models:
-RepairRequestForm → RepairRequest`
-MaintenanceUpdateForm → MaintenanceUpdate`

We also added:
-custom widget configuration for multi-line notes and descriptions
-custom validation in RepairRequestForm.clean()` to ensure the selected tenant belongs to the selected dwelling



#Rationale  
This approach was selected because Django ModelForm` provides a structured and maintainable way to connect forms directly to the data model.

#Why this approach was chosen:
-reduces duplication between models and forms
-automatically uses model field definitions and validation
-improves consistency between user input and database schema
-simplifies form creation and maintenance
-supports additional custom validation where business rules require it

The clean() method in RepairRequestForm` was especially important because it enforces a domain rule that cannot be fully guaranteed by field definitions alone: a tenant must belong to the selected dwelling.



#Alternatives Considered  

#1. Use regular Django Form classes
Advantages:
-full control over every form field
-flexible for custom behavior

Disadvantages:
-duplicates model definitions
-requires more manual validation
-harder to maintain as the models evolve



#2. Handle validation only in views
Advantages:
-keeps form definitions simple
-allows validation closer to request handling

Disadvantages:
-mixes validation logic into views
-reduces reusability
-makes forms less self-contained



#3. Use Django ModelForm with custom validation
Advantages:
-directly linked to models
-less repetitive code
-easier to maintain
-supports both model-level and form-level validation
-keeps validation logic close to data input

Disadvantages:
-requires understanding of Django form lifecycle
-some custom rules still need explicit methods such as clean()`



#Consequences  

#Positive:
-improves consistency between forms and models
-reduces duplicated code
-supports clear and reusable validation logic
-improves usability through custom widgets
-ensures better data integrity during input

#Negative:
-introduces another layer developers must understand
-custom validation must be maintained if model relationships change



#Code Reference  
-housing/forms.py`
  -RepairRequestForm`
  -MaintenanceUpdateForm
  -custom validation in RepairRequestForm.clean()



#Conclusion  
Using Django ModelForm classes provides a clean and maintainable approach to data entry in the housing application. It aligns form behavior with the underlying data model and supports custom validation rules required by the project domain.