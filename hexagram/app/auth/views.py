from flask import render_template, redirect, url_for, flash, request, session
from app.models import User, Project
from app.auth.forms import RegistrationForm, LoginForm
from app import db
from flask_login import login_user, logout_user, login_required, current_user
from . import auth

from app import limiter

@auth.route('/registration', methods=['GET', 'POST'])
def registration_page():
    """
    Loads registration page, sends new admin data to the database
    """
    register_form = RegistrationForm() # Loads Registration Form
    # Assigns data input on the form to Admin
    if register_form.validate_on_submit():
        user_to_create = User(username=register_form.username.data,
                               first_name=register_form.first_name.data,    
                               last_name=register_form.last_name.data,
                               department=register_form.department.data,
                               email=register_form.email.data,
                               password=register_form.password1.data)
        
        db.session.add(user_to_create)
        db.session.commit()
        login_user(user_to_create)
            
        flash(f"Your account has been created successfully! You are now logged in as {user_to_create.username}", category='success')
        return redirect(url_for('user.projects_page'))

    # Shows user if there are any error with registration
    if register_form.errors != {}: #If there are not errors from the validations
        for err_msg in register_form.errors.values():
            flash(f'An error has been encountered creating your account: {err_msg}', category='danger')

    return render_template('authentication/registration.html', form=register_form)

@auth.route('/login', methods=['GET', 'POST'])
@limiter.limit("5 per minute", error_message="You have exceeded the maximum number of login attempts. Please try again in 1 minute.")
def login_page():
    """
    Loads login page and makes sure username and password match
    """
    #TODO function to validate password and username
    form = LoginForm()
    if form.validate_on_submit():
        username=form.username.data
        attempted_user = User.query.filter_by(username=username).first()
        if attempted_user and attempted_user.check_password_correction(
                attempted_password=form.password.data
        ):
            session["name"] = username
            login_user(attempted_user) # If username and password match login happens
            if attempted_user.is_admin:
                flash(f'Success! You are logged in as: {attempted_user.username}', category='success')
                return redirect(url_for('admin.projects_page'))
            else:
                return redirect(url_for('user.projects_page'))    
        else:
            flash('The username or password is incorrect. Please make sure you have entered the correct information', category='danger')

    return render_template('authentication/login.html', form=form)

@auth.route('/logout')
@login_required # Requires admin login
def logout_page():
    """
    Logout of current user
    """

    # Function that logs out the user
    session["name"] = None
    logout_user()
    flash("Logged out successfully!", category='info')
    return redirect(url_for("home.home_page"))