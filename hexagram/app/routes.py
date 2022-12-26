from app import app
from flask import render_template, redirect, url_for, flash, request
from app.models import Admin, Designer, Project
from app.authentication.forms import RegistrationForm, LoginForm
from app import db
from flask_login import login_user, logout_user, login_required, current_user

"""
Formal Modelling

Routes represent a communication medium and the rendered HTML files are the events
"""
@app.route('/') # Route is the same as home page
@app.route('/home')
def home_page():
    """
    Loads home page
    """
    return render_template('home.html')

@app.route('/about')
def about_page():
    """
    Loads about page
    """
    return render_template('about.html')

@app.route('/update_account', methods = ['GET', 'POST'])
@login_required # Requires admin login
def update():
    """
    Prompts update popup and assigns new values to the current logged in user
    """

    # New values
    new_email = request.form.get('email')
    new_username = request.form.get('username')

    if new_email != '' and new_username != '':
        # Assign to the current user
        current_user.email = new_email
        current_user.username = new_username

        # Write changes in the database
        db.session.commit()
        flash("User data has been successfully updated", category='success')
        return redirect(url_for('home_page'))
    else:
        flash("User data can not be empty", category='danger')
        return redirect(url_for('home_page'))


@app.route('/delete', methods=['GET', 'POST'])
@login_required # Requires admin login
def delete():
    """
    Prompts delete popup to make sure user wants to delete account
    """

    # Function to delete current user from the database
    db.session.delete(current_user)

    # Write changes in the database
    db.session.commit()
    return redirect(url_for('home_page'))

@app.errorhandler(404)
# Inbuilt function which takes error as parameter
def not_found(e):
    """
    Handles 404 error
    """
    return render_template("errors/404.html")

@app.errorhandler(410)
# Inbuilt function which takes error as parameter
def not_found(e):
    """
    Handles 410 error
    """
    return render_template("errors/404.html")

@app.errorhandler(500)
# Inbuilt function which takes error as parameter
def not_found(e):
    """
    Handles 500 error
    """
    return render_template("errors/500.html")

@app.errorhandler(403)
# Inbuilt function which takes error as parameter
def not_found(e):
    """
    Handles 403 error
    """
    return render_template("errors/403.html")


# @app.route('/projects', methods=['GET', 'POST'])
# @login_required # Requires admin login
# def projects_page():
#     """
#     Shows all available projects
#     """

#     # Shows the Projects list
#     if request.method == "GET":
#         project = Project.query
#         designer = Designer.query
#         return render_template('projects.html', designer=designer, proj=project)

# @app.route('/add_project', methods=['GET', 'POST'])
# @login_required # Requires admin login
# def add_project():
#     """
#     Route to create a new Project with validation
#     """
#     # Assigns data input on the form to Project
#     project_to_create = Project(title=request.form.get('title'),
#                                   hours=request.form.get('hours'),
#                                   status="Open",
#                                   project_details=None,
#                                   project_start_date=None,
#                                   estimated_time=None,
#                                   assigned_designer=None)

#     if Project.query.filter_by(title=project_to_create.title).first(): # Checks if project already exists
#         flash(f'Project already exists', category='danger')
#         return redirect(url_for('projects_page'))
#     else:
#         if project_to_create.aircon != "" and project_to_create.hours != "":
#             db.session.add(project_to_create)
#             db.session.commit()
#             flash(f"Project has been created successfully!", category='success')
#             return redirect(url_for('projects_page'))
#         flash(f"Project entries can't be empty!", category='danger')
#         return redirect(url_for('projects_page'))

# @app.route('/update_project', methods = ['GET', 'POST'])
# @login_required # Requires admin login
# def update_project():
#     """
#     Prompts project update popup and assigns new values to the project
#     """
#     # New values
#     new_status = request.form.get('status')
#     #new_check = request.form.get('check')
#     new_project_details = request.form.get('project_details')
#     #new_man_hours = request.form.get('man_hours')
#     new_project_start_date = request.form.get('project_start_date')
#     new_estimated_time = request.form.get('estimated_time')
#     assign_designer = request.form.get('assign')
#     project_title = request.form.get('title')
#     last_update = request.form.get('project_start_date')

#     designer_assigned = Designer.query.filter_by(id=assign_designer).first()

#     # Assign to the current project
#     current_project = Project.query.filter_by(title=project_title).first()
#     if new_project_start_date != "" and new_estimated_time != '0':
#         if new_status == "Open": # Checks if it is available or in maintenance
#             current_project.status = new_status
#             current_project.assigned_designer = None
#             current_project.project_details = None
#             #current_project.man_hours = None
#             current_project.project_start_date = None
#             current_project.estimated_time = None
#             current_project.remove_assign(designer_assigned)
#             designer_assigned.managed_project = None
#         else:
#             current_project.status = new_status
#             current_project.project_details = new_project_details
#             #current_project.check_system = new_check
#             #current_project.man_hours = new_man_hours
#             current_project.project_start_date = new_project_start_date
#             current_project.estimated_time = new_estimated_time
#             current_project.assign(designer_assigned)
#             current_project.last_updated = last_update
#             #current_project.last_maintenance = f"{new_check} on {last_update}"

#         # Write changes in the database
#         db.session.commit()
#         flash("Project Has Been Successfully Assigned", category='success')
#         return redirect(url_for('projects_page'))
#     else:
#         flash("Insert a valid date and time for the maintenance", category='danger')
#         return redirect(url_for('projects_page'))

# @app.route('/delete_project', methods=['GET', 'POST'])
# @login_required # Requires admin login
# def delete_project():
#     """
#     Prompts delete popup to make sure admin wants to delete project
#     """
#     project_title = request.form.get('title')
#     current_project = Project.query.filter_by(title=project_title).first()

#     # Function to delete current project from the database
#     db.session.delete(current_project)

#     # Write changes in the database
#     db.session.commit()
#     return redirect(url_for('projects_page'))

# @app.route('/designer', methods=['GET', 'POST'])
# @login_required  # Requires admin login
# def designers_page():
#     """
#     Shows all designer available
#     """
#     # Shows the designer list and assigned projects
#     if request.method == "GET":
#         designer = Designer.query
#         project = Project.query
#         return render_template('designer.html', designer=designer, project=project)

# @app.route('/add_designer', methods=['GET', 'POST'])
# @login_required # Requires admin login
# def add_designer():
#     """s
#     Route to create a new designer with validation
#     """

#     # Assigns data input on the form to Designer
#     designer_to_create = Designer(name=request.form.get('name'),
#                                   department=request.form.get('department'),
#                                   managed_project=None)

#     if Designer.query.filter_by(name=designer_to_create.name).first(): # Checks if designer already exists
#         flash(f'Designer already exists', category='danger')
#         return redirect(url_for('designers_page'))
#     else:
#         if designer_to_create.name != "" and designer_to_create.department != "":
#             db.session.add(designer_to_create)
#             db.session.commit()
#             flash(f"Designer Has Been Successfully Added!", category='success')
#             return redirect(url_for('designers_page'))
#         flash(f"Designer Entries can not be empty!", category='danger')
#         return redirect(url_for('designers_page'))

# @app.route('/delete_designer', methods=['GET', 'POST'])
# @login_required # Requires admin login
# def delete_designer():
#     """
#     Prompts delete popup to make sure admin wants to delete designer
#     """
#     designer_name = request.form.get('name')
#     current_designer = Designer.query.filter_by(name=designer_name).first()

#     # Function to delete current designer from the database
#     db.session.delete(current_designer)

#     # Write changes in the database
#     db.session.commit()
#     return redirect(url_for('designers_page'))