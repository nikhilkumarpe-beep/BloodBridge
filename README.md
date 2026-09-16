# BloodBridge

BloodBridge is a blood donation management web application I built using Flask and MySQL. The idea was to bring donor details, blood requests and basic blood-bank management into one place.

## What it does

- User signup and login
- Donor registration and donor details
- Create and manage blood requests
- Store blood-group and inventory information
- MySQL database integration using SQLAlchemy
- Password hashing and protected routes
- Image upload support
- Email configuration through environment variables
- Database migrations with Flask-Migrate

## Built with

- Python
- Flask
- SQLAlchemy
- MySQL
- HTML / CSS / JavaScript
- Jinja2
- Flask-Login
- Flask-Migrate
- PyMySQL

## Project structure

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

## Running it locally

Clone the project:

```bash
git clone https://github.com/nikhilkumarpe-beep/BloodBridge.git
cd BloodBridge
```

Create and activate a virtual environment:

```bash
python -m venv venv
venv\Scripts\activate
```

Install the required packages:

```bash
pip install -r requirements.txt
```

Create a `.env` file with your own database and application settings. For example:

```env
SECRET_KEY=your-secret-key
JWT_SECRET_KEY=your-jwt-secret
DATABASE_URL=mysql+pymysql://username:password@localhost/blood_donation_system
MAIL_USERNAME=your-email
MAIL_PASSWORD=your-mail-password
MAIL_DEFAULT_SENDER=your-email
```

Then run:

```bash
python app.py
```

## A few things I learned from this project

This project gave me hands-on experience with Flask routing, forms, authentication, database models, CRUD operations, MySQL and connecting a frontend to a Python backend. It also helped me understand why application credentials should be kept outside the source code.

## Things I want to improve

- Add proper automated tests
- Improve the API structure
- Add better role-based dashboards
- Containerize the application
- Deploy it with proper logging and monitoring

## Author

Nikhil Kumar PE

Computer Science Engineering student | Python | Web Development | AI/ML
