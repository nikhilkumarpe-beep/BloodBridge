from app import app, db, User, BloodRequest, Notification
import datetime

def notify_existing_request():
    with app.app_context():
        # 1. Get Users
        admin = User.query.filter_by(email='admin@gmail.com').first()
        ff = User.query.filter_by(email='ff@gmail.com').first()

        if not admin or not ff:
            print("Users not found.")
            return

        # 2. Find the LAST request made by ff@gmail.com
        last_req = BloodRequest.query.filter_by(requester_id=ff.id).order_by(BloodRequest.created_at.desc()).first()
        
        if not last_req:
            print("No blood requests found for ff@gmail.com")
            return

        print(f"Found Request: Patient={last_req.patient_name}, Units={last_req.units_required}, Type={last_req.blood_type}")

        # 3. Clear Admin Notifications
        Notification.query.filter_by(user_id=admin.id).delete()
        
        # 4. Create Notification for THIS request
        msg = f"{last_req.patient_name} has requested {last_req.units_required} units of blood. Contact {last_req.contact_phone} if you are interested in donating."
        
        notif = Notification(
            user_id=admin.id,
            message=msg,
            is_read=False,
            created_at=datetime.datetime.now()
        )
        db.session.add(notif)
        db.session.commit()
        print(f"Notification sent to Admin: {msg}")

if __name__ == '__main__':
    notify_existing_request()
