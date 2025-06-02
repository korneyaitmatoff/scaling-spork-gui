from sqlalchemy import create_engine, Column, Integer, String, DateTime, Boolean, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime, date
import os

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String(80), unique=True, nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    is_active = Column(Boolean, default=True)

    def __repr__(self):
        return f'<User {self.username}>'


class Student(Base):
    __tablename__ = 'students'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    group_code = Column(String(20), nullable=False)
    inn = Column(String(12), unique=True, nullable=False)
    serial_number = Column(String(20), nullable=False)
    birthdate = Column(Date, nullable=False)
    is_resident = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    @property
    def passport_data(self):
        return self.serial_number

    def __repr__(self):
        return f'<Student {self.name}>'


# Database configuration
DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://username:password@localhost/scaling_spork_db')
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
