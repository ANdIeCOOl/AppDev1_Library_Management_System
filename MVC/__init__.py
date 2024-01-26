
from flask import Flask
#Flask is an microwebframework used to building web applications fast
from flask_migrate import Migrate


from flask_sqlalchemy import SQLAlchemy
import os

"""
Flask-SQLAlchemy is an extension for Flask that adds support for SQLAlchemy to 
your application. It simplifies using SQLAlchemy with Flask by setting up 
common objects and patterns for using those objects, such as a session tied 
to each web request, models, and engines
"""

#----------------------------------------------------------------

from flask import Flask,render_template , flash , request , redirect , url_for


# render template renders html template, flash flashes alerts and messages, customized with bootstrap
# request is request POST form data not really needed as I am using wtforms
# redirect you to specified url
# url_for gets the relevalent url for the that function 
#----------------------------------------------------------------------

from flask_login import LoginManager #TODOOOOOOOOO

from flask_login import login_user, logout_user , login_required , current_user #TODO




#--------------------------------------------------------
""" 
__name__ is standard python variable that tells the where the script is being run
from here is MVC as it is being run from MVC package but when we run it from command
line in the app.py file __name__ is main  
"""
app = Flask(__name__)
#---------------------------------------------------------------

"""
app is an instance of the Flask dependcies and is an object of the same as
python uses objects for everything
app.config is configuration of the Flask app 
  ->Secret key is need for csrf token  Cross-Site Request Forgery (CSRF) 
    is an attack that forces authenticated users to submit a request to a 
    Web application against which they are currently authenticated. Basically
    for security
  ->SQLALCHEMY_DATABASE_URI tells the infomation of the type of database and
    also where it is located URI:Uniform Resource Locater

    a URL and a URI is that a URL specifies the location of a resource on the internet
     while a URI can be used to identify any type of resource, not just those 
     on the internet.

"""
app.config['SECRET_KEY'] = '123456'


app.config['SQLALCHEMY_DATABASE_URI'] ='sqlite:///LMS.db'

#----------------------------------------------------------------------------------------
"""
USING  flask_sqlalchemy to give our flask app all the features and ORM's that a database
needs configured over SQLALCHEMY

"""

#Create the db object using the SQLAlchemy constructor.
db = SQLAlchemy()


# connects to a SQLite database, which is stored in the app’s instance folder.
db.init_app(app)
migrate = Migrate(app, db ,render_as_batch=True)


#------------------------------------------------------------------------

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"
login_manager.login_message_category = "info"



#------------------------------------------------------------------
from MVC import Views_Routes #sometimes you need it , sometimes you don't?
#CLEAR THIS DOUBT
#----------------------------------------------------------------------