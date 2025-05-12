from flask import Blueprint, render_template, request, abort
from models import Doctor, Department, DoctorDepartment
from flask_babel import gettext as _

doctors_bp = Blueprint('doctors', __name__)

@doctors_bp.route('/')
def index():
    specialty = request.args.get('specialty', '')
    department_id = request.args.get('department', '')
    
    query = Doctor.query.filter_by(is_active=True)
    
    if specialty:
        query = query.filter(Doctor.specialty.ilike(f'%{specialty}%'))
    
    if department_id:
        doctor_ids = DoctorDepartment.query.filter_by(department_id=department_id).with_entities(DoctorDepartment.doctor_id)
        query = query.filter(Doctor.id.in_(doctor_ids))
    
    doctors = query.all()
    departments = Department.query.all()
    
    return render_template(
        'doctors/index.html', 
        title=_('Our Doctors'), 
        doctors=doctors, 
        departments=departments,
        current_specialty=specialty,
        current_department=department_id
    )

@doctors_bp.route('/<int:doctor_id>')
def profile(doctor_id):
    doctor = Doctor.query.get_or_404(doctor_id)
    
    # Get the departments this doctor belongs to
    doctor_departments = DoctorDepartment.query.filter_by(doctor_id=doctor_id).all()
    departments = [dep.department for dep in doctor_departments]
    
    return render_template(
        'doctors/profile.html',
        title=f"Dr. {doctor.first_name} {doctor.last_name}",
        doctor=doctor,
        departments=departments
    )
