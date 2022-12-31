from flask import abort, render_template, redirect, url_for, flash, request
from app.models import User, Project, Role, Permissions
from .forms import ProjectAssignForm
from app import db
from flask_login import login_user, logout_user, login_required, current_user
from sqlalchemy.orm import sessionmaker, relationship, load_only

from . import user

Session = sessionmaker()
db_session = Session()
   
"""
Project Managment
"""
@user.route('/projects', methods=['GET', 'POST'])
@login_required # Requires login
def projects_page():
    """
    Shows projects the user is enrolled in
    """
    
    designer_permission= Permissions.query.with_entities(Permissions.project_id) \
                        .filter(Permissions.user_id == current_user.id, Permissions.role_id != 1).all()
    designer_permission = [p.project_id for p in designer_permission]
    #print(designer_permission)
    manager_permission= Permissions.query.with_entities(Permissions.project_id).filter_by(user_id=current_user.id, role_id=2).all()
    manager_permission = [p.project_id for p in manager_permission]
    
    view_projects = Project.query.filter(Project.id.in_(designer_permission))
    managed_projects = Project.query.filter(Project.id.in_(manager_permission))
    #managed_projects = Project.
    #print(projects)
    designers = User.query
    return render_template('user/projects/projects.html', managed_projects=managed_projects, view_projects=view_projects)


@user.route('/projects/update_project', methods = ['GET', 'POST'])
@login_required # Requires admin login
def update_project():
    """
    Prompts project update popup and assigns new values to the project
    """

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