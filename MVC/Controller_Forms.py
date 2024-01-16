from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField,IntegerField
from flask_wtf.file import FileField
from wtforms.validators import Length, EqualTo, Email, DataRequired, ValidationError

class LoginForm(FlaskForm):
    username = StringField("Username" , validators=[DataRequired()])
    password = PasswordField("Password" , validators=[DataRequired()])
    submit = SubmitField("Login")

class RegisterForm(FlaskForm):
	name = StringField("Name", validators=[DataRequired()])
	username = StringField("Username", validators=[DataRequired()])
	password = PasswordField('Password', validators=[DataRequired(), EqualTo('password_hash2', message='Passwords Must Match!')])
	confirm_password = PasswordField('Confirm Password', validators=[DataRequired()])
	submit = SubmitField("Register")
      
class SearchBarForm(FlaskForm):
	searched = StringField("Searched", validators=[DataRequired()])
	submit = SubmitField("Search")  
	
class FeedBackForm(FlaskForm):
	feedback = StringField("Feedback", validators=[DataRequired() , Length(max=300)])
	rating = IntegerField("Rating",validators=[DataRequired()])
	submit = SubmitField("Give FeedBack")  
	

class UploadBookForm(FlaskForm):
    title =  StringField("Title", validators=[DataRequired()])
    author =  StringField("Author", validators=[DataRequired()])
    description =  StringField("Description", validators=[DataRequired()])
    content =   FileField("Description", validators=[DataRequired()])
	# <form method = 'POST' enctype = multipart/form-data> ADD THIS TO FORM 
    section_id =   IntegerField("Description", validators=[DataRequired()])
    submit = SubmitField("Upload Book")  
	
class EditBookForm(FlaskForm):
	pass

class EditUserForm(FlaskForm):
	pass



