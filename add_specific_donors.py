from app import app, db, User
from werkzeug.security import generate_password_hash
import datetime

def add_donors():
    with app.app_context():
        # Donor 1: Prajwal B
        d1 = User.query.filter_by(phone='8105336328').first()
        if not d1:
            d1 = User(
                first_name='Prajwal',
                last_name='B',
                email='prajwal.b@example.com',
                password=generate_password_hash('password123'),
                phone='8105336328',
                blood_type='A+',
                is_donor=True,
                city='Bangalore',
                address='Bangalore',
                postal_code='560001',
                date_of_birth=datetime.date(1995, 1, 1),
                last_donation=datetime.datetime.now() - datetime.timedelta(days=100)
            )
            db.session.add(d1)
            print("Added Prajwal B")
        else:
            print("Prajwal B already exists")

        # Donor 2: Poonamlal
        d2 = User.query.filter_by(phone='7483176991').first()
        if not d2:
            d2 = User(
                first_name='Poonamlal',
                last_name='',
                email='poonamlal@example.com',
                password=generate_password_hash('password123'),
                phone='7483176991',
                blood_type='A+',
                is_donor=True,
                city='Bangalore',
                address='Bangalore',
                postal_code='560001',
                date_of_birth=datetime.date(1990, 1, 1),
                last_donation=datetime.datetime.now() - datetime.timedelta(days=200)
            )
            db.session.add(d2)
            print("Added Poonamlal")
        else:
            print("Poonamlal already exists")

        db.session.commit()
        print("Done!")

if __name__ == '__main__':
    add_donors()
