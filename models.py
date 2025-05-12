from app import db
from flask_login import UserMixin
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    first_name = db.Column(db.String(64), nullable=False)
    last_name = db.Column(db.String(64), nullable=False)
    date_of_birth = db.Column(db.Date, nullable=True)
    phone = db.Column(db.String(20), nullable=True)
    address = db.Column(db.String(256), nullable=True)
    role = db.Column(db.String(20), default='patient')
    preferred_language = db.Column(db.String(10), default='en')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationship
    appointments = db.relationship('Appointment', backref='user', lazy='dynamic')
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
        
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def __repr__(self):
        return f'<User {self.username}>'

class Doctor(db.Model):
    __tablename__ = 'doctors'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    first_name = db.Column(db.String(64), nullable=False)
    last_name = db.Column(db.String(64), nullable=False)
    specialty = db.Column(db.String(128), nullable=False)
    qualifications = db.Column(db.String(256), nullable=False)
    bio = db.Column(db.Text, nullable=True)
    years_experience = db.Column(db.Integer, nullable=True)
    photo_url = db.Column(db.String(256), nullable=True)
    languages_spoken = db.Column(db.String(128), nullable=True)
    consulting_hours = db.Column(db.String(256), nullable=True)
    is_active = db.Column(db.Boolean, default=True)
    
    # Relationship
    appointments = db.relationship('Appointment', backref='doctor', lazy='dynamic')
    departments = db.relationship('DoctorDepartment', backref='doctor', lazy='dynamic')
    
    def __repr__(self):
        return f'<Doctor {self.first_name} {self.last_name} - {self.specialty}>'

class Department(db.Model):
    __tablename__ = 'departments'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    description = db.Column(db.Text, nullable=True)
    floor = db.Column(db.String(10), nullable=True)
    building = db.Column(db.String(64), nullable=True)
    
    # Relationship
    doctors = db.relationship('DoctorDepartment', backref='department', lazy='dynamic')
    
    def __repr__(self):
        return f'<Department {self.name}>'

class DoctorDepartment(db.Model):
    __tablename__ = 'doctor_departments'
    
    id = db.Column(db.Integer, primary_key=True)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctors.id'), nullable=False)
    department_id = db.Column(db.Integer, db.ForeignKey('departments.id'), nullable=False)

class Appointment(db.Model):
    __tablename__ = 'appointments'
    
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctors.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    time = db.Column(db.Time, nullable=False)
    reason = db.Column(db.Text, nullable=True)
    status = db.Column(db.String(20), default='scheduled')  # scheduled, completed, cancelled, no-show
    appointment_type = db.Column(db.String(20), default='in-person')  # in-person, telemedicine
    notes = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Appointment {self.id} - {self.date} {self.time}>'

class Service(db.Model):
    __tablename__ = 'services'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    description = db.Column(db.Text, nullable=True)
    department_id = db.Column(db.Integer, db.ForeignKey('departments.id'), nullable=True)
    is_active = db.Column(db.Boolean, default=True)
    
    def __repr__(self):
        return f'<Service {self.name}>'

class FAQ(db.Model):
    __tablename__ = 'faqs'
    
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String(256), nullable=False)
    answer = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(64), nullable=True)
    display_order = db.Column(db.Integer, default=0)
    
    def __repr__(self):
        return f'<FAQ {self.question[:30]}>'
