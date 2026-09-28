# BloodBridge

A full-stack blood donation management platform that demonstrates practical backend engineering, relational database design, authentication, validation, and frontend integration.

**Stack:** Python · Flask · MySQL · SQLAlchemy · JavaScript

## What it demonstrates

- Donor registration and management workflows
- Blood-request creation and tracking
- Blood-bank inventory management
- Authentication and protected routes
- Password hashing and session management
- Server-side form validation
- SQLAlchemy ORM with MySQL
- Database migrations with Flask-Migrate
- Environment-based configuration
- Email, upload, CORS, and JWT integrations

## Architecture

```text
Browser
   │
   ▼
HTML / CSS / JavaScript / Jinja2
   │
   ▼
Flask application
   ├── Authentication
   ├── Validation
   ├── Business logic
   └── Application routes
   │
   ▼
SQLAlchemy ORM
   │
   ▼
MySQL
```

## Tech stack

| Layer | Technologies |
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

## Project structure

```text
BloodBridge/
├── run.py
├── app.py                 # Legacy entry point; use run.py
├── config.py
├── requirements.txt
├── app/
│   ├── static/
│   └── templates/
├── .env.example
├── .gitignore
└── README.md
```

## Run locally

### 1. Clone

```bash
git clone https://github.com/nikhilkumarpe-beep/BloodBridge.git
cd BloodBridge
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

Windows:

```powershell
.venv\Scripts\Activate.ps1
```

macOS/Linux:

```bash
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure the environment

Copy `.env.example` to `.env` and provide your local MySQL and mail configuration.

Never commit real credentials.

### 5. Start the application

```bash
python run.py
```

The application factory is exposed by `run.py`. The project expects a configured MySQL database; create the database first and configure `DATABASE_URL` in `.env`. Use `python run.py` for local development. Do not expose Flask's debug server to the public internet.

## Engineering highlights

- CRUD-oriented application workflows
- Relational data modelling
- ORM-based database access
- Authentication and authorization
- Server-side validation
- Secure password storage
- Environment-based secrets
- Frontend/backend integration
- Production-oriented deployment configuration

## Security

- Secrets are loaded from environment variables.
- Passwords are hashed before storage.
- `.env` files are excluded from version control.
- Upload size and file-extension controls are implemented.
- Production deployments should use HTTPS, secure cookie settings, strong secrets, and a managed database.

## Roadmap

- Automated unit and integration tests
- Role-based dashboards
- Improved donor matching
- Docker-based development
- GitHub Actions CI
- Production monitoring and logging

## Author

**Nikhil Kumar PE**  
Computer Science Engineering · Python · Backend Development · AI/ML

[GitHub](https://github.com/nikhilkumarpe-beep)
