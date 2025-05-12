from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from models import Appointment
from datetime import datetime
from flask_babel import gettext as _

patients_bp = Blueprint('patients', __name__)

@patients_bp.route('/portal')
@login_required
def portal():
    # Get all upcoming appointments for the current user
    upcoming_appointments = Appointment.query.filter_by(
        patient_id=current_user.id,
        status='scheduled'
    ).filter(
        Appointment.date >= datetime.now().date()
    ).order_by(
        Appointment.date, Appointment.time
    ).all()
    
    # Get past appointments
    past_appointments = Appointment.query.filter_by(
        patient_id=current_user.id
    ).filter(
        Appointment.date < datetime.now().date()
    ).order_by(
        Appointment.date.desc(), Appointment.time.desc()
    ).limit(10).all()
    
    return render_template(
        'patients/portal.html', 
        title=_('Patient Portal'),
        upcoming_appointments=upcoming_appointments,
        past_appointments=past_appointments
    )

@patients_bp.route('/cancel-appointment/<int:appointment_id>', methods=['POST'])
@login_required
def cancel_appointment(appointment_id):
    appointment = Appointment.query.get_or_404(appointment_id)
    
    # Verify this appointment belongs to the current user
    if appointment.patient_id != current_user.id:
        flash(_('You do not have permission to cancel this appointment.'), 'danger')
        return redirect(url_for('patients.portal'))
    
    # Only allow cancellation of future appointments
    if appointment.date < datetime.now().date():
        flash(_('You cannot cancel past appointments.'), 'danger')
        return redirect(url_for('patients.portal'))
    
    appointment.status = 'cancelled'
    from app import db
    db.session.commit()
    
    flash(_('Your appointment has been cancelled.'), 'success')
    return redirect(url_for('patients.portal'))
