from flask import Blueprint, render_template, request, redirect, url_for, flash, abort
from flask_login import login_required, current_user
from flask_babel import gettext as _
from models import Doctor, Appointment, DoctorSchedule, Patient
from app import db
from datetime import datetime, timedelta
import calendar
from sqlalchemy import and_
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, DateField, TextAreaField, HiddenField
from wtforms.validators import DataRequired, Email

appointments_bp = Blueprint('appointments', __name__)

class AppointmentForm(FlaskForm):
    first_name = StringField(_('First Name'), validators=[DataRequired()])
    last_name = StringField(_('Last Name'), validators=[DataRequired()])
    email = StringField(_('Email'), validators=[DataRequired(), Email()])
    phone = StringField(_('Phone'), validators=[DataRequired()])
    date = DateField(_('Appointment Date'), validators=[DataRequired()])
    time_slot = SelectField(_('Time Slot'), validators=[DataRequired()])
    reason = TextAreaField(_('Reason for Visit'))
    doctor_id = HiddenField('Doctor ID', validators=[DataRequired()])

@appointments_bp.route('/book', methods=['GET', 'POST'])
def book():
    form = AppointmentForm()
    
    # Get doctor ID from query param or form
    doctor_id = request.args.get('doctor_id', type=int) or form.doctor_id.data
    
    # If no doctor selected, redirect to doctor list
    if not doctor_id:
        flash(_('Please select a doctor first'), 'warning')
        return redirect(url_for('doctors.index'))
    
    doctor = Doctor.query.get_or_404(doctor_id)
    form.doctor_id.data = doctor_id
    
    # For GET requests or invalid form, populate the time slots
    if request.method == 'GET' or not form.validate_on_submit():
        # Get available time slots for the doctor
        selected_date = request.args.get('date') or datetime.now().strftime('%Y-%m-%d')
        selected_date = datetime.strptime(selected_date, '%Y-%m-%d').date()
        
        # Get day of week (0-6 for Monday-Sunday)
        day_of_week = selected_date.weekday()
        
        # Get doctor's schedule for this day
        schedule = DoctorSchedule.query.filter(
            and_(
                DoctorSchedule.doctor_id == doctor_id,
                DoctorSchedule.day_of_week == day_of_week,
                DoctorSchedule.is_available == True
            )
        ).first()
        
        # Generate available time slots
        time_slots = []
        if schedule:
            # Get already booked appointments for this doctor on this date
            booked_appointments = Appointment.query.filter(
                and_(
                    Appointment.doctor_id == doctor_id,
                    Appointment.date == selected_date,
                    Appointment.status != 'cancelled'
                )
            ).all()
            
            # Create list of booked times
            booked_times = [appointment.time for appointment in booked_appointments]
            
            # Generate 30-minute slots between start and end time
            current_time = schedule.start_time
            while current_time < schedule.end_time:
                # If this slot is not already booked
                if current_time not in booked_times:
                    time_slots.append((current_time.strftime('%H:%M'), current_time.strftime('%I:%M %p')))
                
                # Move to next 30-minute slot
                hour = current_time.hour
                minute = current_time.minute + 30
                if minute >= 60:
                    hour += 1
                    minute -= 60
                current_time = datetime.strptime(f"{hour}:{minute}", "%H:%M").time()
        
        form.time_slot.choices = time_slots
        
        return render_template('appointments/book.html', 
                               title=_('Book an Appointment'),
                               doctor=doctor,
                               form=form,
                               selected_date=selected_date)
    
    # Process form submission
    if form.validate_on_submit():
        # Create the appointment
        appointment_time = datetime.strptime(form.time_slot.data, '%H:%M').time()
        
        # Check if user is logged in
        patient = None
        if current_user.is_authenticated and hasattr(current_user, 'patient_profile'):
            patient = current_user.patient_profile
        
        # If patient doesn't exist, either not logged in or doctor/admin account
        # In a real application, you would create a temporary patient record here
        # or require login, but for this example we'll just show a confirmation
        # without actually saving the record to demonstrate the flow
        if not patient:
            flash(_('Your appointment request with Dr. {doctor} on {date} at {time} has been received. '
                    'Please create a patient account to confirm.').format(
                        doctor=f"{doctor.first_name} {doctor.last_name}",
                        date=form.date.data.strftime('%B %d, %Y'),
                        time=datetime.strptime(form.time_slot.data, '%H:%M').strftime('%I:%M %p')
                    ), 'info')
            return redirect(url_for('appointments.confirm'))
        
        # Create and save appointment
        appointment = Appointment(
            patient_id=patient.id,
            doctor_id=doctor_id,
            date=form.date.data,
            time=appointment_time,
            reason=form.reason.data,
            status='scheduled'
        )
        
        db.session.add(appointment)
        db.session.commit()
        
        flash(_('Your appointment with Dr. {doctor} has been scheduled successfully!').format(
            doctor=f"{doctor.first_name} {doctor.last_name}"
        ), 'success')
        
        return redirect(url_for('appointments.confirm'))
    
    return render_template('appointments/book.html', 
                           title=_('Book an Appointment'),
                           doctor=doctor,
                           form=form)

@appointments_bp.route('/confirm')
def confirm():
    return render_template('appointments/confirm.html', title=_('Appointment Confirmation'))

@appointments_bp.route('/my-appointments')
@login_required
def my_appointments():
    # This route would show a patient their upcoming appointments
    # Only accessible to authenticated users with a patient profile
    if not hasattr(current_user, 'patient_profile') or not current_user.patient_profile:
        flash(_('You need a patient profile to view appointments'), 'warning')
        return redirect(url_for('main.index'))
    
    patient = current_user.patient_profile
    appointments = Appointment.query.filter_by(patient_id=patient.id).all()
    
    return render_template('appointments/my_appointments.html', 
                           title=_('My Appointments'),
                           appointments=appointments)
