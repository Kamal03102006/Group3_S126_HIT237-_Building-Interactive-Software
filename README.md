# Indigenous Housing Management System — Group 3

## Project Overview
A Django web application for managing indigenous community housing, dwellings, tenants, and repair/maintenance requests. The system allows users to view available houses, submit repair requests, track request status, and manage maintenance updates.

## Features
- **Dwelling Management** — View a list of all houses with details (house code, address, community, bedrooms, condition status).
- **Repair Request CRUD** — Create, view, update, and delete repair requests through the browser.
- **Repair Request Tracking** — Each request tracks category (plumbing, electrical, roofing, etc.), priority (low to urgent), and status (reported → in progress → completed).
- **Maintenance Updates** — Timestamped notes attached to repair requests to record progress.
- **Admin Panel** — Full Django admin interface for managing Communities, Dwellings, Tenants, Repair Requests, and Maintenance Updates.

## Technologies Used
| Technology | Version | Purpose |
|------------|---------|---------|
| Python     | 3.9+    | Programming language |
| Django     | 4.2.29  | Web framework |
| SQLite 3   | —       | Development database |
| HTML       | 5       | Templates / frontend |

## Project Structure
```
Group3_Django_Project/
├── config/                # Django project configuration
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── housing/               # Main application
│   ├── models.py          # Community, Dwelling, Tenant, RepairRequest, MaintenanceUpdate
│   ├── views.py           # List, Detail, Create, Update, Delete views
│   ├── urls.py            # URL routing for the housing app
│   ├── admin.py           # Admin panel configuration
│   └── templates/housing/ # HTML templates
│       ├── house_list.html
│       ├── request_list.html
│       ├── repairrequest_detail.html
│       ├── repairrequest_form.html
│       └── repairrequest_confirm_delete.html
├── manage.py
├── requirements.txt
├── testing.md             # Test cases and results
├── ADR.md                 # Architecture Decision Records
└── README.md
```

## Steps to Run the Project

### 1. Clone the Repository
```bash
git clone https://github.com/Kamal03102006/Group3_S126_HIT237-_Building-Interactive-Software.git
cd Group3_S126_HIT237-_Building-Interactive-Software
```

### 2. Create a Virtual Environment (recommended)
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install django==4.2.29 sqlparse asgiref
```

### 4. Run Migrations
```bash
python manage.py migrate
```

### 5. Create a Superuser (for admin access)
```bash
python manage.py createsuperuser
```

### 6. Start the Development Server
```bash
python manage.py runserver
```

### 7. Access the Application
| Page | URL |
|------|-----|
| Repair Requests (Home) | http://127.0.0.1:8000/ |
| Dwelling List | http://127.0.0.1:8000/houses/ |
| New Repair Request | http://127.0.0.1:8000/repairs/create/ |
| Admin Panel | http://127.0.0.1:8000/admin/ |
