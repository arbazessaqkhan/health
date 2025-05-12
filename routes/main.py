from flask import Blueprint, render_template, request, redirect, url_for, session, current_app
from flask_babel import gettext as _

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    return render_template('index.html', title=_('Welcome to Lifeline Hospital'))

@main_bp.route('/about')
def about():
    return render_template('about.html', title=_('About Lifeline Hospital'))

@main_bp.route('/contact')
def contact():
    return render_template('contact.html', title=_('Contact Us'))

@main_bp.route('/faq')
def faq():
    return render_template('faq.html', title=_('Frequently Asked Questions'))

@main_bp.route('/privacy')
def privacy():
    return render_template('privacy.html', title=_('Privacy Policy & HIPAA Compliance'))

@main_bp.route('/change-language/<lang_code>')
def change_language(lang_code):
    # Validate that the language code is supported
    supported_languages = current_app.config.get('LANGUAGES', ['en', 'hi', 'ur'])
    if lang_code in supported_languages:
        session['lang'] = lang_code
    return redirect(request.referrer or url_for('main.index'))
