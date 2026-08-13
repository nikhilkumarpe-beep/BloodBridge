import importlib.util
import sys
import os

# Import app.py directly
spec = importlib.util.spec_from_file_location("app_module", "app.py")
app_module = importlib.util.module_from_spec(spec)
sys.modules["app_module"] = app_module
spec.loader.exec_module(app_module)

app = app_module.app
db = app_module.db
User = app_module.User

def check_db():
    with app.app_context():
        # Check for specific donors
        phones = ['8105336328', '7483176991']
        for p in phones:
            u = User.query.filter_by(phone=p).first()
            if u:
                print(f"Found {u.first_name} {u.last_name} - Phone: {u.phone}, Blood: {u.blood_type}, Pincode: {u.postal_code}, IsDonor: {u.is_donor}")
            else:
                print(f"Not found: {p}")

        # Check pincodes
        pincodes = db.session.query(User.postal_code).distinct().all()
        print("Available pincodes:", [p[0] for p in pincodes])
        
        count = User.query.count()
        print(f"Total users: {count}")

if __name__ == '__main__':
    check_db()
