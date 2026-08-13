from app import app, db, User, BloodRequest, Notification
import datetime

def setup_demo():
    with app.app_context():
        # 1. Get Users
        admin = User.query.filter_by(email='admin@gmail.com').first()
        ff = User.query.filter_by(email='ff@gmail.com').first()

        if not admin:
            print("Error: admin@gmail.com not found.")
            return
        if not ff:
            print("Error: ff@gmail.com not found.")
            return

        print(f"Found Admin: {admin.first_name} (ID: {admin.id})")
        print(f"Found FF: {ff.first_name} (ID: {ff.id})")

        # 2. Ensure Admin is a Donor and has A+ blood (to match the request)
        if not admin.is_donor:
            admin.is_donor = True
            print("Updated Admin to be a donor.")
        
        # Force Admin to A+ for this demo to ensure matching
        admin.blood_type = 'A+'
        db.session.add(admin)

        # 3. Create the Blood Request from FF
        # Check if one exists recently to avoid duplicates, or just create a new one
        req = BloodRequest(
            requester_id=ff.id,
            patient_name="Demo Patient",
            blood_type="A+",
            units_required=2,
            required_by=datetime.datetime.now() + datetime.timedelta(days=2),
            hospital_name="City Hospital",
            hospital_address="123 Main St",
            city="Bangalore",
            contact_name=ff.first_name,
            contact_phone=ff.phone,
            status="Open",
            created_at=datetime.datetime.now()
        )
        db.session.add(req)
        print("Created new Blood Request from ff@gmail.com")

        # 4. CLEANUP: Delete ALL existing notifications for Admin
        # This fixes the "stuck old message" issue
        deleted = Notification.query.filter_by(user_id=admin.id).delete()
        print(f"Deleted {deleted} old notifications for Admin.")

        # 5. Create the specific Notification for Admin
        # Using the format the user requested
        msg = f"{req.patient_name} has requested {req.units_required} units of blood. Contact {req.contact_phone} if you are interested in donating."
        
        notif = Notification(
            user_id=admin.id,
            message=msg,
            is_read=False,
            created_at=datetime.datetime.now()
        )
        db.session.add(notif)
        print(f"Created new Notification for Admin: '{msg}'")

        db.session.commit()
        print("SUCCESS: Demo scenario setup complete!")
        
        # Verify
        print("\n--- VERIFICATION ---")
        notifs = Notification.query.filter_by(user_id=admin.id).all()
        print(f"Admin has {len(notifs)} notifications:")
        for n in notifs:
            print(f"- [{n.created_at}] Read={n.is_read}: {n.message}")

if __name__ == '__main__':
    setup_demo()
