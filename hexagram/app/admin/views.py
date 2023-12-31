from flask import abort, render_template, redirect, url_for, flash, request
from app.models import User, Project, Role, Permissions
from .forms import ProjectAssignForm
from app import db
from flask_login import login_user, logout_user, login_required, current_user
from flask import render_template, redirect, url_for, flash, request, session
from app.models import User, Project
from app import db
from flask_login import login_user, logout_user, login_required, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import Length, EqualTo, Email, DataRequired, ValidationError, Regexp
from app.models import User

from app import limiter
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


@admin.route('/delete_account', methods=['GET', 'POST'])
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
    if request.method == "GET":
        designers = User.query
        projects = Project.query
        return render_template('admin/designers/designers.html', designers=designers, projects=projects)

@admin.route('/designers/delete_designer', methods=['GET', 'POST'])
@login_required # Requires admin login
def delete_designer():
    """
    Prompts delete popup to make sure admin wants to delete designer
    """
    check_admin()

    designer_name = request.form.get('name')
    current_designer = User.query.filter_by(username=designer_name).first()
    #print(current_designer.id)

    permissions= Permissions.query.with_entities(Permissions.user_id).filter_by(user_id=current_designer.id).all()
    permissions = [p.user_id for p in permissions]
    
    if len(permissions) == 0:
        # Function to delete current designer from the database
        db.session.delete(current_designer)
        # Write changes in the database
        db.session.commit()
        flash(f"User was successfully deleted!", category='success')
    else:
        flash(f"User is assigned to project!", category='danger')
    
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

    if current_role.id == 1 | current_role.id == 2:
        flash(f"Main user roles cannot be deleted!", category='danger')
    else:

        permissions= Permissions.query.with_entities(Permissions.role_id).filter_by(role_id=current_role.id).all()
        permissions = [p.role_id for p in permissions]
    
        if len(permissions) == 0:
            # Function to delete current role from the database
            db.session.delete(current_role)
            #Write changes in the database
            db.session.commit()
        else:
            flash(f"Roles assigned to user!", category='danger')
   
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
                                  last_updated= None)

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
    new_project_details = request.form.get('project_details')
    new_project_start_date = request.form.get('project_start_date')
    new_estimated_time = request.form.get('estimated_time')
    project_name = request.form.get('name')
    last_update = request.form.get('project_start_date')


    # Assign to the current project
    current_project = Project.query.filter_by(name=project_name).first()
    if new_project_start_date != "" and new_estimated_time != '0':
        if new_status == "open": # Checks if it is available or in maintenance
            current_project.status = new_status
        else:
            current_project.status = new_status
            current_project.project_details = new_project_details
            current_project.project_start_date = new_project_start_date
            current_project.estimated_time = new_estimated_time
            current_project.last_updated = last_update
            

        # Write changes in the database
        db.session.commit()
        flash("Project Has Been Successfully Updated", category='success')
        return redirect(url_for('admin.projects_page'))
    else:
        flash("Insert a valid date and time for the project", category='danger')
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
    flash("Project Has Been Successfully Deleted", category='success')
    return redirect(url_for('admin.projects_page'))

"""
Assignment to Projects and Permissions
"""
@admin.route('/projects/assign_project/<int:id>', methods=['GET', 'POST'])
@login_required
def assign_project(id):
    """
    Assign a designer and role to an project
    """
    check_admin()

    project = Project.query.get_or_404(id)
    project_permission= Permissions.query.with_entities(Permissions.user_id).filter(Permissions.project_id == project.id).all()
    project_permission = [p.user_id for p in project_permission]
    
    query = User.query.filter(User.id.notin_(project_permission), User.is_admin.like(0), User.id != current_user.id).all()
    
    if not query:
        flash('All designers are currently assigned to this project', category='danger')
        return redirect(url_for('admin.projects_page'))
    
    form = ProjectAssignForm(obj=project)
    form.designer.query = query
    
    permission = Permissions()
    if form.validate_on_submit():
        permission.assign(project=project, designer=form.designer.data, role=form.role.data)
       
        flash('You have successfully assigned the project to the user.', category='success')

        # redirect to the roles page
        return redirect(url_for('admin.projects_page'))

    return render_template('admin/projects/project_assign.html',
                           project=project, form=form,
                           title='Assign Project')