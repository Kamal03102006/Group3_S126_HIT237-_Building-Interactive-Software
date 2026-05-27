# Architectural Decision Record 09: Add Dashboard Aggregation Query Helpers

## Date
25/05/2026

## Status
Partially implemented – dashboard aggregation helpers integrated with authenticated repair workflows; final dashboard presentation testing pending.

## Related Previous ADRs
- Assessment 2 ADR on Class-Based Views and QuerySets
- ADR 08: Service Layer for Repair Workflow Logic


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

The project added dashboard aggregation helper functions inside:

`housing/services/dashboard_service.py`

The implemented helper functions include:
- repair count by status
- repair count by priority
- repair count by community
- total/open/urgent repair summaries

Dashboard aggregation helpers are now connected to authenticated repair workflows through the service layer. Dashboard summaries are filtered according to the repair requests visible to the authenticated user.


## Code References

Implemented:
- `housing/services/dashboard_service.py`
- `housing/services/repair_request_service.py`
- `housing/views.py`

Future enhancements:
- dashboard templates
- optional custom QuerySet methods


## Consequences

### Positive

- Dashboard query logic became reusable.
- The project directly responds to Assessment 2 feedback about aggregations.
- Views can call service helpers instead of containing all query logic.
- Dashboard summaries now support authenticated and tenant-aware repair visibility.
- Aggregation logic is reusable across multiple views and workflows.
- The system better supports manager-level summaries.

### Negative

- Dashboard presentation still requires further UI testing.
- Custom QuerySet methods may still be added later.
- Dashboard visibility depends on correctly configured user roles and tenant links.


## Testing Implications

Future tests should verify:
- status summary totals
- priority summary totals
- community repair totals
- open repair counts
- urgent repair counts
- tenant users only see summaries related to their own repairs


## Assessment 4 Reflection

This decision directly responds to Assessment 2 feedback.

Instead of only using basic filtering inside views, Assessment 4 introduces reusable aggregation helpers to support dashboard features, authenticated workflows and stronger QuerySet reasoning.

## Final Assessment 4 Update

A custom `RepairRequestQuerySet` was added to support reusable repair workflow queries such as:

- open repairs
- urgent repairs
- completed repairs
- in-progress repairs
- status summaries
- priority summaries
- community summaries

The dashboard service now uses these QuerySet methods instead of repeating query logic inside views. This directly responds to Assessment 2 feedback about stronger QuerySet composition and aggregation.

This also improves feature depth because the application can now support staff and manager decision-making through repair summaries instead of only displaying a simple repair list.