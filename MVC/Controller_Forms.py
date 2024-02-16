from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField,IntegerField,SelectField,SearchField
from flask_wtf.file import FileField,FileRequired,FileAllowed
from wtforms.validators import Length, EqualTo, Email, DataRequired, ValidationError,NumberRange
from datetime import date

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
	
class FeedBackForm(FlaskForm):
	feedback = StringField("Feedback", validators=[DataRequired() , Length(max=300)])
	rating = IntegerField("Rating",validators=[DataRequired()])
	submit = SubmitField("Give FeedBack")  
	

class UploadBookForm(FlaskForm):
    title =  StringField("Title", validators=[DataRequired()])
    author =  StringField("Author", validators=[DataRequired()])
    description =  StringField("Description", validators=[DataRequired()])
    content =   FileField("Content", validators=[FileRequired(),FileAllowed(['jpg', 'png','pdf'], 'Filesonly only!')])
	# <form method = 'POST' enctype = multipart/form-data> ADD THIS TO FORM 
    section_id =   StringField("SectionID")
    submit = SubmitField("Upload Book")  
	
class EditBookForm(FlaskForm):
	title =  StringField("Title")
	author =  StringField("Author")
	book_pic = FileField("Choose Book picture", validators=[FileAllowed(['jpg', 'png','jpeg'])])
	description =  StringField("Description")
	content =   FileField("Content", validators=[FileAllowed(['pdf'], 'Filesonly only!')])
	# <form method = 'POST' enctype = multipart/form-data> ADD THIS TO FORM 
	section_id =   StringField("SectionID")
	submit = SubmitField("Upload Book")  
	

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