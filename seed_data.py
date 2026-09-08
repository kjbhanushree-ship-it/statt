"""
seed_data.py — Populates the database with demo data for BIT Bangalore.
Run once:  python seed_data.py
"""
import random
from datetime import date, timedelta
from app import app
from models import db, User, Student, Subject, Department, AttendanceRecord

DEPARTMENTS = [
    ('Computer Science and Engineering',          'CSE'),
    ('Electronics and Communication Engineering', 'ECE'),
    ('Mechanical Engineering',                    'ME'),
    ('Civil Engineering',                         'Civil'),
    ('Electrical and Electronics Engineering',    'EEE'),
    ('Information Science and Engineering',       'ISE'),
    ('Chemical Engineering',                      'Chemical'),
    ('Biotechnology',                             'Biotech'),
]

SUBJECTS = {
    'CSE':     [('Data Structures','21CS301'),('DBMS','21CS302'),('OS','21CS303'),('CN','21CS304'),('DAA','21CS305')],
    'ECE':     [('Signals & Systems','21EC301'),('Analog Circuits','21EC302'),('DSP','21EC303'),('VLSI','21EC304'),('EMF','21EC305')],
    'ME':      [('Thermodynamics','21ME301'),('Fluid Mechanics','21ME302'),('Machine Design','21ME303'),('Manufacturing','21ME304'),('Heat Transfer','21ME305')],
    'Civil':   [('Structural Analysis','21CV301'),('Soil Mechanics','21CV302'),('Fluid Mechanics','21CV303'),('Surveying','21CV304'),('Transportation Engg','21CV305')],
    'EEE':     [('Power Systems','21EE301'),('Electrical Machines','21EE302'),('Control Systems','21EE303'),('Power Electronics','21EE304'),('Instrumentation','21EE305')],
    'ISE':     [('Software Engg','21IS301'),('Web Technologies','21IS302'),('Cloud Computing','21IS303'),('ML','21IS304'),('Cyber Security','21IS305')],
    'Chemical':[('Chemical Rxn Engg','21CH301'),('Mass Transfer','21CH302'),('Heat Transfer','21CH303'),('Process Control','21CH304'),('Petrochemical Engg','21CH305')],
    'Biotech': [('Molecular Biology','21BT301'),('Bioinformatics','21BT302'),('Genetic Engg','21BT303'),('Fermentation','21BT304'),('Biochemistry','21BT305')],
}

STUDENT_NAMES = [
    'Aarav Sharma','Aditi Nair','Akash Reddy','Anamika Iyer','Ananya Kulkarni',
    'Arjun Patel','Bhavana Rao','Chetan Gowda','Deepika Singh','Divya Menon',
    'Ganesh Patil','Harsha Joshi','Ishaan Verma','Jyothi Hegde','Kavya Shetty',
    'Keerthi Murthy','Kiran Kumar','Lakshmi Prasad','Manoj Bhatt','Meera Subramaniam',
    'Naveen Krishnamurthy','Nisha Thomas','Prashanth Kamath','Priya Agarwal','Rahul Desai',
    'Ramesh Naidu','Rohini Bhat','Sachin Pillai','Sandeep Shukla','Shruti Yadav',
]

def seed():
    with app.app_context():
        db.drop_all()
        db.create_all()

        # Admin
        admin = User(username='admin', email='admin@bit.edu.in',
                     name='Administrator', role='admin')
        admin.set_password('admin123')
        db.session.add(admin)
        db.session.flush()

        dept_objs = {}
        hod_objs  = {}
        fac_objs  = {}

        for dname, dcode in DEPARTMENTS:
            dept = Department(name=dname, code=dcode)
            db.session.add(dept)
            db.session.flush()
            dept_objs[dcode] = dept

            # HOD
            hod = User(username=f'hod_{dcode.lower()}',
                       email=f'hod.{dcode.lower()}@bit.edu.in',
                       name=f'Dr. HOD {dcode}', role='hod',
                       department_id=dept.id)
            hod.set_password('hod123')
            db.session.add(hod)

            # 2 Faculty
            fac_list = []
            for j in range(1, 3):
                fac = User(username=f'fac_{dcode.lower()}_{j}',
                           email=f'faculty{j}.{dcode.lower()}@bit.edu.in',
                           name=f'Prof. Faculty{j} {dcode}', role='faculty',
                           department_id=dept.id)
                fac.set_password('fac123')
                db.session.add(fac)
                fac_list.append(fac)
            db.session.flush()
            hod_objs[dcode] = hod
            fac_objs[dcode] = fac_list

        db.session.flush()

        # Subjects (Sem 3, Section A) for each dept
        subj_objs = {}
        for dcode, subj_list in SUBJECTS.items():
            dept = dept_objs[dcode]
            facs = fac_objs[dcode]
            subj_objs[dcode] = []
            for i, (sname, scode) in enumerate(subj_list):
                subj = Subject(name=sname, code=scode,
                               department_id=dept.id, semester=3,
                               credits=4, section='A',
                               faculty_id=facs[i % 2].id)
                db.session.add(subj)
                subj_objs[dcode].append(subj)
        db.session.flush()

        # Students (6 per dept for demo, USN format 1BIyyDDDnnn)
        stu_objs = {}
        for dcode, dept in dept_objs.items():
            stu_objs[dcode] = []
            for idx, sname in enumerate(STUDENT_NAMES[:6], 1):
                usn = f'1BI23{dcode[:2]}{idx:03d}'
                uname = f'stu_{dcode.lower()}_{idx}'
                email = f'{uname}@bit.edu.in'
                u = User(username=uname, email=email, name=sname,
                         role='student', department_id=dept.id)
                u.set_password('stu123')
                db.session.add(u); db.session.flush()
                s = Student(usn=usn, name=sname, department_id=dept.id,
                            semester=3, section='A', user_id=u.id, email=email)
                db.session.add(s); db.session.flush()
                stu_objs[dcode].append(s)

        db.session.flush()

        # Attendance for last 2 months (only working days Mon-Fri, 1 class/day/subject)
        today = date.today()
        for offset_m in range(2, 0, -1):
            # approximate: go back offset_m * 30 days
            start = today - timedelta(days=offset_m * 30)
            end   = today - timedelta(days=(offset_m - 1) * 30)
            for dcode in dept_objs:
                for subj in subj_objs[dcode]:
                    d = start
                    while d < end:
                        if d.weekday() < 5:  # Mon-Fri
                            for stu in stu_objs[dcode]:
                                # 80% present, 20% absent
                                st = 'P' if random.random() < 0.80 else 'A'
                                rec = AttendanceRecord(
                                    student_id=stu.id, subject_id=subj.id,
                                    date=d, status=st,
                                    marked_by_id=subj.faculty_id)
                                db.session.add(rec)
                        d += timedelta(days=1)

        db.session.commit()
        print("[OK] Database seeded successfully!")
        print("\nLogin credentials:")
        print("  Admin   - admin    / admin123")
        print("  HOD     - hod_cse  / hod123")
        print("  Faculty - fac_cse_1/ fac123")
        print("  Student - stu_cse_1/ stu123")

if __name__ == '__main__':
    seed()
