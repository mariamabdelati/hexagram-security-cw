from app import db, login_manager
from app import bcrypt
from flask_login import UserMixin
"""
Formal Modelling

Models represent objects in Petri Nets
"""
@login_manager.user_loader
def load_user(admin_id):
    """
    Returns the current logged in admin
    """
    return Admin.query.get(int(admin_id))


class Admin(db.Model, UserMixin):
    """
    Create Admin object model
    """
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(length=30), nullable=False, unique=True)
    email = db.Column(db.String(length=50), nullable=False, unique=True)
    admin_code = db.Column(db.String(length=15), nullable=False)
    password_hash = db.Column(db.String(length=60), nullable=False)

    @property
    def password(self):
        """
        Returns the password
        """
        return self.password

    @password.setter
    def password(self, plain_text_password):
        """
        Hash password
        """
        self.password_hash = bcrypt.generate_password_hash(plain_text_password).decode('utf-8')

    def check_password_correction(self, attempted_password):
        """
        Compare hashed password with the attempted password
        """
        return bcrypt.check_password_hash(self.password_hash, attempted_password)


class Designer(db.Model):
    """
    Create designer object model
    """
    id = db.Column(db.Integer(), primary_key=True)

    name = db.Column(db.String(length=30), nullable=False, unique=True)
    department = db.Column(db.String(length=20), nullable=False)
    managed_project = db.Column(db.Integer(), nullable=False)


class Project(db.Model):
    """
    Create Project object model
    """
    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String(length=30), nullable=False, unique=True)
    hours = db.Column(db.String(length=20), nullable=False)
    status = db.Column(db.String(length=20), nullable=False)
    project_details = db.Column(db.String(), nullable=False)
    #check_system = db.Column(db.String(length=2), nullable=False)
    project_start_date = db.Column(db.String(), nullable=False)
    estimated_time = db.Column(db.Integer(), nullable=False)
    assigned_designer = db.Column(db.String(), nullable=False)
    #man_hours = db.Column(db.Integer(), nullable=False)
    last_updated = db.Column(db.String(), nullable=False)

    def assign(self, designer):
        """
        Assigns technician to the ac maintenance
        """
        designer.managed_project = self.id
        self.assigned_designer = designer.name
        db.session.commit() # Write changes to the database

    def remove_assign(self, designer):
        """
        Removes the assigned technician from the ac maintenance
        """
        designer.managed_project = None
        self.assigned_designer = None
        db.session.commit() # Write changes to the database
