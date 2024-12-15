from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length
from .models import User, LoginRecord
from . import db, login_manager

auth_bp = Blueprint('auth', __name__)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Define the login form using Flask-WTF
class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=150)])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

# Define the register form using Flask-WTF
class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=150)])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Register')

# Helper function to extract client IP
def get_client_ip():
    if request.headers.get('X-Forwarded-For'):
        # Use the first IP in X-Forwarded-For (real client IP)
        return request.headers.get('X-Forwarded-For').split(',')[0].strip()
    return request.remote_addr  # Fallback for local dev

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        flash(f"Hello, {current_user.username}! You are already logged in.", "info")
        return redirect(url_for('main.tools'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            client_ip = get_client_ip()
            login_user(user)
            try:
                # Log the login attempt
                db.session.add(LoginRecord(user_id=user.id, ip_address=client_ip))
                db.session.commit()
                flash(f"Login successful from IP: {client_ip}", "success")
                print(f"[INFO] User {user.username} logged in from IP {client_ip}")
            except Exception as e:
                print(f"[ERROR] Failed to log login record: {e}")
            return redirect(url_for('main.tools'))
        flash('Invalid username or password. Please try again.', 'error')
    return render_template('login.html', form=form)


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        flash(f"Hello, {current_user.username}! You are already logged in.", "info")
        return redirect(url_for('main.tools'))

    form = RegisterForm()
    if form.validate_on_submit():
        if User.query.filter_by(username=form.username.data).first():
            flash('Username already exists.', 'error')
        else:
            try:
                client_ip = get_client_ip()
                new_user = User(username=form.username.data, ip_address=client_ip)
                new_user.set_password(form.password.data)
                db.session.add(new_user)
                db.session.commit()
                flash(f'Registration successful! Registered from IP: {client_ip}', 'success')
                print(f"[INFO] User {new_user.username} registered from IP {client_ip}")
                return redirect(url_for('auth.login'))
            except Exception as e:
                db.session.rollback()
                flash('An error occurred during registration. Please try again.', 'error')
                print(f"Database Error: {e}")
    return render_template('register.html', form=form)

@auth_bp.route('/logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('auth.login'))
