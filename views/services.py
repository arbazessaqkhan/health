from flask import Blueprint, render_template
from models import Service, Department
from flask_babel import gettext as _

services_bp = Blueprint('services', __name__)

@services_bp.route('/')
def index():
    services = Service.query.filter_by(is_active=True).all()
    departments = Department.query.all()
    
    # Group services by department
    services_by_dept = {}
    for dept in departments:
        services_by_dept[dept] = [s for s in services if s.department_id == dept.id]
    
    # Add services without a department
    services_without_dept = [s for s in services if s.department_id is None]
    if services_without_dept:
        services_by_dept['Other Services'] = services_without_dept
    
    return render_template(
        'services.html', 
        title=_('Our Services'),
        services_by_dept=services_by_dept,
        all_services=services
    )
