from sqlalchemy import create_engine
from models import Base, User, Student, IncomingRequest, SessionLocal
from werkzeug.security import generate_password_hash
from datetime import date, datetime
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
        if not existing_user:
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

            print("Test users added successfully!")

        # Check if test students already exist
        existing_student = db.query(Student).first()
        if not existing_student:
            # Create test students
            test_students = [
                {
                    'name': 'Иванов Иван Иванович',
                    'group_code': 'ИС-21-1',
                    'inn': '1234567890',
                    'serial_number': '1234 567890',
                    'birthdate': date(2003, 5, 15),
                    'is_resident': True
                },
                {
                    'name': 'Петрова Анна Сергеевна',
                    'group_code': 'ИС-21-1',
                    'inn': '2345678901',
                    'serial_number': '2345 678901',
                    'birthdate': date(2003, 8, 22),
                    'is_resident': True
                },
                {
                    'name': 'Сидоров Петр Александрович',
                    'group_code': 'ИС-21-2',
                    'inn': '3456789012',
                    'serial_number': '3456 789012',
                    'birthdate': date(2003, 12, 10),
                    'is_resident': True
                },
                {
                    'name': 'Козлова Мария Дмитриевна',
                    'group_code': 'ИС-21-2',
                    'inn': '4567890123',
                    'serial_number': '4567 890123',
                    'birthdate': date(2003, 3, 7),
                    'is_resident': True
                },
                {
                    'name': 'Новиков Алексей Викторович',
                    'group_code': 'ИС-20-1',
                    'inn': '5678901234',
                    'serial_number': '5678 901234',
                    'birthdate': date(2002, 9, 18),
                    'is_resident': True
                },
                {
                    'name': 'Морозова Елена Павловна',
                    'group_code': 'ИС-20-1',
                    'inn': '6789012345',
                    'serial_number': '6789 012345',
                    'birthdate': date(2002, 11, 25),
                    'is_resident': False
                },
                {
                    'name': 'Волков Дмитрий Андреевич',
                    'group_code': 'ИС-22-1',
                    'inn': '7890123456',
                    'serial_number': '7890 123456',
                    'birthdate': date(2004, 1, 14),
                    'is_resident': True
                },
                {
                    'name': 'Лебедева Ольга Николаевна',
                    'group_code': 'ИС-22-1',
                    'inn': '8901234567',
                    'serial_number': '8901 234567',
                    'birthdate': date(2004, 6, 30),
                    'is_resident': True
                }
            ]

            for student_data in test_students:
                student = Student(**student_data)
                db.add(student)

            print("Test students added successfully!")

        # Check if test incoming requests already exist
        existing_request = db.query(IncomingRequest).first()
        if not existing_request:
            # Create test incoming requests
            test_requests = [
                {
                    'dean_name': 'Профессор Смирнов А.В.',
                    'student_name': 'Иванов Иван Иванович',
                    'education_form': 'full-time',
                    'education_basis': 'budget',
                    'faculty': 'Факультет информационных систем',
                    'course': 3,
                    'group': 'ИС-21-1',
                    'phone': '+7 (999) 123-45-67',
                    'reason': 'Прошу оказать материальную помощь в связи с тяжелым материальным положением семьи. Отец потерял работу, мать находится в декретном отпуске. Необходимы средства на оплату общежития и питания.',
                    'status': 'pending'
                },
                {
                    'dean_name': 'Доцент Петрова М.И.',
                    'student_name': 'Козлова Мария Дмитриевна',
                    'education_form': 'full-time',
                    'education_basis': 'budget',
                    'faculty': 'Факультет информационных систем',
                    'course': 3,
                    'group': 'ИС-21-2',
                    'phone': '+7 (999) 234-56-78',
                    'reason': 'Прошу предоставить материальную помощь для покрытия расходов на лечение. Требуется дорогостоящая операция, семья не может самостоятельно оплатить медицинские услуги.',
                    'status': 'approved'
                },
                {
                    'dean_name': 'Профессор Волков С.П.',
                    'student_name': 'Новиков Алексей Викторович',
                    'education_form': 'full-time',
                    'education_basis': 'contract',
                    'faculty': 'Факультет информационных систем',
                    'course': 4,
                    'group': 'ИС-20-1',
                    'phone': '+7 (999) 345-67-89',
                    'reason': 'Прошу оказать материальную поддержку в связи с рождением ребенка в семье. Необходимы средства на детские товары и медицинское обслуживание.',
                    'status': 'pending'
                },
                {
                    'dean_name': 'Доцент Морозова Е.А.',
                    'student_name': 'Лебедева Ольга Николаевна',
                    'education_form': 'full-time',
                    'education_basis': 'budget',
                    'faculty': 'Факультет информационных систем',
                    'course': 2,
                    'group': 'ИС-22-1',
                    'phone': '+7 (999) 456-78-90',
                    'reason': 'Прошу предоставить материальную помощь в связи с потерей кормильца. После смерти отца семья оказалась в трудном финансовом положении.',
                    'status': 'approved'
                },
                {
                    'dean_name': 'Профессор Смирнов А.В.',
                    'student_name': 'Петрова Анна Сергеевна',
                    'education_form': 'full-time',
                    'education_basis': 'budget',
                    'faculty': 'Факультет информационных систем',
                    'course': 3,
                    'group': 'ИС-21-1',
                    'phone': '+7 (999) 567-89-01',
                    'reason': 'Прошу оказать материальную помощь для приобретения учебной литературы и оплаты интернета для дистанционного обучения. Семья имеет низкий доход.',
                    'status': 'rejected'
                },
                {
                    'dean_name': 'Доцент Кузнецов И.В.',
                    'student_name': 'Волков Дмитрий Андреевич',
                    'education_form': 'full-time',
                    'education_basis': 'budget',
                    'faculty': 'Факультет информационных систем',
                    'course': 2,
                    'group': 'ИС-22-1',
                    'phone': '+7 (999) 678-90-12',
                    'reason': 'Прошу предоставить материальную поддержку в связи с необходимостью оплаты проезда к месту прохождения практики в другом городе.',
                    'status': 'pending'
                }
            ]

            for request_data in test_requests:
                incoming_request = IncomingRequest(**request_data)
                db.add(incoming_request)

            print("Test incoming requests added successfully!")

        db.commit()
        print("\nTest login credentials:")
        print("Username: admin, Password: admin123")
        print("Username: testuser, Password: test123")
        print("Username: demo, Password: demo123")

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
