#---------------------------------
"""
URL : https://docs.sqlalchemy.org/en/20/orm/basic_relationships.html#many-to-many
"""

#------------------------------------------------
#-------------------------------------------------------------------------
from flask_login import UserMixin
"""
URL: https://flask-login.readthedocs.io/en/latest/#flask_login.UserMixin

This provides default implementations for the 
methods that Flask-Login expects user objects to have.
"""

#------------------------------------------------------------------------
from MVC import db,login_manager
"""
imports the database object and login manager object to
give functionality to the database

"""


#-----------------------------------------------------------
#@login_manager.user_loader
#def load_user(user_id):
#    return User.get((int)user_id)

"""
URL:https://flask-login.readthedocs.io/en/latest/

You will need to provide a user_loader callback. This callback is 
used to reload the user object from the user ID stored in the session. 
It should take the str(HERE in my database , id is int) ID of a user, and 
return the corresponding user object. 
"""
#---------------------------------------

#--------------------------------------------
users_books = db.Table(
    "users_books",
    db.Column("user_id", db.ForeignKey("users.id"),primary_key=True),
    db.Column("book_id", db.ForeignKey("books.id"),primary_key=True),
)


class Users(db.Model, UserMixin):
    __tablename__ = "users"
    id = db.Column(db.Integer(), primary_key = True)
    name =  db.Column(db.String(length = 60) , nullable = False )
    password_hash = db.Column(db.String(length = 256) , nullable = False) 
    books = db.relationship("Books",secondary = users_books )
    role = db.Column(db.String(10) , default = "User")

    def __repr__(self) -> str:
        return f"Name: {self.name}; Books:{self.books} ; Role:{self.role}"
    



class Books(db.Model):
    __tablename__ = "books"
    id = db.Column(db.Integer(), primary_key = True)
    title =  db.Column(db.String(length = 60) , nullable = False )
    author =  db.Column(db.String(length = 60) , nullable = False )
    description =  db.Column(db.String(length = 60) , nullable = False )
    content =  db.Column(db.String(length = 60) , nullable = False )
    section_id =  db.Column(db.Integer,db.ForeignKey("sections.id"))
    books = db.relationship("Books",secondary = users_books )
    visits =  db.Column(db.String(length = 60) , nullable = False )
    name =  db.Column(db.String(length = 60) , nullable = False )

    def __repr__(self) -> str:
        return f"Name: {self.title}; Author:{self.author} ; Readers:{self.current_readers}"


class Sections(db.Model):
    __tablename__ = "sections"
    id = db.Column(db.Integer(), primary_key = True)
    name =  db.Column(db.String(length = 60) , nullable = False )
    date_created =  db.Column(db.String(length = 60) , nullable = False )
    description =  db.Column(db.String(length = 60) , nullable = False )
    content =  db.Column(db.String(length = 60) , nullable = False )
    visits =  db.Column(db.String(length = 60) , nullable = False )
    current_readers =  db.Column(db.String(length = 60) , nullable = False )
    name =  db.Column(db.String(length = 60) , nullable = False )

class Feedbacks(db.Model):
    __tablename__ = "feedbacks"
    id = db.Column(db.Integer(), primary_key = True)
    user_id =  db.Column(db.Integer(), nullable = False)
    book_id =  db.Column(db.Integer(), nullable = False)
    feedback=  db.Column(db.String(length = 300))
    rating =  db.Column(db.Integer() )

class Requests(db.Model):
    __tablename__ = "requests"
    id = db.Column(db.Integer(), primary_key = True)
    book_id =  db.Column(db.String(length = 60) , nullable = False )
    date =  db.Column(db.String(length = 60) , nullable = False )
    status =  db.Column(db.String(length = 60) , nullable = False )

class Retrictions(db.Model):
    __tablename__ = "restrictions"
    id = db.Column(db.Integer(), primary_key = True)
    user_id =  db.Column(db.String(length = 60) , nullable = False )
    book_id =  db.Column(db.String(length = 60) , nullable = False )






