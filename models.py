from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()


class Department(db.Model):
    __tablename__ = 'departments'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    code = db.Column(db.String(20), unique=True, nullable=False)

    users = db.relationship('User', backref='department', lazy='dynamic')
    students = db.relationship('Student', backref='department', lazy='dynamic')
    subjects = db.relationship('Subject', backref='department', lazy='dynamic')

    def __repr__(self):
        return f'<Department {self.code}>'


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(20), nullable=False)  # admin, hod, faculty, student
    department_id = db.Column(db.Integer, db.ForeignKey('departments.id'))
    is_active_user = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    subjects_taught = db.relationship(
        'Subject', backref='faculty', lazy='dynamic',
        foreign_keys='Subject.faculty_id')
    attendance_marked = db.relationship(
        'AttendanceRecord', backref='marked_by_user', lazy='dynamic',
        foreign_keys='AttendanceRecord.marked_by_id')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.username} ({self.role})>'


class Student(db.Model):
    __tablename__ = 'students'
    id = db.Column(db.Integer, primary_key=True)
    usn = db.Column(db.String(20), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    department_id = db.Column(db.Integer, db.ForeignKey('departments.id'), nullable=False)
    semester = db.Column(db.Integer, nullable=False)
    section = db.Column(db.String(5), nullable=False, default='A')
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), unique=True, nullable=True)
    phone = db.Column(db.String(15))
    email = db.Column(db.String(120))

    user = db.relationship('User', backref='student_profile', foreign_keys=[user_id])
    attendance_records = db.relationship('AttendanceRecord', backref='student', lazy='dynamic')

    def __repr__(self):
        return f'<Student {self.usn} - {self.name}>'


class Subject(db.Model):
    __tablename__ = 'subjects'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    code = db.Column(db.String(20), nullable=False)
    department_id = db.Column(db.Integer, db.ForeignKey('departments.id'), nullable=False)
    semester = db.Column(db.Integer, nullable=False)
    credits = db.Column(db.Integer, default=4)
    faculty_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    section = db.Column(db.String(5), default='A')

    attendance_records = db.relationship('AttendanceRecord', backref='subject', lazy='dynamic')

    def __repr__(self):
        return f'<Subject {self.code} - {self.name}>'


class AttendanceRecord(db.Model):
    __tablename__ = 'attendance_records'
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False)
    subject_id = db.Column(db.Integer, db.ForeignKey('subjects.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    status = db.Column(db.String(10), nullable=False)  # P, A, L
    marked_by_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    marked_at = db.Column(db.DateTime, default=datetime.utcnow)

    __table_args__ = (
        db.UniqueConstraint('student_id', 'subject_id', 'date', name='uq_attendance'),
    )

    def __repr__(self):
        return f'<Attendance {self.student_id} {self.date} {self.status}>'


class Condonation(db.Model):
    __tablename__ = 'condonations'
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False)
    subject_id = db.Column(db.Integer, db.ForeignKey('subjects.id'), nullable=False)
    month = db.Column(db.Integer, nullable=False)
    year = db.Column(db.Integer, nullable=False)
    condoned_classes = db.Column(db.Integer, default=0)
    condoned_by_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    reason = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    student = db.relationship('Student', backref='condonations')
    subject = db.relationship('Subject', backref='condonations')
    condoned_by = db.relationship('User', backref='condonations_granted')
