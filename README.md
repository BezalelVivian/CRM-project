# CRM Web App — FastAPI + MySQL

A clean CRM application for managing clients/leads with:

- Create, read, update and delete clients
- Client name, date, email, phone, company, budget, status, source and notes
- Statuses: Lead, Prospect, Customer, Churned
- Search and status filtering
- Dashboard KPIs
- Analysis dashboard with charts
- MySQL database
- FastAPI backend
- Server-rendered HTML with Jinja2
- Responsive CSS
- No React

## 1. Create the MySQL database

Open MySQL and run:

```sql
CREATE DATABASE crm_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

## 2. Create and activate a virtual environment

Windows:

```bash
python -m venv .venv
.venv\Scripts\activate
```

## 3. Install packages

```bash
pip install -r requirements.txt
```

## 4. Configure environment

Copy `.env.example` to `.env` and change the MySQL username/password.

Example:

```env
DATABASE_URL=mysql+pymysql://root:password@localhost:3306/crm_db
```

If your MySQL user has no password:

```env
DATABASE_URL=mysql+pymysql://root:@localhost:3306/crm_db
```

## 5. Run

```bash
uvicorn app.main:app --reload
```

Open:

http://127.0.0.1:8000

The application automatically creates the `clients` table.

## Project structure

```text
crm_app/
├── app/
│   ├── __init__.py
│   ├── database.py
│   ├── main.py
│   ├── models.py
│   ├── schemas.py
│   ├── crud.py
│   ├── templates/
│   │   ├── base.html
│   │   ├── dashboard.html
│   │   ├── clients.html
│   │   ├── client_form.html
│   │   └── analysis.html
│   └── static/
│       ├── css/style.css
│       └── js/app.js
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
```

## API

The UI uses these FastAPI endpoints:

- `GET /api/clients`
- `POST /api/clients`
- `PUT /api/clients/{client_id}`
- `DELETE /api/clients/{client_id}`
- `GET /api/analytics`

Swagger docs:

http://127.0.0.1:8000/docs
