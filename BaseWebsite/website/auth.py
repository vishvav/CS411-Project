from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')  # type: ignore
        password = request.form.get('password')  # type: ignore
        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Login success.', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password. Try again.', category='error')
        else:
            flash('Account not found.', category='error')

    return render_template("login.jinja", user=current_user)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        # Get the form data
        email = request.form.get('email')  # type: ignore
        first_name = request.form.get('firstName')  # type: ignore
        password1 = request.form.get('password1')  # type: ignore
        password2 = request.form.get('password2')  # type: ignore

        # Check if email already exists, flash error if it does
        user = User.query.filter_by(email=email).first()
        if user:
            flash('Acccount already exists.', category='error')
        # if length of email is less than 7, flash error
        elif len(email) < 7:
            flash('Email must be greater than 7 characters.', category='error')
        # if length of first name is less than 2, flash error
        elif len(first_name) < 2:
            flash('First name must be greater than 1 character.', category='error')
        # Check if passwords match, flash error if they don't
        elif password1 != password2:
            flash('Passwords don\'t match.', category='error')
        # Check if password is less than 7 characters, flash error if it is
        elif len(password1) < 7:
            flash('Password must be at least 7 characters.', category='error')
        # If all checks pass, add user to database
        else:
            # Create new user and hash password
            new_user = User(email=email, first_name=first_name, password=generate_password_hash(password1, method='sha256'))
            # Add user to database
            db.session.add(new_user)
            db.session.commit()
            # Log user in with flask login function
            login_user(new_user, remember=True)
            flash('Account created.', category='success')
            # Redirect to home page
            return redirect(url_for('views.home'))

    return render_template("sign_up.jinja", user=current_user)
