from app import app, db, User, Notification
import datetime

def fix_and_test():
    with app.app_context():
        # 1. Find Admin
        admin = User.query.filter_by(email='admin@gmail.com').first()
        if not admin:
            print("Admin not found")
            return

        # 2. Check current notifications
        print(f"--- Current Notifications for {admin.email} ---")
        notifs = Notification.query.filter_by(user_id=admin.id).order_by(Notification.created_at.desc()).limit(5).all()
        for n in notifs:
            print(f"ID: {n.id} | Read: {n.is_read} | Msg: {n.message}")

        # 3. Mark all as read manually to verify DB works
        print("\n--- Marking all as read via Python ---")
        unread_count = Notification.query.filter_by(user_id=admin.id, is_read=False).update({'is_read': True})
        db.session.commit()
        print(f"Marked {unread_count} notifications as read.")

        # 4. Create a NEW test notification with the NEW format
        print("\n--- Creating a TEST notification with NEW format ---")
        new_notif = Notification(
            user_id=admin.id,
            message="TEST PATIENT has requested 2 units of blood. Contact 9999999999 if you are interested in donating.",
            is_read=False,
            created_at=datetime.datetime.now()
        )
        db.session.add(new_notif)
        db.session.commit()
        print("Test notification created.")

if __name__ == '__main__':
    fix_and_test()
