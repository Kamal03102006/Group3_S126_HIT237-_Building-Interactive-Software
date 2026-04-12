# Testing Document — Group 3 Indigenous Housing Management System

## Test Environment
- **Framework:** Django 4.2.29
- **Database:** SQLite 3 (development)
- **Python:** 3.14
- **Server:** Django development server (`manage.py runserver`)

---

## Test Cases

### TC-01: Home Page (Repair Request List) Loads Successfully
| Field            | Details |
|------------------|---------|
| **Input**        | Navigate to `http://127.0.0.1:8000/` |
| **Expected Output** | Page displays "Repair Requests" heading with a table of repair requests (or an empty-state message). Navigation links to Houses and "Submit New Request" are visible. |
| **Actual Output** | Page loads with status 200. Heading, table, and navigation links render correctly. |
| **Status**       | **Pass** |

---

### TC-02: Dwelling List Page Loads Successfully
| Field            | Details |
|------------------|---------|
| **Input**        | Navigate to `http://127.0.0.1:8000/houses/` |
| **Expected Output** | Page displays "Available Houses" heading with a table showing house code, address, community, bedrooms, and condition. |
| **Actual Output** | Page loads with status 200. Table columns render correctly. Empty-state message shown when no data exists. |
| **Status**       | **Pass** |

---

### TC-03: Repair Request Detail Page
| Field            | Details |
|------------------|---------|
| **Input**        | Create a RepairRequest via Django admin, then navigate to `http://127.0.0.1:8000/repairs/1/` |
| **Expected Output** | Page displays the repair request title, dwelling, tenant, category, priority, status, description, and timestamps. Maintenance updates section is shown. |
| **Actual Output** | Detail page renders all fields correctly with status 200. |
| **Status**       | **Pass** |

---

### TC-04: Repair Request Detail — Non-Existent ID Returns 404
| Field            | Details |
|------------------|---------|
| **Input**        | Navigate to `http://127.0.0.1:8000/repairs/9999/` |
| **Expected Output** | Server responds with HTTP 404 Not Found. |
| **Actual Output** | Django returns a 404 error page. |
| **Status**       | **Pass** |

---

### TC-05: Create Repair Request — Valid Form Submission
| Field            | Details |
|------------------|---------|
| **Input**        | Navigate to `http://127.0.0.1:8000/repairs/create/`. Fill all required fields (dwelling, title, description, category, priority) and submit. |
| **Expected Output** | Form submits successfully. User is redirected to the repair request list page. New request appears in the table. |
| **Actual Output** | POST succeeds with 302 redirect to `/`. New repair request visible in list. |
| **Status**       | **Pass** |

---

### TC-06: Create Repair Request — Empty Required Fields (Form Validation)
| Field            | Details |
|------------------|---------|
| **Input**        | Navigate to `http://127.0.0.1:8000/repairs/create/`. Leave the title and description fields empty and submit. |
| **Expected Output** | Form does not submit. Validation errors are displayed for required fields (title, description, dwelling, category). |
| **Actual Output** | Form re-renders with validation errors: "This field is required" shown next to each empty required field. |
| **Status**       | **Pass** |

---

### TC-07: Update Repair Request — Change Status
| Field            | Details |
|------------------|---------|
| **Input**        | Navigate to `http://127.0.0.1:8000/repairs/1/edit/`. Change the status field from "Reported" to "In Progress" and submit. |
| **Expected Output** | Form submits successfully. User is redirected to the list page. The request's status is updated to "In Progress". |
| **Actual Output** | POST succeeds with 302 redirect. Status updated in both the list and detail views. |
| **Status**       | **Pass** |

---

### TC-08: Update Repair Request — Form Validation on Edit
| Field            | Details |
|------------------|---------|
| **Input**        | Navigate to `http://127.0.0.1:8000/repairs/1/edit/`. Clear the title field and submit. |
| **Expected Output** | Form does not submit. Validation error shown for the title field. |
| **Actual Output** | Form re-renders with "This field is required" error on the title field. |
| **Status**       | **Pass** |

---

### TC-09: Delete Repair Request — Confirmation and Deletion
| Field            | Details |
|------------------|---------|
| **Input**        | Navigate to `http://127.0.0.1:8000/repairs/1/delete/`. Confirm deletion by clicking "Yes, delete". |
| **Expected Output** | Request is deleted. User is redirected to the list page. The deleted request no longer appears. |
| **Actual Output** | POST succeeds with 302 redirect. Request removed from list. |
| **Status**       | **Pass** |

---

### TC-10: Delete Repair Request — Cancel Returns to Detail
| Field            | Details |
|------------------|---------|
| **Input**        | Navigate to `http://127.0.0.1:8000/repairs/1/delete/`. Click "Cancel" instead of confirming. |
| **Expected Output** | User is taken back to the repair request detail page. The request is not deleted. |
| **Actual Output** | Cancel link navigates to detail page. Request still exists. |
| **Status**       | **Pass** |

---

### TC-11: Navigation — Links Between Pages Work Correctly
| Field            | Details |
|------------------|---------|
| **Input**        | From the repair request list page, click "View Houses". From the houses page, click "View Repair Requests". From the list, click a request title to view details. From details, click "Back to Requests". |
| **Expected Output** | All navigation links resolve correctly and load the expected pages without 404 errors. |
| **Actual Output** | All links work. Pages load with HTTP 200. |
| **Status**       | **Pass** |

---

### TC-12: Admin Panel — Model Registration
| Field            | Details |
|------------------|---------|
| **Input**        | Navigate to `http://127.0.0.1:8000/admin/` and log in with superuser credentials. |
| **Expected Output** | Admin panel shows registered models: Community, Dwelling, Tenant, RepairRequest, MaintenanceUpdate. Each model has list display, search, and filter configurations. |
| **Actual Output** | All five models appear in admin. List display columns, search fields, and filters work as configured in `admin.py`. |
| **Status**       | **Pass** |

---

### TC-13: URL Routing — Invalid URL Returns 404
| Field            | Details |
|------------------|---------|
| **Input**        | Navigate to `http://127.0.0.1:8000/nonexistent-page/` |
| **Expected Output** | Server responds with HTTP 404 Not Found. |
| **Actual Output** | Django returns 404 error page. |
| **Status**       | **Pass** |

---

### TC-14: CSRF Protection on Forms
| Field            | Details |
|------------------|---------|
| **Input**        | Attempt a POST request to `http://127.0.0.1:8000/repairs/create/` without a CSRF token (e.g., via curl). |
| **Expected Output** | Server responds with HTTP 403 Forbidden. |
| **Actual Output** | Django returns 403 Forbidden with "CSRF verification failed" message. |
| **Status**       | **Pass** |

---

## Summary

| Total Tests | Passed | Failed |
|-------------|--------|--------|
| 14          | 14     | 0      |

All pages load successfully, form validation works on both create and update views, CRUD operations function correctly, navigation links are properly connected, and Django's CSRF protection is enforced.
