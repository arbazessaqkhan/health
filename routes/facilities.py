from flask import Blueprint, render_template, abort
from flask_babel import gettext as _
from models import Department, Service

facilities_bp = Blueprint('facilities', __name__)

@facilities_bp.route('/')
def index():
    departments = Department.query.all()
    return render_template('facilities/index.html', 
                          title=_('Our Facilities & Departments'),
                          departments=departments)

@facilities_bp.route('/department/<int:department_id>')
def department(department_id):
    department = Department.query.get_or_404(department_id)
    services = Service.query.filter_by(department_id=department_id).all()
    doctors = department.doctors.all()
    
    return render_template('facilities/department.html',
                          title=department.name,
                          department=department,
                          services=services,
                          doctors=doctors)
