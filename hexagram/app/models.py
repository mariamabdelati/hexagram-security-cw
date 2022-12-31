from app import db, login_manager
from app import bcrypt
from flask_login import UserMixin
"""
Formal Modelling

Models represent objects in Petri Nets
"""
@login_manager.user_loader
def load_user(user_id):
    """
    Returns the current logged in user
    """
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    """
    Create User object model
    """
    id = db.Column(db.Integer(), primary_key=True)
    email = db.Column(db.String(length=50), nullable=False, unique=True)
    username = db.Column(db.String(length=30), nullable=False, unique=True)
    first_name = db.Column(db.String(60), index=True)
    last_name = db.Column(db.String(60), index=True)
    password_hash = db.Column(db.String(length=60), nullable=False)
    department = db.Column(db.String(length=20), nullable=False)
    permission = db.relationship('Permissions', backref='user')
    is_admin = db.Column(db.Boolean, default=False)

    @property
    def password(self):
        # Preventing password from being accessed      
        raise AttributeError('Password is not a readable attribute.')

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

    def __repr__(self):
        return '<User: {}>'.format(self.username)

class Project(db.Model):
    """
    Create Project object model
    """
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(length=30), nullable=False, unique=True)
    hours = db.Column(db.String(length=20), nullable=False)
    status = db.Column(db.String(length=20), nullable=False)
    project_details = db.Column(db.String(), nullable=False)
    project_start_date = db.Column(db.String(), nullable=False)
    estimated_time = db.Column(db.Integer(), nullable=False)
    last_updated = db.Column(db.String(), nullable=False)
    permission = db.relationship('Permissions', backref='project')

    def __repr__(self):
        return '<Project: {}>'.format(self.name)


class Permissions(db.Model):
    """
    Create permissions object model
    """
    id = db.Column(db.Integer(), primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'))

    def assign(self, project, designer, role):
        self.project_id = project.id
        self.user_id = designer.id
        self.role_id = role.id
        db.session.add(self) # Add new record to the database
        db.session.commit() # Write changes to the database

    def remove_assign(self, designer):
        """
        Removes the assigned designer from the project
        """
        self.project_id = None
        self.user_id = None
        self.role_id = None
        db.session.commit() # Write changes to the database

class Role(db.Model):
    """
    Create role object model
    """
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(length=60), nullable=False, unique=True)
    description = db.Column(db.String(200))
    permission = db.relationship('Permissions', backref='role')

    def __repr__(self):
        return '<Role: {}>'.format(self.name)