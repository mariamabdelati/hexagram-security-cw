from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, ValidationError
from wtforms_sqlalchemy.fields import QuerySelectField
from app.models import User, Role


class RoleForm(FlaskForm):
    
    """
    Form for admin to add or edit a role
    """
    name = StringField('Name', validators=[DataRequired()])
    description = StringField('Description', validators=[DataRequired()])
    submit = SubmitField('Submit')

class ProjectAssignForm(FlaskForm):
    """
    Form for admin to assign designer and roles to project
    """
    designer = QuerySelectField(query_factory=lambda: User.query.all(),
                                  get_label="username")
    role = QuerySelectField(query_factory=lambda: Role.query.all(),
                            get_label="name")
    submit = SubmitField('Submit')