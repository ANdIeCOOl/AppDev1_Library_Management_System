from MVC import app
from MVC import Controller_Forms
from MVC.Model import Users,Books,Sections,Requests,Restrictions,Feedbacks,users_books
from MVC.Model import Sections as SectionTable
from MVC.Model import Requests as RequestsTable
from MVC import db


from flask import render_template, url_for,redirect,flash,request
from flask_login import login_user, logout_user, login_required, current_user, login_manager
from werkzeug.security import generate_password_hash, check_password_hash 

#LANDING PAGE-------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------

@app.route("/" , methods = ['GET' , 'POST'])
def index():
    if current_user.is_authenticated:
        return redirect(url_for("Home"))
    else:
       return render_template("index.html") 



#--------------------------------------------------------------------------------------
#LOGIN-------------------------------------------------------------------------------



@app.route("/login" , methods = ['GET','POST'])
def login():

    form = Controller_Forms.LoginForm()
    if form.validate_on_submit():
        #with db.engine.connect() as conn:
         #   user = conn.execute(f"SELECT * FROM users WHERE username = {form.username.data}")
       # user = db.engine.execute(f"SELECT * FROM users WHERE username = {form.username.data}")
        user = Users.query.filter_by(username = form.username.data).first()
        #DB CONFIG
        if user:              
            if check_password_hash(user.password_hash,form.password.data):
                login_user(user)
                flash("Login Successfull" , category="success")
                return redirect(url_for("Home"))
            else:
                flash("Please check entered Password and try again" , category="danger")
                #need to render something here right <><><>><><"""
        else:
            flash("User does not exist",category="warning")
            return redirect(url_for("login"))

    return render_template("login.html",form = form)



#--------------------------------------------------------------------------------------
#LOGOUT-------------------------------------------------------------------------------


@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You have been successfully logged out", category="success")
    return redirect(url_for("index"))

#REGISTER-------------------# still need to check why form.validate on submit not working
@app.route("/register" , methods = ['GET','POST'])
def register():
    form = Controller_Forms.RegisterForm()
    print("TESTING FORM VALIDATION--------------\n---------------")
    print(form.validate_on_submit())
    print("TESTING FORM VALIDATION--------------\n---------------")
    print("I AM HERE ----\n---------1 ---\n----------\n----------")
    if form.validate_on_submit() or request.method == "POST":
    # ):
    #if request.method == "POST":

        print("I AM HERE ----\n---------2 ---\n----------\n----------")
        user = Users.query.filter_by(username = form.username.data).first()
        
        if user:    
            flash("Username is already taken", category="info")
            print("I AM HERE ----\n---------3 ---\n----------\n----------")
            return redirect(url_for("register"))
            
        else:
            if (form.password.data == form.confirm_password.data):
                New_User = Users(username=form.username.data,
                                 name = form.name.data,
                                 password_hash =generate_password_hash(form.password.data)
                                )
                              
                            
                db.session.add(New_User)
                db.session.commit() 
                login_user(New_User)
                flash("Registration Successfull" , category="success")
                print("I AM HERE ----\n---------4 ---\n----------\n----------")
                return redirect(url_for("Home"))
            else:
                flash("Passwords did not match" , category="warning")
                print("I AM HERE ----\n---------5 ---\n----------\n----------")
                return redirect(url_for("register"))
    print("I AM HERE ----\n---------7 ---\n----------\n----------")         
    print("I AM HERE ----\n---------6 ---\n----------\n----------")
    return render_template("register.html",form = form)


#--------------------------------------------------------------------------------------
#HOME OR DASHBOARD-------------------------------------------------------------------------------



@app.route("/Home") #LVL 1
@login_required
def Home():
    print("--------------------\n'''''''''''''''''\n-------")
    print(current_user.name)
    print(current_user.username)
    print(current_user.role)
    print(current_user.id)
    user = Users.query.filter_by(username = current_user.username).first()
    print(user)
    print("--------------------\n'''''''''''''''''\n-------")
    if (current_user.role == "Administrator"):
        return render_template("AdminHome.html")
    else:
        return render_template("UserHome.html")


#--------------------------------------------------------------------------------------
#REQUESTS-------------------------------------------------------------------------------

"""
LVL 1
"""
@app.route("/Requests")
@login_required
def Requests():
    if (current_user.role == "Administrator"):
        requests = db.session.execute(db.select(RequestsTable)).scalars()
        return render_template("AdminRequests.html" , requests = requests)
    else:
        return render_template("UserRequests.html")
    

"""
LVL 2
"""
#Pending Requests

@app.route("/Requests/Pending")
@login_required
def PendingRequests():
    if (current_user.role == "Administrator"):
        return render_template("AdminRequestsPending.html")
    else:
        return render_template("UserRequestsPending.html")


#Request history for analytics maybe in the future  

@app.route("/Requests/History")
@login_required
def RequestsHistory():
    if (current_user.role == "Administrator"):
        return render_template("AdminRequestsHistory.html")
    else:
        return render_template("UserRequestsHistory.html")


#--------------------------------------------------------------------------------------
#ANALYTICS-------------------------------------------------------------------------------
"""
LVL 1
"""
@app.route("/Analytics" , methods = ['GET' , 'POST'])
@login_required
def Analytics():
    if (current_user.role == "Administrator"):
        return render_template("AdminAnalytics.html")
    else:
        return render_template("UserAnalytics.html")

"""
LVL 2
"""  
#ALL USERS ANALYTICS
@app.route("/Analytics/Users" , methods = ['GET' , 'POST'])
@login_required
def UsersAnalytics():
    pass

#System Analytics Visits CLicks etc
@app.route("/Analytics/System" , methods = ['GET' , 'POST'])
@login_required
def SystemAnalytics():
    pass
#Book Analytics highest rating, most requested etc
@app.route("/Analytics/Books" , methods = ['GET' , 'POST'])
@login_required
def BooksAnalytics():
    pass
#Section Analytics highest rating, most visted etc
@app.route("/Analytics/Sections" , methods = ['GET' , 'POST'])
@login_required
def SectionsAnalytics():
    pass

#--------------------------------------------------------------------------------------
#ALL USERS ACCESS FOR ADMIN--------------------------------------------------
@login_required
@app.route("/Users")
def ALLUsers():
    if current_user.role == "Administrator":
        users = db.session.execute(db.select(Users)).scalars()
        return render_template("AllUserProfiles.html",users = users)
    else:
        logout_user
        flash("Access Denied", category="danger")
        return redirect(url_for("/"))


#--------------------------------------------------------------------------------------
#SECTIONS-------------------------------------------------------------------------------

@app.route("/Sections" , methods = ['GET' , 'POST'])
@login_required
def Sections():
    sections = db.session.execute(db.select(SectionTable)).scalars()
    if (current_user.role =="Administrator"):
        return render_template("AdminSections.html",sections = sections)
    else:
        return render_template("UserSections.html",sections = sections)
    
@app.route("/Sections/<int:ID>" , methods = ['GET' , 'POST'])
@login_required
def Section(ID):
    orderFilter = request.args.get("filter") #makesure correct filter displayes as buttons
    try:
        books = db.engine.execute(f"SELECT * FROM books WHERE section_id = {ID} ORDERBY {orderFilter} ;")
    except:
        pass
    if (current_user.role == "Administrator"):
        return render_template("AdminBooks.html",books = books)
    else:
        return render_template("UserBooks.html",books = books)
    




#--------------------------------------------------------------------------------------
#Need to update books and blob datatype also need to modify database so save this for 
    # later

#BOOKS
@app.route("/Books" , methods = ['GET' , 'POST'])
@login_required
def Books():
    form = Controller_Forms.UploadBookForm()
    """orderFilter = request.args.get("filter") #makesure correct filter displayes as buttons
    try:
        books = db.engine.execute(f"SELECT * FROM books ORDERBY {orderFilter} ;")
    except:
        pass"""
    
    if form.validate_on_submit() or request.method == "POST":
        book = Books(title = form.title.data , 
                     author = form.author.data ,
                     description =form.description.data ,
                     content=form.content.data )

    else:
        if (current_user.role =="Administrator"):
            return render_template("AdminBooks.html",form = form)
        else:
            return render_template("UserBooks.html")

#Book Info
@app.route("/Books/<int:BookID>" , methods = ['GET' , 'POST']) #get id then book name pass book name in url but better to use id
@login_required
def Book(Book_ID): 
    
    book = db.Books.query.filter_by( id = int(Book_ID)).first()
    bookFeedback = db.Feedbacks.query.filter_by(book_id = int(Book_ID))
    feedbacks = []
    
    for feedback in bookFeedback:
        feedbacks.append(feedback)

    if (current_user.role == "Administrator"):
        return render_template("AdminBooks.html",book= book,feedbacks = feedbacks)
    else:
        return render_template("UserBooks.html",book = book)



 #######################################################################

# ALL USER CODE

#####################################################################