from flask import Blueprint, render_template, redirect, url_for, flash, request
from app.forms import RegistrationForm, LoginForm, NGORegistrationForm
from app.models import User, NGO
from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required, current_user

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            flash('Logged in successfully!', 'success')
            return redirect(url_for('main.home'))
        else:
            flash('Invalid email or password.', 'danger')
    return render_template('auth/login.html', form=form)

@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data)
        user = User(
            name=form.name.data,
            email=form.email.data,
            phone=form.phone.data,
            password=hashed_password,
            role=form.role.data
        )
        db.session.add(user)
        db.session.commit()
        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', form=form)

@auth.route('/register_ngo', methods=['GET', 'POST'])
def register_ngo():
    form = NGORegistrationForm()
    if form.validate_on_submit():
        ngo = NGO(
            name=form.name.data,
            email=form.email.data,
            location=form.location.data,
            verified=False
        )
        db.session.add(ngo)
        db.session.commit()
        flash('NGO registration submitted! Awaiting verification.', 'success')
        return redirect(url_for('main.home'))
    return render_template('auth/register_ngo.html', form=form)

@auth.route('/ngo/register', methods=['GET', 'POST'])
def ngo_register():
    form = NGORegistrationForm()
    if form.validate_on_submit():
        # Create user with role 'ngo'
        user = User(
            name=form.name.data,
            email=form.email.data,
            phone='',
            password=generate_password_hash(form.password.data),
            role='ngo'
        )
        db.session.add(user)
        db.session.commit()
        # Create NGO profile linked to this user
        ngo = NGO(
            name=form.name.data,
            email=form.email.data,
            location=form.location.data,
            verified=False
        )
        db.session.add(ngo)
        db.session.commit()
        flash('NGO registration successful! Please log in.', 'success')
        return redirect(url_for('auth.login'))
    return render_template('auth/ngo_register.html', form=form)

@auth.route('/profile')
@login_required
def profile():
    return render_template('user/profile.html', user=current_user)

@auth.route('/ngo_profile')
@login_required
def ngo_profile():
    ngo = NGO.query.filter_by(email=current_user.email).first()
    return render_template('ngo/ngo_profile.html', ngo=ngo)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('main.home')) 