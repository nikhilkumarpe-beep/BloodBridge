from setuptools import setup, find_packages

setup(
    name="blood_donation_system",
    version="1.0.0",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'Flask==2.3.3',
        'Flask-SQLAlchemy==3.1.1',
        'Flask-Migrate==4.0.5',
        'Flask-JWT-Extended==4.5.2',
        'Flask-Cors==4.0.0',
        'Flask-Bcrypt==1.0.1',
        'python-dotenv==1.0.0',
        'PyMySQL==1.1.0',
        'email-validator==2.0.0',
        'python-dateutil==2.8.2',
        'geopy==2.3.0',
        'requests==2.31.0',
        'python-jose==3.3.0',
        'PyJWT==2.8.0',
        'gunicorn==21.2.0'
    ],
    python_requires='>=3.8',
)
