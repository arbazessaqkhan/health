from flask import Blueprint, render_template, request, redirect, url_for, abort
from flask_babel import gettext as _
from models import Doctor, Department
from app import db

doctors_bp = Blueprint('doctors', __name__)

@doctors_bp.route('/')
def index():
    # Get optional department filter
    department_id = request.args.get('department', type=int)
    
    # Query doctors with optional filtering
    if department_id:
        doctors = Doctor.query.filter_by(department_id=department_id).all()
        department = Department.query.get_or_404(department_id)
        title = _('Doctors in {department}').format(department=department.name)
    else:
        doctors = Doctor.query.all()
        title = _('Our Doctors')
    
    # Get all departments for filter dropdown
    departments = Department.query.all()
    
    return render_template('doctors/index.html', 
                           title=title,
                           doctors=doctors, 
                           departments=departments, 
                           selected_department=department_id)

@doctors_bp.route('/<int:doctor_id>')
def profile(doctor_id):
    doctor = Doctor.query.get_or_404(doctor_id)
    schedules = doctor.schedules.all()
    
    return render_template('doctors/profile.html', 
                           title=f"Dr. {doctor.first_name} {doctor.last_name}", 
                           doctor=doctor,
                           schedules=schedules)
