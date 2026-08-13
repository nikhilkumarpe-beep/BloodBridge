from app import app, db, User

def check_admin():
    with app.app_context():
        u = User.query.filter_by(email='admin@gmail.com').first()
        if u:
            print(f"Admin: {u.email}, Blood: {u.blood_type}, IsDonor: {u.is_donor}")
            if not u.is_donor:
                print("Admin is NOT a donor. Setting is_donor=True...")
                u.is_donor = True
                db.session.commit()
                print("Admin is now a donor.")
        else:
            print("Admin user not found.")

if __name__ == '__main__':
    check_admin()
