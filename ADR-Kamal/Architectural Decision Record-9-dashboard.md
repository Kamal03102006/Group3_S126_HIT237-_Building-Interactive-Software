# Architectural Decision Record 11: Add Dashboard Aggregation Query Helpers

## Date
25/05/2026

## Status
Proposed and partially implemented – dashboard aggregation helper functions added; custom QuerySet methods pending.

## Related Previous ADRs
- Assessment 2 ADR on Class-Based Views and QuerySets
- ADR 09: Service Layer for Repair Workflow Logic

## Context

Assessment 2 feedback stated that the project could be strengthened by demonstrating stronger QuerySet composition through custom managers and aggregations, with these patterns justified in the ADR.

Assessment 4 introduces dashboards, authenticated workflows and role-based views. These features require more reusable query logic than simple filtering inside views.

## Assessment 2 Limitation

In Assessment 2, the application used useful QuerySet patterns such as:
- `select_related`
- `prefetch_related`
- status filtering
- priority filtering

However, much of the query logic was located directly inside views. There were no reusable dashboard aggregation helpers or custom QuerySet methods.

This made the query logic less reusable and limited the architectural depth of the project.

## Alternatives Considered

### Option 1: Keep filtering and summaries inside views

This is simple but repeats query logic and makes views responsible for too much.

### Option 2: Put dashboard queries inside templates

This would be poor design because templates should focus on presentation, not database query logic.

### Option 3: Add dashboard aggregation helper functions

This provides a dedicated location for dashboard query logic and prepares the project for later custom QuerySet methods.

## Decision

The project will add dashboard aggregation helper functions inside:

`housing/services/dashboard_service.py`

The first helper functions include:
- repair count by status
- repair count by priority
- repair count by community
- total/open/urgent repair summaries

Custom QuerySet methods may be added later after integration planning with the model owner.

## Code References

Implemented:
- `housing/services/dashboard_service.py`

Planned integration:
- `housing/models.py`
- `housing/views.py`
- dashboard templates

## Consequences

### Positive

- Dashboard query logic becomes reusable.
- The project directly responds to Assessment 2 feedback about aggregations.
- Views can later call service helpers instead of containing all query logic.
- The system better supports manager-level summaries.

### Negative

- The helper functions are not fully visible in the UI until dashboard integration is completed.
- Custom QuerySet methods still need to be discussed before modifying shared model code.

## Testing Implications

Future tests should verify:
- status summary totals
- priority summary totals
- community repair totals
- open repair counts
- urgent repair counts

## Assessment 4 Reflection

This decision directly responds to Assessment 2 feedback. Instead of only using basic filtering inside views, Assessment 4 introduces reusable aggregation helpers to support dashboard features and stronger QuerySet reasoning.