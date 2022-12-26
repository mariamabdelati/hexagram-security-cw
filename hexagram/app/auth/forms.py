from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import Length, EqualTo, Email, DataRequired, ValidationError, Regexp
from app.models import User
"""
Formal Verification
"""
class RegistrationForm(FlaskForm):
    """
    Registration Form object
    """
    def validate_username(self, username_to_check):
        """
        Unique username validation
        """
        user = User.query.filter_by(username=username_to_check.data).first()
        if user:
            raise ValidationError('Username already exists! Please try a different username')

    def validate_email_address(self, email_address_to_check):
        """
        Unique email validation
        """
        email = User.query.filter_by(email_address=email_address_to_check.data).first()
        if email:
            raise ValidationError('Email Address already exists! Please try a different email address')

    # Variables needed for registration
    username = StringField(label='Username:', validators=[Length(min=3, max=30), DataRequired()])
    email = StringField(label='Email Address:', validators=[Email(), DataRequired()])
    department = StringField(label='Department:', validators=[DataRequired()])
    password1 = PasswordField(label='Password:', validators=[Length(min=8), DataRequired(), Regexp(regex="^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,}$", message="Minimum eight characters, at least one uppercase letter, one lowercase letter and one symbol, and one number")])
    password2 = PasswordField(label='Confirm Password:', validators=[EqualTo('password1'), DataRequired()])
    submit = SubmitField(label='Create Account')

class LoginForm(FlaskForm):
    """
    Login Form object
    """
    # Data needed to login
    username = StringField(label='User Name:', validators=[DataRequired()])
    password = PasswordField(label='Password:', validators=[DataRequired()])
    submit = SubmitField(label='Sign in')