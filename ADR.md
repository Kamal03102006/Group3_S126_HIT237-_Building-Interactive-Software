# Architecture Decision Records (ADR)

> An Architecture Decision Record (ADR) captures an important architectural decision made along with its context and consequences.
>
> Template based on [Michael Nygard's ADR format](https://github.com/joelparkerhenderson/architecture-decision-record).

---

## ADR-1: Standardise URL Routing and Connect All Views to Templates

**Date:** 2026-04-12

### Status

Accepted

### Context

The project root URL configuration (`config/urls.py`, line 5) uses `include('housing.urls')` to delegate all housing-related routes to the housing application. However, the housing app's URL module was saved as `url.py` rather than the Django-conventional `urls.py`. At runtime this produced a `ModuleNotFoundError` because Python could not resolve `housing.urls`.

Beyond the naming issue, the existing URL patterns only registered two routes — a list view and a detail view for repair requests — while the templates directory contained `house_list.html` and `request_list.html` that were not wired to any view or URL. No route existed for creating, editing, or deleting repair requests either, meaning the application only supported read-only browsing.

### Alternatives Considered

| # | Alternative | Pros | Cons |
|---|------------|------|------|
| 1 | **Change the `include()` call** to `include('housing.url')` so it matches the existing filename | Single one-line change; no file rename needed | Violates Django convention (`urls.py`); confuses future contributors who expect the standard name; every Django tutorial and linter assumes `urls.py` |
| 2 | **Rename the file to `urls.py` and expand the URL patterns** to cover every view and template in the app | Follows Django convention; every template becomes reachable; supports full CRUD workflow | Requires renaming a file and adding several new URL entries (more changes overall) |

### Decision

We chose **Alternative 2**. The file `housing/url.py` was renamed to `housing/urls.py`, and the URL patterns were expanded to six routes:

| Route | View | Name |
|-------|------|------|
| `/` | `RepairRequestListView` | `repairrequest-list` |
| `/houses/` | `DwellingListView` | `dwelling-list` |
| `/repairs/<id>/` | `RepairRequestDetailView` | `repairrequest-detail` |
| `/repairs/create/` | `RepairRequestCreateView` | `repairrequest-create` |
| `/repairs/<id>/edit/` | `RepairRequestUpdateView` | `repairrequest-update` |
| `/repairs/<id>/delete/` | `RepairRequestDeleteView` | `repairrequest-delete` |

### Code Reference

| File | Lines | What changed |
|------|-------|--------------|
| `config/urls.py` | 5 | `include('housing.urls')` — unchanged, now resolves correctly |
| `housing/urls.py` | 1–18 | Renamed from `url.py`; six URL patterns defined |

### Consequences

**What becomes easier:**
- The application follows standard Django conventions, so any Django developer can navigate the codebase immediately.
- Every template is reachable through a named URL; the `{% url %}` tag works in all templates without error.
- Full CRUD operations are exposed to the browser, not just read-only views.

**What becomes harder or requires attention:**
- Any existing branch, CI script, or documentation referencing `housing/url.py` must be updated to `housing/urls.py`.
- Adding new routes now goes through `housing/urls.py`, which is a longer file to maintain (18 lines vs. the original 7).

---

## ADR-2: Fix Template–View Mismatch Bug Discovered During Testing

**Date:** 2026-04-12

### Status

Accepted

### Context

During the first test run after cloning the repository, every page returned a Django `TemplateDoesNotExist` error. Investigation revealed two related bugs:

1. **Views pointed to non-existent templates.** `RepairRequestListView` set `template_name = "housing/repairrequest_list.html"` and `RepairRequestDetailView` set `template_name = "housing/repairrequest_detail.html"`, but neither file existed. The only templates on disk were `house_list.html` and `request_list.html`.

2. **Existing templates had duplicate content and wrong field names.** Both `house_list.html` and `request_list.html` contained two identical `<h1>Available Houses</h1>` blocks and referenced model attributes `house.location` and `house.capacity`, which do not exist on the `Dwelling` model (see `housing/models.py`, lines 18–42). The actual fields are `house_code`, `address`, `bedrooms`, and `condition_status`.

These two bugs together meant the application was completely non-functional — no page could render.

### Alternatives Considered

| # | Alternative | Pros | Cons |
|---|------------|------|------|
| 1 | **Rename existing templates** to match the names the views expect (`repairrequest_list.html`, `repairrequest_detail.html`) | No new files; minimal changes | `house_list.html` is semantically a dwelling list, not a repair-request detail; its content would not suit a detail view; leaves no template for a dwelling list view |
| 2 | **Update the views** to use the existing template filenames, fix the template content to match the actual models, and create missing templates for detail/form/delete | Every template matches a real view; field names align with the database schema; no duplicate HTML | More files to create (3 new templates) and 2 existing templates to edit |

### Decision

We chose **Alternative 2**:

- `RepairRequestListView.template_name` was changed to `"housing/request_list.html"`.
- A new `DwellingListView` was created to serve `"housing/house_list.html"`.
- Both existing templates were rewritten: duplicate `<h1>` blocks removed, field names corrected to `house_code`, `address`, `community`, `bedrooms`, `condition_status`.
- Three new templates were created: `repairrequest_detail.html`, `repairrequest_form.html`, `repairrequest_confirm_delete.html`.

### Code Reference

| File | Lines | What changed |
|------|-------|--------------|
| `housing/views.py` | 6–12 | New `DwellingListView` using `house_list.html` |
| `housing/views.py` | 15–26 | `RepairRequestListView` now uses `request_list.html` |
| `housing/views.py` | 29–39 | `RepairRequestDetailView` — prefetches `updates` |
| `housing/templates/housing/house_list.html` | 1–38 | Rewrote with correct `Dwelling` model fields |
| `housing/templates/housing/request_list.html` | 1–49 | Rewrote with `RepairRequest` model fields and navigation links |
| `housing/templates/housing/repairrequest_detail.html` | 1–38 | New file — shows full request details and maintenance updates |
| `housing/templates/housing/repairrequest_form.html` | 1–19 | New file — shared create/edit form with CSRF token |
| `housing/templates/housing/repairrequest_confirm_delete.html` | 1–14 | New file — delete confirmation page |

### Consequences

**What becomes easier:**
- All six URLs return HTTP 200 — the `TemplateDoesNotExist` error is eliminated.
- Templates render real data from the database because they reference actual model field names.
- Each template has a single purpose with no duplicated markup.

**What becomes harder or requires attention:**
- The original template content was fully replaced. Any in-progress front-end work based on the old markup must be re-applied against the new template structure.
- Future model field changes (e.g. renaming `condition_status`) now need updates in both the template and the view.

---

## ADR-3: Introduce Form Validation Through Django Generic Class-Based Views

**Date:** 2026-04-12

### Status

Accepted

### Context

The original codebase provided only two read-only views (`ListView` and `DetailView`). There was no browser-based way to create, edit, or delete a repair request — those operations required superuser access to the Django admin panel at `/admin/`. For a housing management system used by maintenance staff in remote communities, requiring admin credentials and navigating the admin UI is not practical.

Django offers generic class-based views (`CreateView`, `UpdateView`, `DeleteView`) that automatically generate HTML forms from model field definitions and enforce server-side validation (required fields, `max_length`, `choices`, etc.). They also include built-in CSRF protection via the `{% csrf_token %}` template tag.

### Alternatives Considered

| # | Alternative | Pros | Cons |
|---|------------|------|------|
| 1 | **Custom function-based views** with manually coded form handling (`request.POST`, `form.is_valid()`, etc.) | Full control over every validation step; no need to learn class-based view API | Significant boilerplate per view (~30–40 lines each); must manually wire CSRF, GET/POST branching, error rendering, and redirects; higher risk of omitting a validation check |
| 2 | **Django generic class-based views** (`CreateView`, `UpdateView`, `DeleteView`) with the `fields` attribute | Each view is ~5 lines of code; validation derives automatically from model field definitions; CSRF is built in; follows documented Django patterns | Less fine-grained control over form layout without a custom `ModelForm`; complex cross-field validation requires overriding `get_form()` or writing a separate form class |

### Decision

We chose **Alternative 2**. Three new views were added:

- **`RepairRequestCreateView`** — fields: `dwelling`, `tenant`, `title`, `description`, `category`, `priority`. On success redirects to `/` (`repairrequest-list`).
- **`RepairRequestUpdateView`** — fields: `title`, `description`, `category`, `priority`, `status`. On success redirects to `/`.
- **`RepairRequestDeleteView`** — renders a confirmation page; on POST deletes the object and redirects to `/`.

A single shared template (`repairrequest_form.html`) handles both create and edit, toggling its heading and button text based on whether `form.instance.pk` exists.

### Code Reference

| File | Lines | What changed |
|------|-------|--------------|
| `housing/views.py` | 42–47 | `RepairRequestCreateView` — fields and success URL |
| `housing/views.py` | 50–55 | `RepairRequestUpdateView` — fields and success URL |
| `housing/views.py` | 58–61 | `RepairRequestDeleteView` — template and success URL |
| `housing/urls.py` | 14 | `repairs/create/` route |
| `housing/urls.py` | 15 | `repairs/<int:pk>/edit/` route |
| `housing/urls.py` | 16 | `repairs/<int:pk>/delete/` route |
| `housing/templates/housing/repairrequest_form.html` | 10–17 | `<form method="post">` with `{% csrf_token %}` and `{{ form.as_table }}` |
| `housing/models.py` | 100–101 | `title` is `CharField(max_length=150)` — validation enforced automatically |
| `housing/models.py` | 102 | `description` is `TextField()` — required by default |

### Consequences

**What becomes easier:**
- Maintenance staff can create, edit, and delete repair requests through the browser without admin credentials.
- Server-side validation is automatic: empty required fields, values outside `choices`, and strings exceeding `max_length` are all rejected with clear error messages.
- CSRF protection is enforced on every POST, protecting against cross-site request forgery attacks.
- Code is minimal — three views totalling ~20 lines, easy to read and maintain.

**What becomes harder or requires attention:**
- The auto-generated form uses HTML `<table>` layout. A more polished UI will require either a custom `ModelForm` with widget overrides or a CSS/JS framework (e.g. Bootstrap, Tailwind).
- If cross-field validation is needed later (e.g. "urgent priority requires a tenant"), a custom `clean()` method must be added to a `ModelForm` subclass, which means migrating away from the `fields` shortcut on the view.
