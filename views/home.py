from flask import Blueprint, render_template, session, redirect, url_for, request
from flask_babel import gettext as _

home_bp = Blueprint('home', __name__)

@home_bp.route('/')
def index():
    return render_template('home.html', title=_('Welcome to Lifeline Hospital'))

@home_bp.route('/about')
def about():
    return render_template('about.html', title=_('About Lifeline Hospital'))

@home_bp.route('/facilities')
def facilities():
    return render_template('facilities.html', title=_('Our Facilities'))

@home_bp.route('/faq')
def faq():
    from models import FAQ
    faqs = FAQ.query.order_by(FAQ.display_order).all()
    return render_template('faq.html', title=_('Frequently Asked Questions'), faqs=faqs)

@home_bp.route('/privacy')
def privacy():
    return render_template('privacy.html', title=_('Privacy Policy & HIPAA Compliance'))

@home_bp.route('/set-language/<language>')
def set_language(language):
    session['language'] = language
    return redirect(request.referrer or url_for('home.index'))
