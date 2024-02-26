
#------------


from datetime import date

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
@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))

"""
URL:https://flask-login.readthedocs.io/en/latest/

You will need to provide a user_loader callback. This callback is 
used to reload the user object from the user ID stored in the session. 
It should take the str(HERE in my database , id is int) ID of a user, and 
return the corresponding user object. 
"""
#---------------------------------------

#--------------------------------------------

#Association Table or RelationTable in SQL terms for a User's Books
users_books = db.Table(
    "users_books",
    db.Column("user_id", db.ForeignKey("users.id"),primary_key=True),
    db.Column("book_id", db.ForeignKey("books.id"),primary_key=True),
    db.Column("doi",db.String(), default  = date.today().strftime("%d/%m/%Y"))
)

#UserMixin has predefined methods that are required for login manager wrt to UserModel
class  Users(db.Model, UserMixin):
    __tablename__ = "users"
    profile_pic = db.Column(db.LargeBinary() ) 
    username = db.Column(db.String(length = 30),nullable = False , unique = True)
    id = db.Column(db.Integer(), primary_key = True)
    name =  db.Column(db.String(length = 60) , nullable = False )
    password_hash = db.Column(db.String(length = 256) , nullable = False) 
    books = db.relationship("Books",secondary = users_books )
    role = db.Column(db.String(10) , default = "User")
    feedback = db.relationship("Feedbacks")
    logins = db.Column(db.Integer(),default = 0)
    no_books_requested = db.Column(db.Integer(),default = 0)

    def __repr__(self) -> str:
        return f"""Name: {self.name};
                Username: {self.username};
                Books:{self.books} ;
                Role:{self.role}"""
    
  


class Books(db.Model):
    __tablename__ = "books"
    book_pic = db.Column(db.LargeBinary() ) 
    id = db.Column(db.Integer(), primary_key = True)
    title =  db.Column(db.String(length = 60) , nullable = False )
    author =  db.Column(db.String(length = 60) , nullable = False )
    description =  db.Column(db.String(length = 60) , nullable = False )
    content =  db.Column(db.LargeBinary() , nullable = False ) #verybad practice need cloud for actual data and just store metadata
    section_id =  db.Column(db.Integer,db.ForeignKey("sections.id"))
    feedback = db.relationship("Feedbacks",cascade="all, delete")  
    requests = db.relationship("Requests",cascade="all, delete")
    rating = db.Column(db.Integer() , default = 5)
    current_readers = db.relationship("Users",secondary = users_books )
    visits = db.Column(db.Integer(),default = 0)
    requests = db.Column(db.Integer(),default = 0)
    
    def __repr__(self) -> str:
        return f"Name: {self.title}; Author:{self.author} ; Content:{self.content}"


class Sections(db.Model):
    __tablename__ = "sections"
    id = db.Column(db.Integer(), primary_key = True)
    name =  db.Column(db.String(length = 60) , nullable = False )
    date_created =  db.Column(db.String(length = 60) , nullable = False ,default = date.today().strftime("%d/%m/%Y") )
    description =  db.Column(db.String(length = 60) , nullable = False )
    name =  db.Column(db.String(length = 60) , nullable = False )
    visits = db.Column(db.Integer(),default = 0)
    requests = db.Column(db.Integer(),default = 0)


class Feedbacks(db.Model):
    __tablename__ = "feedbacks"
    id = db.Column(db.Integer(), primary_key = True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    book_id = db.Column(db.Integer, db.ForeignKey('books.id'))
    feedback=  db.Column(db.String(length = 300))
    rating =  db.Column(db.Integer() )

class Requests(db.Model):
    __tablename__ = "requests"
    id = db.Column(db.Integer(), primary_key = True)
    book_id = db.Column(db.Integer(), db.ForeignKey('books.id'),nullable = False,unique = True)

    date =  db.Column(db.String(length = 60) , nullable = False,default =date.today().strftime(f"%d/%m/%Y")  )
    status =  db.Column(db.String(length = 60) , nullable = False , default = "Pending" )
    user_id = db.Column(db.Integer(),nullable = False)
 
    def __repr__(self) -> str:
        return f"Book: {Books.query.get(self.book_id)}; date:{self.date} ; Status:{self.status}"





