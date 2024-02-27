from flask_wtf import FlaskForm
"""Simple integration of Flask and WTForms, including CSRF, file upload, and reCAPTCHA.
https://flask-wtf.readthedocs.io/en/0.15.x/"""

#--------------------------------------------------------------------

from wtforms import StringField, SubmitField, PasswordField,IntegerField,SelectField,SearchField

"""
WTForms is a flexible forms validation and rendering library for Python web development.
It can work with whatever web framework and template engine you choose. 
It supports data validation, CSRF protection, internationalization (I18N), and more. 
There are various community libraries that provide closer integration with
popular frameworks.
"""
#--------------------------------------------------------------------
from flask_wtf.file import FileField,FileRequired,FileAllowed
#Validators for form fields that include file uploads

#--------------------------------------------------------------------
from wtforms.validators import Length, EqualTo, DataRequired,NumberRange
"""
Validators for Form Fields
"""

#--------------------------------------------------------------------


class LoginForm(FlaskForm):
    username = StringField("Username" , validators=[DataRequired()])
    password = PasswordField("Password" , validators=[DataRequired()])
    submit = SubmitField("Login")

class RegisterForm(FlaskForm):
	name = StringField("Name", validators=[DataRequired()])
	username = StringField("Username", validators=[DataRequired()])
	password = PasswordField('Password', validators=[DataRequired(), EqualTo('confirm_password', message='Passwords Must Match!')])
	confirm_password = PasswordField('Confirm Password', validators=[DataRequired()])
	submit = SubmitField("Register")  
	

class UploadBookForm(FlaskForm):
    title =  StringField("Title", validators=[DataRequired()])
    author =  StringField("Author", validators=[DataRequired()])
    description =  StringField("Description", validators=[DataRequired()])
    content =   FileField("Content", validators=[FileRequired(),FileAllowed(['jpg', 'png','pdf'], 'Filesonly only!')])
	# <form method = 'POST' enctype = multipart/form-data> ADD THIS TO FORM 
    submit = SubmitField("Upload Book")  
	
class EditBookForm(FlaskForm):
	title =  StringField("Title")
	author =  StringField("Author")
	book_pic = FileField("Choose Book picture", validators=[FileAllowed(['jpg', 'png','jpeg'])])
	description =  StringField("Description")
	content =   FileField("Content", validators=[FileAllowed(['pdf'], 'Filesonly only!')])
	# <form method = 'POST' enctype = multipart/form-data> ADD THIS TO FORM 
	submit = SubmitField("Update Book")  
	

class EditUserForm(FlaskForm):
	name = StringField("Name")
	profile_pic = FileField("Choose profile picture", validators=[FileAllowed(['jpg', 'png','jpeg'])])
	username = StringField("Username")
	submit = SubmitField("Update")

class UploadSectionForm(FlaskForm):
    name =  StringField("Section Name", validators=[DataRequired()])
    description =  StringField("Description", validators=[DataRequired()])
    submit = SubmitField("Add Section")  

class EditSectionForm(FlaskForm):
    name =  StringField("Section Name")
    description =  StringField("Description")
    submit = SubmitField("Add Section")  

class UploadFeedBackForm(FlaskForm):
	feedback = StringField("Feedback",validators=[DataRequired()])
	rating = IntegerField("Rating",validators = [DataRequired(),NumberRange(min=0,max=5)])
	submit = SubmitField("Give Feedback") 

class SearchForm(FlaskForm):
	search = SearchField("Enter what you are looking for",validators=[DataRequired()])
	lookfor = SelectField("Search for:",choices= [("Books","Books"),("Authors","Authors"),("Sections","Sections")])
	submit = SubmitField("Search") 