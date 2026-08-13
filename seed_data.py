import importlib.util
import sys
import os
from werkzeug.security import generate_password_hash
from datetime import datetime, date
import random
from sqlalchemy import text

# Import app.py directly to avoid conflict with 'app' package
spec = importlib.util.spec_from_file_location("app_module", "app.py")
app_module = importlib.util.module_from_spec(spec)
sys.modules["app_module"] = app_module
spec.loader.exec_module(app_module)

app = app_module.app
db = app_module.db
User = app_module.User
create_tables = app_module.create_tables

def seed_data():
    with app.app_context():
        print("Ensuring database tables exist...")
        create_tables()
        print("Seeding database with MASSIVE donor data...")
        
        # Bangalore Pincodes
        pincodes = [
            "560001", "560002", "560003", "560004", "560011", "560025", 
            "560034", "560038", "560043", "560061", "560066", "560078", "560085", 
            "560095", "560100", "560102", "560103"
        ]
        
        blood_types = ['A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-']
        
        first_names = ["Rahul", "Priya", "Amit", "Sneha", "Karthik", "Anjali", "Vikram", "Pooja", "Sanjay", "Divya", "Arjun", "Meera", "Rohan", "Kavya", "Suresh", "Lakshmi", "Manoj", "Vidya", "Deepak", "Rekha", "Vijay", "Swati", "Anand", "Geeta", "Rajesh", "Nithya", "Pradeep", "Shweta", "Ganesh", "Preeti"]
        last_names = ["Sharma", "Patel", "Singh", "Reddy", "Gowda", "Rao", "Kumar", "Nair", "Menon", "Iyer", "Prasad", "Joshi", "Das", "Shetty", "Babu", "Devi", "Patil", "Hegde", "Verma", "Gupta", "Krishna", "Deshpande", "Raj", "Kulkarni", "Pai", "Bhat", "Acharya", "Naik", "Shenoy", "Kamath"]
        
        areas = {
            "560001": "MG Road", "560002": "City Market", "560003": "Malleswaram", "560004": "Basavanagudi",
            "560011": "Jayanagar", "560025": "Richmond Town", "560034": "Koramangala", "560038": "Indiranagar",
            "560043": "Kalyan Nagar", "560061": "Subramanyapura", "560066": "Whitefield", "560078": "JP Nagar", "560085": "Banashankari",
            "560095": "Koramangala 6th Block", "560100": "Electronic City", "560102": "HSR Layout", "560103": "Bellandur"
        }

        count = 0
        for pincode in pincodes:
            area_name = areas.get(pincode, "Bangalore")
            for b_type in blood_types:
                # Create 4 donors per blood type per pincode
                for i in range(4):
                    f_name = random.choice(first_names)
                    l_name = random.choice(last_names)
                    email = f"{f_name.lower()}.{l_name.lower()}.{pincode}.{b_type.replace('+', 'pos').replace('-', 'neg')}.{i}@example.com"
                    
                    if not User.query.filter_by(email=email).first():
                        user = User(
                            first_name=f_name,
                            last_name=l_name,
                            email=email,
                            password=generate_password_hash('password123'),
                            phone=f"98{random.randint(10000000, 99999999)}",
                            blood_type=b_type,
                            date_of_birth=date(1980 + random.randint(0, 20), random.randint(1, 12), random.randint(1, 28)),
                            gender=random.choice(["Male", "Female"]),
                            address=f"{random.randint(1, 999)}, {area_name}",
                            city='Bangalore',
                            state='Karnataka',
                            postal_code=pincode,
                            country='India',
                            is_donor=True,
                            is_verified=True,
                            donation_count=random.randint(0, 15),
                            last_donation=datetime.now() if random.choice([True, False]) else None
                        )
                        db.session.add(user)
                        count += 1
        
        db.session.commit()
        print(f"Successfully added {count} new donors! Total donors covering all pincodes and blood types.")

        # Seed Blood Inventory
        print("Seeding Blood Inventory...")
        
        # Drop table to handle schema change
        try:
            db.session.execute(text('DROP TABLE IF EXISTS blood_inventory'))
            db.session.commit()
            print("Dropped old blood_inventory table.")
            create_tables()
            print("Recreated blood_inventory table.")
        except Exception as e:
            print(f"Error resetting table: {e}")

        BloodInventory = app_module.BloodInventory
        
        blood_banks = [
            "Rotary Bangalore TTK Blood Bank - Indiranagar",
            "Rashtrotthana Blood Bank - Jayanagar",
            "Lions Blood Bank - Malleswaram",
            "Red Cross Blood Bank - MG Road",
            "Victoria Hospital Blood Bank - City Market"
        ]
        
        for bank in blood_banks:
            for b_type in blood_types:
                if random.random() > 0.1: # 90% chance
                    inventory = BloodInventory(
                        blood_type=b_type,
                        blood_bank_name=bank,
                        units_available=random.randint(5, 50),
                        units_reserved=random.randint(0, 5),
                        target_level=100,
                        critical_level=10,
                        last_updated=datetime.now()
                    )
                    db.session.add(inventory)
        db.session.commit()
        print("Blood Inventory seeded successfully!")

if __name__ == '__main__':
    seed_data()
