from app import app, db, User, Notification
import datetime

def reset_and_notify():
    with app.app_context():
        # Get Admin User
        admin = User.query.filter_by(email='admin@gmail.com').first()
        if not admin:
            print("Admin user not found!")
            return

        # Delete ALL existing notifications for admin to clear confusion
        Notification.query.filter_by(user_id=admin.id).delete()
        
        # Create the specific notification the user wants to see
        # Simulating a request from "Priya" (Patient)
        msg = "Priya has requested 2 units of blood. Contact 9876543210 if you are interested in donating."
        
        notif = Notification(
            user_id=admin.id,
            message=msg,
            is_read=False,
            created_at=datetime.datetime.now()
        )
        
        db.session.add(notif)
        db.session.commit()
        print(f"Cleared old notifications and added new alert for {admin.email}")

if __name__ == '__main__':
    reset_and_notify()
