# BloodBridge

A full-stack blood donation management platform designed to connect donors, blood requests, and blood-bank inventory through a structured web application.

> **Built with:** Python · Flask · MySQL · SQLAlchemy · JavaScript

## Overview

BloodBridge is a practical web application built around a real-world healthcare coordination workflow. It provides a centralized system for donor registration, blood-request management, and inventory tracking while demonstrating backend development, relational database design, authentication, validation, and frontend-backend integration.

The project focuses on building a maintainable application: configuration is environment-based, database access is modeled through SQLAlchemy, migrations are supported through Flask-Migrate, and authenticated routes protect application workflows.

## Key Features

- **Donor Management** — registration and donor information workflows
- **Blood Requests** — create and manage requests based on blood-group requirements
- **Inventory Management** — track blood-group stock and availability
- **Authentication** — session-based authentication, protected routes, and password hashing
- **Database Integration** — MySQL with SQLAlchemy and PyMySQL
- **Validation** — Flask-WTF, WTForms, and email validation
- **Migrations** — database schema management with Flask-Migrate
- **Application Services** — email configuration, image uploads, CORS, and JWT support
- **Environment Configuration** — secrets and deployment configuration kept outside source code

## Architecture

```text
Browser
   │
   ▼
HTML / CSS / JavaScript / Jinja2
   │
   ▼
Flask Application
   │
   ├── Authentication & Authorization
   ├── Form Validation
   ├── Business Logic
   └── Application Routes
   │
   ▼
SQLAlchemy ORM
   │
   ▼
MySQL Database
```

## Tech Stack

| Area | Technologies |
|---|---|
| Language | Python, JavaScript |
| Backend | Flask |
| Frontend | HTML5, CSS3, JavaScript, Jinja2 |
| Database | MySQL, SQLAlchemy, PyMySQL |
| Authentication | Flask-Login, Flask-Bcrypt, JWT |
| Forms | Flask-WTF, WTForms, email-validator |
| Migrations | Flask-Migrate |
| Utilities | python-dotenv, requests, geopy |
| Server | Gunicorn |

## Project Structure

```text
BloodBridge/
├── app.py
├── config.py
├── requirements.txt
├── app/
│   ├── static/
│   └── templates/
├── .env.example
├── .gitignore
└── README.md
```

## Getting Started

### 1. Clone

```bash
git clone https://github.com/nikhilkumarpe-beep/BloodBridge.git
cd BloodBridge
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

Windows:

```bash
venv\Scripts\activate
```

macOS/Linux:

```bash
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create `.env` from `.env.example` and provide your local configuration. Never commit real credentials.

```env
SECRET_KEY=your-secret-key
JWT_SECRET_KEY=your-jwt-secret
DATABASE_URL=mysql+pymysql://username:password@localhost/blood_donation_system
MAIL_USERNAME=your-email
MAIL_PASSWORD=your-mail-password
MAIL_DEFAULT_SENDER=your-email
```

### 5. Run

```bash
python app.py
```

## Engineering Concepts Demonstrated

- Flask application structure and routing
- Authentication and protected routes
- CRUD operations and relational data modeling
- SQLAlchemy ORM and MySQL integration
- Form handling and server-side validation
- Password hashing and session management
- Database migrations
- Environment-based configuration
- Frontend/backend integration
- API-oriented capabilities with JWT and CORS

## Security Notes

- Secrets are loaded through environment variables rather than hard-coded credentials.
- Passwords are hashed before storage.
- `.env` files should remain local and must not be committed.
- Production deployments should use HTTPS, secure cookie settings, strong secret keys, and a production database configuration.

## Roadmap

- Add automated unit and integration tests
- Introduce a cleaner REST API layer
- Add role-based dashboards
- Improve donor matching and search workflows
- Containerize with Docker
- Add CI/CD with GitHub Actions
- Deploy with production-ready monitoring and logging

## Author

**Nikhil Kumar PE**  
Computer Science Engineering Student · Python · Web Development · AI/ML

[GitHub](https://github.com/nikhilkumarpe-beep)
