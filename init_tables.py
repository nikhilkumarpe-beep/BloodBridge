from app import app, db

def init_tables():
    with app.app_context():
        print("Creating database tables...")
        try:
            db.create_all()
            print("Tables created successfully!")
        except Exception as e:
            print(f"Error creating tables: {e}")

if __name__ == "__main__":
    init_tables()
