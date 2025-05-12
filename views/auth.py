from flask import Blueprint, render_template, redirect, url_for, flash, request, session
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from models import User, db
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, EmailField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError
from datetime import datetime
from flask_babel import gettext as _

auth_bp = Blueprint('auth', __name__)

class LoginForm(FlaskForm):
    email = EmailField(_('Email'), validators=[DataRequired(), Email()])
    password = PasswordField(_('Password'), validators=[DataRequired()])
    remember_me = BooleanField(_('Remember Me'))
    submit = SubmitField(_('Sign In'))

class RegistrationForm(FlaskForm):
    username = StringField(_('Username'), validators=[DataRequired(), Length(min=4, max=64)])
    email = EmailField(_('Email'), validators=[DataRequired(), Email()])
    first_name = StringField(_('First Name'), validators=[DataRequired(), Length(min=2, max=64)])
    last_name = StringField(_('Last Name'), validators=[DataRequired(), Length(min=2, max=64)])
    password = PasswordField(_('Password'), validators=[DataRequired(), Length(min=8)])
    password2 = PasswordField(
        _('Repeat Password'), validators=[DataRequired(), EqualTo('password')])
    phone = StringField(_('Phone Number'), validators=[Length(max=20)])
    submit = SubmitField(_('Register'))

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError(_('Please use a different username.'))

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError(_('Please use a different email address.'))

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home.index'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None or not user.check_password(form.password.data):
            flash(_('Invalid email or password'), 'danger')
            return redirect(url_for('auth.login'))
        
        login_user(user, remember=form.remember_me.data)
        
        # Set user's preferred language
        if user.preferred_language:
            session['language'] = user.preferred_language
        
        next_page = request.args.get('next')
        if not next_page or next_page.startswith('/'):
            next_page = url_for('home.index')
        
        flash(_('You have successfully logged in!'), 'success')
        return redirect(next_page)
    
    return render_template('patients/login.html', title=_('Sign In'), form=form)

@auth_bp.route('/logout')
def logout():
    logout_user()
    flash(_('You have been logged out.'), 'info')
    return redirect(url_for('home.index'))

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home.index'))
    
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(
            username=form.username.data,
            email=form.email.data,
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            phone=form.phone.data,
            role='patient'
        )
        user.set_password(form.password.data)
        
        db.session.add(user)
        try:
            db.session.commit()
            flash(_('Congratulations, you are now a registered user!'), 'success')
            return redirect(url_for('auth.login'))
        except Exception as e:
            db.session.rollback()
            flash(_('There was an error creating your account. Please try again.'), 'danger')
    
    return render_template('patients/login.html', title=_('Register'), form=form, register=True)
