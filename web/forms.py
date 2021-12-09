from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField
from wtforms.fields.html5 import DateField, IntegerField
from wtforms.validators import DataRequired, InputRequired, Regexp, Length, Email, EqualTo, ValidationError
from web.models import User
from flask_admin.form import DateTimePickerWidget


# registration form
class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=15)])
    email = StringField('Email address', validators=[DataRequired(), Email(), Length(min=6, max=35)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8, max=200)])
    password_confirm = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign up')

    # checking whether the username has been already taken or not
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError(
                'This username already exists. Please choose another one or log in.')

    # checking if the email is already used or not
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError(
                'There is a SuggestMe account associated with that email. Please use another email or log in.')

# login form
class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class AddTasksForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(min=2, max=15)])
    description = StringField('Description', validators=[DataRequired(), Length(min=2, max=60)])
    deadline = DateField('DatePicker', format='%Y-%m-%d', validators=[DataRequired()])
    submit = SubmitField('Add tasks')

class AddTimerForm(FlaskForm):
    focus = IntegerField('Focus', validators=[DataRequired(), Length(min=1, max=3)])
    rest = IntegerField('Rest', validators=[DataRequired(), Length(min=1, max=2)])
    submit = SubmitField('Start timer')


# reset form
class ResetForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Length(min=6, max=35), Email()])
    submit = SubmitField('Send Email')

# reset password form
class ResetPasswordForm(FlaskForm):
    new_password = PasswordField('Password', validators=[
                                 DataRequired(), Length(min=8, max=200)])
    new_password2 = PasswordField('Confirm Password', validators=[
                                  DataRequired(), Length(min=8, max=200), EqualTo('new_password')])
    submit = SubmitField('Update Password')

# update username
class UpdateUsernameForm(FlaskForm):
    new_username = StringField('Username', validators=[
                               DataRequired(), Length(min=2, max=15)])
    submit = SubmitField('Update Username')

# update email
class UpdateEmailForm(FlaskForm):
    new_email = StringField('Email address', validators=[
                            DataRequired(), Email(), Length(min=6, max=35)])
    submit = SubmitField('Update Email')

# update password
class UpdatePasswordForm(FlaskForm):
    new_password = PasswordField('Password', validators=[
                                 DataRequired(), Length(min=8, max=200)])
    new_password_confirm = PasswordField('Confirm Password', validators=[
                                         DataRequired(), EqualTo('new_password')])
    submit = SubmitField('Update Password')


# delete account
class DeleteAccountForm(FlaskForm):
    username = StringField('Username', validators=[
                           DataRequired(), Length(min=2, max=15)])
    submit = SubmitField('Delete my account')

class SupportForm(FlaskForm):
    topic = StringField('Topic', validators=[DataRequired()])
    description = StringField('Description', validators=[DataRequired()])

#update preferences
class UpdatePreferences(FlaskForm):
    analyze = SelectField('Analyze posts from your account?', choices=[(True, "Yes"), (False, "No")], validators=[
                                 InputRequired()], coerce=lambda x: x == 'True')
    categories = StringField('Categories', validators=[
                                         DataRequired(), Regexp("^[a-zA-Z0-9#_, ]*$", message="The categories must contain only letters, numbers or underscores. You should use hashtags before each category."), Length(min=3, max=100)])
    submit = SubmitField('Update Preferences')
