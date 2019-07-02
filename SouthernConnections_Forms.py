from flask import Flask, render_template, flash, redirect, url_for, request
from flask_login import LoginManager, UserMixin, login_user, logout_user, \
    current_user, login_required
from werkzeug.urls import url_parse
from werkzeug.security import check_password_hash, generate_password_hash
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField,TextAreaField, \
                    DateTimeField
from wtforms.validators import DataRequired, Email, EqualTo, Length
import getpass, pymysql, sys
from hashlib import md5
import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = '@N4j* kMr3%M 2o9$ f5h*G'
app.db = None
login_manager = LoginManager(app)
login_manager.login_view = 'login'
bootstrap = Bootstrap(app)
moment = Moment(app)

def connect_db():
        if not app.db:
                app.db = pymysql.connect('35.229.121.181', 'root', '$c46n1n2e379', 'meetme')
        else:
                print('Connected', file=sys.stderr)

#Flask Form Classes

# Sign Up
class SignUpForm(FlaskForm):
        email = StringField('SCSU Email:', validators = [DataRequired(), Email()])
        first_name = StringField('First Name:', validators = [DataRequired()])
        last_name = StringField('Last Name:', validators = [DataRequired()])
        password = PasswordField('Password:', validators = [DataRequired()])
        password2 = PasswordField('Re-enter Password:', validators = [DataRequired(), \
                 EqualTo('password')])
        major = StringField('Major:', validators = [DataRequired()])
        gradyear = StringField('Graduation Year:', validators = [DataRequired()])
        submit = SubmitField('Submit')

# Login
class LoginForm(FlaskForm):
        email = StringField('SCSU Email:', validators = [DataRequired(), Email()])
        password = PasswordField('Password:', validators = [DataRequired()])
        submit = SubmitField('Submit')

# Create user profile
class userProfileForm(FlaskForm):
        about_me = TextAreaField('About Me:')
        password = StringField('Password:')
        submit = SubmitField('Submit')

# Add Event
class AddEventForm(FlaskForm):
        title = StringField('Event Title:', validators = [DataRequired()])
        event_date = StringField(id='datepick', validators = [DataRequired(), \
                     Length(min=18, max=19)])
        place = StringField('Meeting Location:', validators = [DataRequired()])
        description = TextAreaField('Description:')
        group = StringField('Group')
        submit = SubmitField('Submit')

#Edit Event Form
class UpdateEventForm(FlaskForm):
        event_date = StringField(id='datepick', validators = [DataRequired(), \
                     Length(min=18, max=19)])
        place = StringField('Meeting Location:', validators = [DataRequired()])
        description = TextAreaField('Description:')
        submit = SubmitField('Update')

# Search Events
class SearchEventsForm(FlaskForm):
        title = StringField('Event Name or Place:', validators = [DataRequired()])
        submit = SubmitField('Submit')

# Add Group
class CreateGroupForm(FlaskForm):
        groupName = StringField('Group Name:', validators = [DataRequired()])
        description = TextAreaField('Description:')
        submit = SubmitField('Submit')

# Edit Group
class EditGroupForm(FlaskForm):
        description = TextAreaField('Description:')
        submit = SubmitField('Update')

# Join Group
class JoinGroupForm(FlaskForm):
        submit = SubmitField('Join Group')

# Join Event
class JoinEventForm(FlaskForm):
        submit = SubmitField('Join Event')

# Leave Group
class LeaveGroupForm(FlaskForm):
        submit = SubmitField('Leave Group')

# Leave Group
class LeaveEventForm(FlaskForm):
        submit = SubmitField('Leave Event')

# Search Groups
class SearchGroupsForm(FlaskForm):
        groupName = StringField('Search:', validators = [DataRequired()])
        submit = SubmitField('Submit')

# Ban user form
class BanUserForm(FlaskForm):
        email = StringField('User Email:')
        reason = TextAreaField('Reason for Ban:')
        submit = SubmitField('Submit')

# Close event form
class CloseEventForm(FlaskForm):
        title = StringField('Event Name:')
        reason = TextAreaField('Reason for Cancellation:')
        submit = SubmitField('Submit')

# close group form
class CloseGroupForm(FlaskForm):
        group_name = StringField('Group Name:')
        reason = TextAreaField('Reason for Close:')
        submit = SubmitField('Submit')

# Create admin form
class CreateAdminForm(FlaskForm):
        email  = StringField('User Email:')
        submit = SubmitField('Submit')

# Close account
class CloseAccountForm(FlaskForm):
        submit = SubmitField('Delete Your Account')

