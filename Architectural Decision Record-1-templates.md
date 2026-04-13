## ADR 008: Use template inheritance with a shared base template

**Status:** Accepted

**Context:**  
The application includes multiple pages such as dashboard, repair list, repair detail, and dwelling detail. These pages share common layout elements such as navigation, styling, and message display.

**Alternatives considered:**  
1. Repeat HTML structure in every template  
   - Quick to implement  
   - Causes duplication  
   - Hard to maintain

2. Use a shared base template with inheritance  
   - Cleaner structure  
   - Reduces duplication  
   - Easier to update UI globally

**Decision:**  
Use a shared `base.html` template with `{% extends %}` and reusable components.

**Rationale:**  
This follows Django’s DRY (Don’t Repeat Yourself) principle and ensures consistent UI across all pages. It also makes future UI updates easier and reduces maintenance effort.

**Code reference:**  (will commit in github till weekend)
`templates/base.html`  
`templates/dashboard/dashboard.html`  
`templates/housing/*.html`

**Consequences:**  
All templates must follow the same structure, but this improves consistency and scalability.

---
