import sys
import traceback

def log(msg):
    with open('db_log.txt', 'a') as f:
        f.write(msg + '\n')

try:
    from app import app, db, User
    from werkzeug.security import generate_password_hash
    import datetime

    log("Starting add_donors_mysql.py")

    with app.app_context():
        log("Inside app context")
        
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
                address='Subramanyapura, Bangalore',
                postal_code='560061',
                date_of_birth=datetime.date(1995, 1, 1),
                last_donation=datetime.datetime.now() - datetime.timedelta(days=100)
            )
            db.session.add(d1)
            log("Added Prajwal B")
        else:
            d1.postal_code = '560061'
            d1.address = 'Subramanyapura, Bangalore'
            log("Updated Prajwal B")

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
                address='Subramanyapura, Bangalore',
                postal_code='560061',
                date_of_birth=datetime.date(1990, 1, 1),
                last_donation=datetime.datetime.now() - datetime.timedelta(days=200)
            )
            db.session.add(d2)
            log("Added Poonamlal")
        else:
            d2.postal_code = '560061'
            d2.address = 'Subramanyapura, Bangalore'
            log("Updated Poonamlal")

        db.session.commit()
        log("Commit successful")

except Exception as e:
    log(f"Error: {str(e)}")
    log(traceback.format_exc())
