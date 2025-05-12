from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from flask_babel import gettext as _
from models import Patient, Appointment
from app import db

patients_bp = Blueprint('patients', __name__)

@patients_bp.route('/portal')
@login_required
def portal():
    # Make sure the user has a patient profile
    if not hasattr(current_user, 'patient_profile') or not current_user.patient_profile:
        flash(_('You need a patient profile to access the patient portal'), 'warning')
        return redirect(url_for('main.index'))
    
    patient = current_user.patient_profile
    
    # Get upcoming appointments
    upcoming_appointments = Appointment.query.filter_by(
        patient_id=patient.id, 
        status='scheduled'
    ).order_by(Appointment.date, Appointment.time).all()
    
    # Get past appointments
    past_appointments = Appointment.query.filter_by(
        patient_id=patient.id,
        status='completed'
    ).order_by(Appointment.date.desc(), Appointment.time.desc()).all()
    
    return render_template('patients/portal.html',
                          title=_('Patient Portal'),
                          patient=patient,
                          upcoming_appointments=upcoming_appointments,
                          past_appointments=past_appointments)

@patients_bp.route('/profile')
@login_required
def profile():
    # In a real application, this would show detailed patient information
    # and allow editing of profile information
    if not hasattr(current_user, 'patient_profile') or not current_user.patient_profile:
        flash(_('You need a patient profile to access your profile'), 'warning')
        return redirect(url_for('main.index'))
    
    patient = current_user.patient_profile
    
    return render_template('patients/profile.html',
                          title=_('My Profile'),
                          patient=patient)
