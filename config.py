import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'bit-bangalore-attendance-secret-2024'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'attendance.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    ATTENDANCE_THRESHOLD = 75
    HOST = os.environ.get('HOST', '0.0.0.0')
    PORT = int(os.environ.get('PORT', 5000))
    DEBUG = os.environ.get('DEBUG', 'False').lower() == 'true'
    COLLEGE_NAME = 'Bangalore Institute of Technology'
    COLLEGE_SHORT = 'BIT'
