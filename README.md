# BloodBridge

A Flask + MySQL web application for managing blood donors, blood requests, and blood-bank inventory in one place.

> A practical full-stack project focused on authentication, database design, CRUD workflows, and connecting a web frontend to a Python backend.

## Highlights

- Donor registration and donor information management
- Blood-request creation and management
- Blood-group and inventory tracking
- User authentication with protected routes
- Password hashing
- MySQL database integration with SQLAlchemy
- Database migrations with Flask-Migrate
- Image upload support
- Email configuration through environment variables
- CORS and JWT support for application/API integration

## Tech Stack

| Layer | Technologies |
|---|---|
| Backend | Python, Flask |
| Database | MySQL, SQLAlchemy, PyMySQL |
| Frontend | HTML, CSS, JavaScript, Jinja2 |
| Authentication | Flask-Login, Flask-Bcrypt, JWT |
| Forms & Validation | Flask-WTF, WTForms, email-validator |
| Database Migration | Flask-Migrate |
| Utilities | python-dotenv, requests, geopy |
| Deployment | Gunicorn |

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

On macOS/Linux:

```bash
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file using `.env.example` as the template. Keep real credentials out of Git.

Example:

```env
SECRET_KEY=your-secret-key
JWT_SECRET_KEY=your-jwt-secret
DATABASE_URL=mysql+pymysql://username:password@localhost/blood_donation_system
MAIL_USERNAME=your-email
MAIL_PASSWORD=your-mail-password
MAIL_DEFAULT_SENDER=your-email
```

### 5. Start the application

```bash
python app.py
```

## What I Learned

Building BloodBridge gave me hands-on experience with:

- Flask application structure and routing
- Authentication and protected routes
- SQLAlchemy models and CRUD operations
- MySQL database integration
- Form handling and validation
- Environment-based configuration
- Database migrations
- Connecting frontend interfaces to a Python backend

## Future Improvements

- Add automated unit and integration tests
- Introduce a cleaner REST API structure
- Add role-based dashboards for different users
- Improve search and donor-matching workflows
- Containerize the application with Docker
- Add CI/CD and production monitoring
- Deploy the application with production-ready configuration

## Author

**Nikhil Kumar PE**  
Computer Science Engineering student | Python | Web Development | AI/ML
