from flask import Blueprint, render_template, flash, redirect, url_for, request
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, EmailField, SubmitField
from wtforms.validators import DataRequired, Email, Length
from flask_babel import gettext as _
import logging

contact_bp = Blueprint('contact', __name__)

class ContactForm(FlaskForm):
    name = StringField(_('Your Name'), validators=[DataRequired(), Length(min=2, max=100)])
    email = EmailField(_('Email Address'), validators=[DataRequired(), Email()])
    phone = StringField(_('Phone Number'), validators=[Length(max=20)])
    subject = StringField(_('Subject'), validators=[DataRequired(), Length(min=2, max=100)])
    message = TextAreaField(_('Message'), validators=[DataRequired(), Length(min=10, max=1000)])
    submit = SubmitField(_('Send Message'))

@contact_bp.route('/', methods=['GET', 'POST'])
def index():
    form = ContactForm()
    
    if form.validate_on_submit():
        # In a real application, you would send an email or save to database
        # For this example, we'll just log the inquiry
        logging.info(f"Contact form submission: {form.name.data} ({form.email.data}): {form.subject.data}")
        
        flash(_('Thank you for contacting us! We will get back to you shortly.'), 'success')
        return redirect(url_for('contact.index'))
    
    return render_template('contact.html', title=_('Contact Us'), form=form)
