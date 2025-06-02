from sqlalchemy import create_engine
from src.models import Base, User, SessionLocal
from werkzeug.security import generate_password_hash
import os

def create_tables():
    """Create all database tables"""
    DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://username:password@localhost/scaling_spork_db')
    engine = create_engine(DATABASE_URL)
    Base.metadata.create_all(bind=engine)
    print("Tables created successfully!")

def add_test_data():
    """Add test data to the database"""
    db = SessionLocal()

    try:
        # Check if test users already exist
        existing_user = db.query(User).filter(User.username == 'admin').first()
        if existing_user:
            print("Test data already exists!")
            return

        # Create test users
        test_users = [
            {
                'username': 'admin',
                'email': 'admin@example.com',
                'password': 'admin123'
            },
            {
                'username': 'testuser',
                'email': 'test@example.com',
                'password': 'test123'
            },
            {
                'username': 'demo',
                'email': 'demo@example.com',
                'password': 'demo123'
            }
        ]

        for user_data in test_users:
            user = User(
                username=user_data['username'],
                email=user_data['email'],
                password_hash=generate_password_hash(user_data['password'])
            )
            db.add(user)

        db.commit()
        print("Test data added successfully!")
        print("\nTest login credentials:")
        for user_data in test_users:
            print(f"Username: {user_data['username']}, Password: {user_data['password']}")

    except Exception as e:
        db.rollback()
        print(f"Error adding test data: {e}")
    finally:
        db.close()

def init_database():
    """Initialize database with tables and test data"""
    print("Initializing database...")
    create_tables()
    add_test_data()
    print("Database initialization complete!")

if __name__ == '__main__':
    init_database()
