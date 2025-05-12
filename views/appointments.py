from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from models import Doctor, Appointment, db
from datetime import datetime, time, timedelta
from flask_wtf import FlaskForm
from wtforms import StringField, DateField, TimeField, SelectField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length
from flask_babel import gettext as _

appointments_bp = Blueprint('appointments', __name__)

class AppointmentForm(FlaskForm):
    doctor_id = SelectField(_('Doctor'), validators=[DataRequired()], coerce=int)
    date = DateField(_('Date'), validators=[DataRequired()], format='%Y-%m-%d')
    time = SelectField(_('Time'), validators=[DataRequired()])
    reason = TextAreaField(_('Reason for Visit'), validators=[DataRequired(), Length(min=5, max=500)])
    appointment_type = SelectField(_('Appointment Type'), 
                                  choices=[('in-person', _('In-person')), ('telemedicine', _('Telemedicine'))],
                                  validators=[DataRequired()])
    submit = SubmitField(_('Book Appointment'))

@appointments_bp.route('/book', methods=['GET', 'POST'])
@login_required
def book():
    form = AppointmentForm()
    
    # Get the selected doctor (if any)
    doctor_id = request.args.get('doctor_id', None)
    
    # Populate doctor dropdown
    doctors = Doctor.query.filter_by(is_active=True).all()
    form.doctor_id.choices = [(d.id, f"Dr. {d.first_name} {d.last_name} - {d.specialty}") for d in doctors]
    
    # Populate available time slots (9 AM to 5 PM, 30-minute intervals)
    time_slots = []
    start_time = time(9, 0)
    for i in range(16):  # 16 half-hour slots from 9 AM to 5 PM
        slot_time = (datetime.combine(datetime.today(), start_time) + timedelta(minutes=30*i)).time()
        time_str = slot_time.strftime('%H:%M')
        time_slots.append((time_str, time_str))
    form.time.choices = time_slots
    
    # If a doctor was specified in the URL, pre-select them
    if doctor_id and form.doctor_id.choices:
        form.doctor_id.data = int(doctor_id)
    
    if form.validate_on_submit():
        # Create new appointment
        appointment = Appointment(
            patient_id=current_user.id,
            doctor_id=form.doctor_id.data,
            date=form.date.data,
            time=datetime.strptime(form.time.data, '%H:%M').time(),
            reason=form.reason.data,
            appointment_type=form.appointment_type.data,
            status='scheduled'
        )
        
        db.session.add(appointment)
        try:
            db.session.commit()
            flash(_('Your appointment has been scheduled successfully!'), 'success')
            return redirect(url_for('patients.portal'))
        except Exception as e:
            db.session.rollback()
            flash(_('There was an error booking your appointment. Please try again.'), 'danger')
    
    return render_template('appointments/book.html', title=_('Book an Appointment'), form=form)
