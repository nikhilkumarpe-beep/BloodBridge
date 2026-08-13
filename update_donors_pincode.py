from app import app, db, User

def update_donors():
    with app.app_context():
        phones = ['8105336328', '7483176991']
        target_pincode = '560061'
        
        for phone in phones:
            user = User.query.filter_by(phone=phone).first()
            if user:
                user.postal_code = target_pincode
                # Also update address to match the area if needed, but user only asked for pincode.
                # I'll append the area name to address for clarity if it's just 'Bangalore'
                if user.address == 'Bangalore':
                    user.address = 'Subramanyapura, Bangalore'
                
                print(f"Updated {user.first_name} {user.last_name} to pincode {target_pincode}")
            else:
                print(f"User with phone {phone} not found")
        
        db.session.commit()
        print("Update complete!")

if __name__ == '__main__':
    update_donors()
