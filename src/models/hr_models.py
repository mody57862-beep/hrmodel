from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Employee(db.Model):
    __tablename__ = 'employees'
    
    employee_id = db.Column(db.Integer, primary_key=True) # مسلسل الموظف
    full_name = db.Column(db.String(255), nullable=False) # الاسم
    house_number = db.Column(db.String(50)) # الدار
    national_id = db.Column(db.String(50), unique=True) # الرقم القومي
    job_title = db.Column(db.String(255)) # الوظيفة
    qualification = db.Column(db.String(255)) # المؤهل
    hire_date = db.Column(db.Date) # تاريخ التعيين
    points_count = db.Column(db.Integer, default=0) # عدد الابناط (النقاط فوق المرتب)
    years_of_experience = db.Column(db.Integer, default=0) # سنوات الخبرة
    salary_from_system = db.Column(db.Float) # الراتب من المنظومة
    actual_salary = db.Column(db.Float) # الراتب
    department_code = db.Column(db.String(50)) # كود القسم
    
    # الحقول القديمة التي قد تكون موجودة أو نحتاجها
    department = db.Column(db.String(255)) # القسم (للتوافق مع الواجهة الحالية)
    email = db.Column(db.String(255))
    phone = db.Column(db.String(50))
    birth_date = db.Column(db.Date)
    nationality = db.Column(db.String(100))
    id_number = db.Column(db.String(50), unique=True) # قد يكون مكرر مع national_id، يمكن توحيده لاحقاً
    address = db.Column(db.Text)
    marital_status = db.Column(db.String(50))
    children_count = db.Column(db.Integer, default=0)
    education_level = db.Column(db.String(255))
    specialization = db.Column(db.String(255))
    contract_end_date = db.Column(db.Date)
    basic_salary = db.Column(db.Float)
    allowances = db.Column(db.Float)
    total_salary = db.Column(db.Float)
    bank_account = db.Column(db.String(255))
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # العلاقات
    leave_management = db.relationship('LeaveManagement', backref='employee', uselist=False)
    leave_requests = db.relationship('LeaveRequest', foreign_keys='[LeaveRequest.employee_id]', backref='requester')
    approved_leave_requests = db.relationship('LeaveRequest', foreign_keys='[LeaveRequest.approved_by]', backref='approver')
    attendance_records = db.relationship('Attendance', backref='employee')
    managed_departments = db.relationship('Department', foreign_keys='[Department.manager_id]', backref='manager')
    created_documents = db.relationship('Document', foreign_keys='[Document.created_by]', backref='creator')
    related_documents = db.relationship('Document', foreign_keys='[Document.employee_id]', backref='related_employee')

    def to_dict(self):
        return {
            'employee_id': self.employee_id,
            'full_name': self.full_name,
            'house_number': self.house_number,
            'national_id': self.national_id,
            'job_title': self.job_title,
            'qualification': self.qualification,
            'hire_date': self.hire_date.isoformat() if self.hire_date else None,
            'points_count': self.points_count,
            'years_of_experience': self.years_of_experience,
            'salary_from_system': self.salary_from_system,
            'actual_salary': self.actual_salary,
            'department_code': self.department_code,
            'department': self.department,
            'email': self.email,
            'phone': self.phone,
            'birth_date': self.birth_date.isoformat() if self.birth_date else None,
            'nationality': self.nationality,
            'id_number': self.id_number,
            'address': self.address,
            'marital_status': self.marital_status,
            'children_count': self.children_count,
            'education_level': self.education_level,
            'specialization': self.specialization,
            'contract_end_date': self.contract_end_date.isoformat() if self.contract_end_date else None,
            'basic_salary': self.basic_salary,
            'allowances': self.allowances,
            'total_salary': self.total_salary,
            'bank_account': self.bank_account,
            'notes': self.notes
        }

class LeaveManagement(db.Model):
    __tablename__ = 'leave_management'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('employees.employee_id'), nullable=False)
    annual_leave_balance = db.Column(db.Integer, default=21)
    casual_leave_balance = db.Column(db.Integer, default=6)
    sick_leave_balance = db.Column(db.Integer, default=15)
    annual_leave_used = db.Column(db.Integer, default=0)
    casual_leave_used = db.Column(db.Integer, default=0)
    sick_leave_used = db.Column(db.Integer, default=0)
    last_updated = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'employee_id': self.employee_id,
            'annual_leave_balance': self.annual_leave_balance,
            'casual_leave_balance': self.casual_leave_balance,
            'sick_leave_balance': self.sick_leave_balance,
            'annual_leave_used': self.annual_leave_used,
            'casual_leave_used': self.casual_leave_used,
            'sick_leave_used': self.sick_leave_used,
            'last_updated': self.last_updated.isoformat() if self.last_updated else None
        }

class LeaveRequest(db.Model):
    __tablename__ = 'leave_requests'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('employees.employee_id'), nullable=False)
    leave_type = db.Column(db.String(50), nullable=False)  # 'annual', 'casual', 'sick', 'other'
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    days_requested = db.Column(db.Integer, nullable=False)
    reason = db.Column(db.Text)
    status = db.Column(db.String(50), default='pending')  # 'pending', 'approved', 'rejected'
    requested_at = db.Column(db.DateTime, default=datetime.utcnow)
    approved_by = db.Column(db.Integer, db.ForeignKey('employees.employee_id'))
    approved_at = db.Column(db.DateTime)
    
    def to_dict(self):
        return {
            'id': self.id,
            'employee_id': self.employee_id,
            'leave_type': self.leave_type,
            'start_date': self.start_date.isoformat() if self.start_date else None,
            'end_date': self.end_date.isoformat() if self.end_date else None,
            'days_requested': self.days_requested,
            'reason': self.reason,
            'status': self.status,
            'requested_at': self.requested_at.isoformat() if self.requested_at else None,
            'approved_by': self.approved_by,
            'approved_at': self.approved_at.isoformat() if self.approved_at else None
        }

class Attendance(db.Model):
    __tablename__ = 'attendance'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('employees.employee_id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    check_in_time = db.Column(db.Time)
    check_out_time = db.Column(db.Time)
    working_hours = db.Column(db.Float)
    late_minutes = db.Column(db.Integer, default=0)
    status = db.Column(db.String(50))  # 'on_time', 'late', 'absent'
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    __table_args__ = (db.UniqueConstraint('employee_id', 'date', name='unique_employee_date'),)
    
    def to_dict(self):
        return {
            'id': self.id,
            'employee_id': self.employee_id,
            'date': self.date.isoformat() if self.date else None,
            'check_in_time': self.check_in_time.isoformat() if self.check_in_time else None,
            'check_out_time': self.check_out_time.isoformat() if self.check_out_time else None,
            'working_hours': self.working_hours,
            'late_minutes': self.late_minutes,
            'status': self.status,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class Department(db.Model):
    __tablename__ = 'departments'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False, unique=True)
    description = db.Column(db.Text)
    manager_id = db.Column(db.Integer, db.ForeignKey('employees.employee_id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'manager_id': self.manager_id,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class Document(db.Model):
    __tablename__ = 'documents'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    document_number = db.Column(db.String(100), unique=True, nullable=False)
    document_type = db.Column(db.String(100), nullable=False)
    employee_id = db.Column(db.Integer, db.ForeignKey('employees.employee_id'))
    subject = db.Column(db.String(255))
    content = db.Column(db.Text)
    recipient = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    created_by = db.Column(db.Integer, db.ForeignKey('employees.employee_id'))
    file_path = db.Column(db.String(500))
    
    def to_dict(self):
        return {
            'id': self.id,
            'document_number': self.document_number,
            'document_type': self.document_type,
            'employee_id': self.employee_id,
            'subject': self.subject,
            'content': self.content,
            'recipient': self.recipient,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'created_by': self.created_by,
            'file_path': self.file_path
        }

