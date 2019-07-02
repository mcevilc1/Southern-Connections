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
import getpass, sys
import pyodbc
from hashlib import md5
import datetime
from SouthernConnections_Forms import SignUpForm, LoginForm
from linkedin_v2 import linkedin


#CONSUMER_KEY = '7885pys3bk2lgp'
#CONSUMER_SECRET = 'dH8BbU7pk9e59a2S'
#USER_TOKEN = 'mcevilc1@gmail.com'
#USER_SECRET = 'caitlin1'
#RETURN_URL = 'http://127.0.0.1:5000/'
#authentication = linkedin.LinkedInDeveloperAuthentication(CONSUMER_KEY, CONSUMER_SECRET, USER_TOKEN, USER_SECRET, 
                                                          #RETURN_URL, linkedin.PERMISSIONS.enums.values())
#application = linkedin.LinkedInApplication(authentication)
#application.get_profile()


app = Flask(__name__)
app.config['SECRET_KEY'] = '@N4j* kMr3%M 2o9$ f5h*G'
app.db = None
login_manager = LoginManager(app)
login_manager.login_view = 'login'
bootstrap = Bootstrap(app)
moment = Moment(app)


def connect_db():
	if not app.db:
		app.db = pyodbc.connect('Driver={SQL Server};'
			'Server=DESKTOP-IO3MC37;'
			'Database=SouthernConnections;'
			'Trusted_Connection=yes;')
	else:
		print('Connected!', file=sys.stderr)

# Check if Email is @southernct.edu
def check_scsu_email(email):
        split_email = email.split('@')
        if split_email[1] != 'southernct.edu':
                return False
        else:
                return True

# Checks if the same username already exists
def check_duplicate_user(email):
        if not app.db:
                connect_db()
        c = app.db.cursor()
        c.execute('SELECT * FROM userData WHERE email="'+email+'";')
        possible_user = c.fetchall()
        c.close()
        if not possible_user:
                return False
        else:
                return True

# Check duplicate email on signup, aka user already signed up
def check_duplicate_userName(name):
        if not app.db:
                connect_db()
        c = app.db.cursor()
        c.execute('SELECT * FROM userData WHERE user_name="'+name+'";')
        possible_duplicate_name = c.fetchall()
        c.close()
        if not possible_duplicate_name:
                return False
        else:
                return True
# Error Routes
@app.errorhandler(404)
def page_not_found(e):
        print('at 400', file=sys.stderr)
        return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
        return render_template('500.html'), 500


# Base Route
@app.route('/')
def base_page():
        if current_user.is_anonymous:
                return render_template('landing.html')
        else:
                return render_template('main_page.html', name = current_user.user_name)

# Sign-up Route
@app.route('/sign-up/', methods=['GET', 'POST'])
def signup():
	if not app.db:
		connect_db()
	user_name = None
	email = None
	first_name = None
	last_name = None
	password = None
	password2 = None
	major = None
	gradyear = None
	form = SignUpForm()
	c=app.db.cursor()
	if form.validate_on_submit():
		email = form.email.data
		form.email.data = ''
		first_name= form.first_name.data
		form.first_name.data = ''
		last_name = form.last_name.data
		form.last_name.data = ''
		password = form.password.data
		form.password.data = ''
		password2 = form.password2.data
		form.password2.data = ''
		major = form.major.data
		form.major.data = ''
		gradyear = form.gradyear.data
		form.gradyear.data = ''
		c.execute("SELECT * FROM bannedUsers WHERE email = '"+email+"';")
		banned_user = c.fetchone()
		if banned_user:
			return redirect(url_for('banned'))
		if check_duplicate_user(email) == True:
			flash("You are already signed up")
			return redirect(url_for('login'))
		elif check_duplicate_userName(user_name) == True:
			flash('Sorry, that user name is already taken')
			return redirect(url_for('signup'))
		elif check_scsu_email(email) == True:
			query = "INSERT INTO MemberProfile(Email, FName, LName, Major, GradYear, UserType, passwd) values(%s, %s, %s, %s, %s, %s, %s);"
			c.execute(query, (email, first_name, last_name, major, gradyear, 'user', password))
			app.db.commit()
			c.close()
			return redirect(url_for('login'))
		else:
			flash('Email must be from SouthernCT')
			return redirect(url_for('signup'))
		return render_template('sign_up.html', form=form, email=email, last_name=last_name,\
				first_name=first_name, password=password,\
				password2=password2, major=major, gradyear=gradyear)

# Success Route
@app.route('/success')
def success():
        return render_template('success.html')

if __name__=='__main__':
	app.run()