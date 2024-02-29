
from flask import Flask
"""Flask is an microwebframework used to building web applications fast
https://flask.palletsprojects.com/en/3.0.x/"""

from flask_migrate import Migrate
"""Flask-Migrate is an extension that handles SQLAlchemy database migrations for 
 Flask applications using Alembic. The database operations are made 
 available through the Flask command-line interface.
 https://flask-migrate.readthedocs.io/en/latest/"""


from flask_sqlalchemy import SQLAlchemy

"""
Flask-SQLAlchemy is an extension for Flask that adds support for SQLAlchemy to 
your application. It simplifies using SQLAlchemy with Flask by setting up 
common objects and patterns for using those objects, such as a session tied 
to each web request, models, and engines
"""

#----------------------------------------------------------------

from flask import Flask


"""
- render template renders html template, flash flashes alerts and messages, customized with bootstrap
- request is request POST form data not really needed as I am using wtforms
- redirect you to specified url
- url_for gets the relevalent url for the that function 
"""
#----------------------------------------------------------------------

from flask_login import LoginManager 
"""
Flask-Login provides user session management for Flask. 
It handles the common tasks of logging in, logging out, and remembering your 
user's sessions over extended periods of time.
https://flask-login.readthedocs.io/en/latest/
"""
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
#secret key required for login manager
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

#required to help migrate database with minimal effort, rather than creating a new
# database everytime
migrate = Migrate(app, db ,render_as_batch=True)


#------------------------------------------------------------------------

#instance of login manager And also UserMixin for UserModel
login_manager = LoginManager()

login_manager.init_app(app)
login_manager.login_view = "login" #function name
login_manager.login_message_category = "info" #the category for the flash message

#All the intricacies for logging

#------------------------------------------------------------------
from MVC import Views_Routes #to avoid circular imports
#----------------------------------------------------------------------