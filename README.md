# BloodBridge

A web-based blood donation management platform built with Flask and MySQL to help manage donors, blood requests, and blood-bank workflows in one place.

## Overview

BloodBridge is a full-stack academic/project application focused on making blood donation coordination easier to manage. It provides authentication, donor management, blood requests, database-backed records, and email-related configuration.

## Key Features

- User authentication and protected application routes
- Donor registration and donor record management
- Blood request management
- Blood-group based data handling
- MySQL database integration with SQLAlchemy
- Secure password hashing
- File upload support for approved image formats
- Email configuration through environment variables
- Database migration support with Flask-Migrate
- Responsive web interface using HTML/CSS templates

## Tech Stack

**Backend:** Python, Flask

**Database:** MySQL, SQLAlchemy

**Authentication & Security:** Flask-Login, password hashing, JWT support

**Frontend:** HTML, CSS, JavaScript, Jinja2

**Other:** Flask-Migrate, PyMySQL, python-dotenv, Gunicorn

## Project Structure

```text
BloodBridge/
├── app.py
├── config.py
├── requirements.txt
├── app/
│   ├── static/
│   └── templates/
└── README.md
```

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/nikhilkumarpe-beep/BloodBridge.git
cd BloodBridge
```

### 2. Create a virtual environment

```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file and provide your own application secrets and database credentials. Never commit real passwords or secret keys.

Example:

```env
SECRET_KEY=change-me
JWT_SECRET_KEY=change-me
DATABASE_URL=mysql+pymysql://username:password@localhost/blood_donation_system
MAIL_USERNAME=your-email
MAIL_PASSWORD=your-mail-password
MAIL_DEFAULT_SENDER=your-email
```

### 5. Start the application

```bash
python app.py
```

## Security Note

Secrets and database credentials should always be stored in environment variables. If a credential has ever been committed to a public repository, rotate it immediately and consider removing the exposed secret from Git history.

## Learning Outcomes

This project demonstrates practical experience with:

- Building a Flask web application
- Designing database-backed features
- Authentication and authorization
- CRUD-style application workflows
- Environment-based configuration
- Python backend development
- Integrating frontend templates with a backend API/application

## Future Improvements

- Automated tests and CI/CD
- Docker-based deployment
- Production database configuration
- Improved API documentation
- Role-based dashboards for donors, hospitals, and administrators
- Deployment with monitoring and logging

## Author

**Nikhil Kumar PE**

Computer Science Engineering student | Python | Flask | Web Development | AI/ML
