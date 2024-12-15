from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    return redirect(url_for('auth.login'))

@main_bp.route('/tools')
@login_required
def tools():
    return render_template('tools.html')
