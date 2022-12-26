from flask import abort, render_template, redirect, url_for, flash, request
from app.models import User, Project, Role
from .forms import ProjectAssignForm
from app import db
from flask_login import login_user, logout_user, login_required, current_user

from . import admin

def check_admin():
    """
    Prevent non-admins from accessing the page
    """
    if not current_user.is_admin:
        abort(403)

"""
Admin Account Managment
"""
@admin.route('/update_account', methods = ['GET', 'POST'])
@login_required # Requires admin login
def update():
    """
    Prompts update popup and assigns new values to the current logged in user
    """
    check_admin()

    # New values
    new_email = request.form.get('email').lower()
    new_username = request.form.get('username').lower()

    if new_email != '' and new_username != '':
        # Assign to the current user
        current_user.email = new_email
        current_user.username = new_username

        # Write changes in the database
        db.session.commit()
        flash("User data has been successfully updated", category='success')
        return redirect(url_for('home.home_page'))
    else:
        flash("User data can not be empty", category='danger')
        return redirect(url_for('home.home_page'))


@admin.route('/delete', methods=['GET', 'POST'])
@login_required # Requires admin login
def delete():
    """
    Prompts delete popup to make sure user wants to delete account
    """
    check_admin()
    # Function to delete current user from the database
    db.session.delete(current_user)

    # Write changes in the database
    db.session.commit()
    return redirect(url_for('home.home_page'))

"""
User Management Routes
"""
@admin.route('/designers', methods=['GET', 'POST'])
@login_required  # Requires admin login
def designers_page():
    """
    Shows all designer available
    """
    check_admin()

    # Shows the designer list and assigned projects
    if request.method == "GET":
        designers = User.query
        projects = Project.query
        return render_template('admin/designers/designers.html', designers=designers, projects=projects)

@admin.route('/designers/add_designer', methods=['GET', 'POST'])
@login_required # Requires admin login
def add_designer():
    """
    Route to create a new designer with validation
    """
    check_admin()

    # Assigns data input on the form to Designer
    designer_to_create = User(name=request.form.get('name').lower(),                            
                                  department=request.form.get('department').lower(),
                                  managed_project=None)

    if User.query.filter_by(name=designer_to_create.name).first(): # Checks if designer already exists
        flash(f'Designer already exists', category='danger')
        return redirect(url_for('admin.designers_page'))
    else:
        if designer_to_create.name != "" and designer_to_create.department != "":
            db.session.add(designer_to_create)
            db.session.commit()
            flash(f"Designer Has Been Successfully Added!", category='success')
            return redirect(url_for('admin.designers_page'))
        flash(f"Designer Entries can not be empty!", category='danger')
        return redirect(url_for('admin.designers_page'))

@admin.route('/designers/delete_designer', methods=['GET', 'POST'])
@login_required # Requires admin login
def delete_designer():
    """
    Prompts delete popup to make sure admin wants to delete designer
    """
    check_admin()

    designer_name = request.form.get('name')
    current_designer = User.query.filter_by(name=designer_name).first()

    # Function to delete current designer from the database
    db.session.delete(current_designer)

    # Write changes in the database
    db.session.commit()
    return redirect(url_for('admin.designers_page'))

"""
Role Management Routes
"""
@admin.route('/roles', methods=['GET', 'POST'])
@login_required  # Requires admin login
def roles_page():
    """
    Shows all roles available
    """
    check_admin()

    # Shows the role list
    if request.method == "GET":
        roles = Role.query
        return render_template('admin/roles/roles.html', roles=roles)

@admin.route('/roles/add_role', methods=['GET', 'POST'])
@login_required # Requires admin login
def add_role():
    """
    Route to create a new role with validation
    """
    check_admin()

    # Assigns data input on the form to Role
    role_to_create = Role(name=request.form.get('name').lower(),
                                  description=request.form.get('description').lower())

    if Role.query.filter_by(name=role_to_create.name).first(): # Checks if Role already exists
        flash(f'Role already exists', category='danger')
        return redirect(url_for('admin.roles_page'))
    else:
        if Role.name != "" and Role.description != "":
            db.session.add(role_to_create)
            db.session.commit()
            flash(f"Role Has Been Successfully Added!", category='success')
            return redirect(url_for('admin.roles_page'))
        flash(f"Roles Entries can not be empty!", category='danger')
        return redirect(url_for('admin.roles_page'))

@admin.route('/roles/delete_role', methods=['GET', 'POST'])
@login_required # Requires admin login
def delete_role():
    """
    Prompts delete popup to make sure admin wants to delete role
    """
    check_admin()

    role_name = request.form.get('name')
    current_role = Role.query.filter_by(name=role_name).first()

    # Function to delete current role from the database
    db.session.delete(current_role)

    # Write changes in the database
    db.session.commit()
    return redirect(url_for('admin.roles_page'))
   
"""
Project Managment
"""
@admin.route('/projects', methods=['GET', 'POST'])
@login_required # Requires admin login
def projects_page():
    """
    Shows all available projects
    """
    check_admin()

    # Shows the Projects list
    if request.method == "GET":
        projects = Project.query
        designers = User.query
        return render_template('admin/projects/projects.html', designers=designers, projects=projects)

@admin.route('/projects/add_project', methods=['GET', 'POST'])
@login_required # Requires admin login
def add_project():
    """
    Route to create a new Project with validation
    """
    check_admin()

    # Assigns data input on the form to Project
    project_to_create = Project(name=request.form.get('name'),
                                  hours=request.form.get('hours'),
                                  status="open",
                                  project_details=None,
                                  project_start_date=None,
                                  estimated_time=None,
                                  assigned_designer=None)

    if Project.query.filter_by(name=project_to_create.name).first(): # Checks if project already exists
        flash(f'Project already exists', category='danger')
        return redirect(url_for('admin.projects_page'))
    else:
        if project_to_create.name != "" and project_to_create.hours != "":
            db.session.add(project_to_create)
            db.session.commit()
            flash(f"Project has been created successfully!", category='success')
            return redirect(url_for('admin.projects_page'))
        flash(f"Project entries can't be empty!", category='danger')
        return redirect(url_for('admin.projects_page'))

@admin.route('/projects/update_project', methods = ['GET', 'POST'])
@login_required # Requires admin login
def update_project():
    """
    Prompts project update popup and assigns new values to the project
    """
    check_admin()

    # New values
    new_status = request.form.get('status')
    #new_check = request.form.get('check')
    new_project_details = request.form.get('project_details')
    #new_man_hours = request.form.get('man_hours')
    new_project_start_date = request.form.get('project_start_date')
    new_estimated_time = request.form.get('estimated_time')
    assigned_designer = request.form.get('assigned_designer')
    project_name = request.form.get('name')
    last_update = request.form.get('project_start_date')

    designer_assigned = User.query.filter_by(id=assigned_designer).first()

    # Assign to the current project
    current_project = Project.query.filter_by(name=project_name).first()
    if new_project_start_date != "" and new_estimated_time != '0':
        if new_status == "open": # Checks if it is available or in maintenance
            current_project.status = new_status
            current_project.assigned_designer = None
            current_project.project_details = None
            #current_project.man_hours = None
            current_project.project_start_date = None
            current_project.estimated_time = None
            current_project.remove_assign(designer_assigned)
            designer_assigned.managed_project = None
        else:
            current_project.status = new_status
            current_project.project_details = new_project_details
            #current_project.check_system = new_check
            #current_project.man_hours = new_man_hours
            current_project.project_start_date = new_project_start_date
            current_project.estimated_time = new_estimated_time
            current_project.assign(designer_assigned)
            current_project.last_updated = last_update
            #current_project.last_maintenance = f"{new_check} on {last_update}"

        # Write changes in the database
        db.session.commit()
        flash("Project Has Been Successfully Assigned", category='success')
        return redirect(url_for('admin.projects_page'))
    else:
        flash("Insert a valid date and time for the maintenance", category='danger')
        return redirect(url_for('admin.projects_page'))

@admin.route('/projects/delete_project', methods=['GET', 'POST'])
@login_required # Requires admin login
def delete_project():
    """
    Prompts delete popup to make sure admin wants to delete project
    """
    project_name = request.form.get('name')
    current_project = Project.query.filter_by(name=project_name).first()

    # Function to delete current project from the database
    db.session.delete(current_project)

    # Write changes in the database
    db.session.commit()
    return redirect(url_for('admin.projects_page'))

"""
Assignment to Projects and Permissions
"""
# @admin.route('/projects/assign_project', methods=['GET', 'POST'])
# @login_required
# def assign_project(id):
#     """
#     Assign a designer and role to an project
#     """
#     check_admin()

#     project = Project.query.get_or_404(id)

#     form = Project(obj=project)
#     if form.validate_on_submit():
#         project. = form.department.data
#         employee.role = form.role.data
#         db.session.add(employee)
#         db.session.commit()
#         flash('You have successfully assigned a department and role.')

#         # redirect to the roles page
#         return redirect(url_for('admin.list_employees'))

#     return render_template('admin/employees/employee.html',
#                            employee=employee, form=form,
#                            title='Assign Employee')