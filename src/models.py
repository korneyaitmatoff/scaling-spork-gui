from sqlalchemy import create_engine, Column, Integer, String, DateTime, Boolean, Date, Text, ForeignKey, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
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


class IncomingRequest(Base):
    __tablename__ = 'incoming_requests'

    id = Column(Integer, primary_key=True)
    dean_name = Column(String(100), nullable=False)
    student_name = Column(String(100), nullable=False)
    education_form = Column(String(50), nullable=False)
    education_basis = Column(String(50), nullable=False)
    faculty = Column(String(100), nullable=False)
    course = Column(Integer, nullable=False)
    group = Column(String(20), nullable=False)
    phone = Column(String(20), nullable=False)
    reason = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    status = Column(String(20), default='pending')  # pending, approved, rejected

    def __repr__(self):
        return f'<IncomingRequest {self.student_name}>'


from datetime import datetime
from sqlalchemy.dialects.postgresql import JSONB


# Add these new model classes to your existing models.py file

class Protocol(Base):
    __tablename__ = 'protocols'

    id = Column(Integer, primary_key=True)
    number = Column(String(255), nullable=True)
    doc_date = Column(DateTime, default=datetime.utcnow)
    maintainer_id = Column(Integer, ForeignKey('users.id'), nullable=True)
    vote_id = Column(Integer, ForeignKey('votes.id'), nullable=True)
    budget_amount = Column(Integer, nullable=True)
    vote_json = Column(JSONB, default=None)
    created_at = Column(DateTime, default=datetime.utcnow)
    changed_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    maintainer = relationship('User', backref='maintained_protocols')
    vote = relationship('Vote', backref='protocols')

    def __repr__(self):
        return f'<Protocol {self.id}: Number {self.number}, Vote {self.vote_id}>'

    @property
    def formatted_doc_date(self):
        """Return formatted document date"""
        if self.doc_date:
            return self.doc_date.strftime('%d.%m.%Y %H:%M')
        return None

    @property
    def formatted_budget_amount(self):
        """Return formatted budget amount"""
        if self.budget_amount:
            return f"{self.budget_amount:,} руб."
        return "Не указано"

class Vote(Base):
    __tablename__ = 'votes'

    id = Column(Integer, primary_key=True)
    maintainer_id = Column(Integer, ForeignKey('users.id'), nullable=True)
    votes_json = Column(JSONB, default=None)
    is_active = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    changed_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'<Vote {self.id}: Maintainer {self.maintainer_id}>'


class VoteStudent(Base):
    __tablename__ = 'vote_students'

    id = Column(Integer, primary_key=True)
    student_id = Column(Integer, ForeignKey('students.id'), nullable=False)
    vote_id = Column(Integer, ForeignKey('votes.id'), nullable=False)
    protocol_id = Column(Integer, ForeignKey('protocols.id'), nullable=True)

    def __repr__(self):
        return f'<VoteStudent {self.id}: Student {self.student_id} -> Vote {self.vote_id}>'


class VoteEmployee(Base):
    __tablename__ = 'vote_employees'

    id = Column(Integer, primary_key=True)
    vote_id = Column(Integer, ForeignKey('votes.id'), nullable=False)
    protocol_id = Column(Integer, ForeignKey('protocols.id'), nullable=True)
    employee_id = Column(Integer, ForeignKey('users.id'), nullable=False)

    def __repr__(self):
        return f'<VoteEmployee {self.id}: Employee {self.employee_id} -> Vote {self.vote_id}>'


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
