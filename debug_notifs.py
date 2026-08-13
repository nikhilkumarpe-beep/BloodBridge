from app import app, db, User, Notification, BloodRequest

def debug_notifications():
    with app.app_context():
        # Check Users
        admin = User.query.filter_by(email='admin@gmail.com').first()
        ff = User.query.filter_by(email='ff@gmail.com').first()
        
        print("--- USERS ---")
        if admin:
            print(f"Admin: ID={admin.id}, Email={admin.email}, Blood={admin.blood_type}, IsDonor={admin.is_donor}")
        else:
            print("Admin user not found!")
            
        if ff:
            print(f"FF: ID={ff.id}, Email={ff.email}, Blood={ff.blood_type}")
        else:
            print("FF user not found!")

        # Check recent Blood Requests
        print("\n--- RECENT REQUESTS ---")
        requests = BloodRequest.query.order_by(BloodRequest.created_at.desc()).limit(3).all()
        for r in requests:
            print(f"Req ID={r.id}, Type={r.blood_type}, RequesterID={r.requester_id}, Status={r.status}")

        # Check Notifications for Admin
        if admin:
            print(f"\n--- NOTIFICATIONS FOR ADMIN (ID={admin.id}) ---")
            notifs = Notification.query.filter_by(user_id=admin.id).all()
            for n in notifs:
                print(f"Notif ID={n.id}, Msg='{n.message}', Read={n.is_read}")
        
        # Check all notifications count
        count = Notification.query.count()
        print(f"\nTotal Notifications in DB: {count}")

if __name__ == '__main__':
    debug_notifications()
