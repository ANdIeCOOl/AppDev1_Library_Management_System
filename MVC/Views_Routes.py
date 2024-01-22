from MVC import app
from MVC import Controller_Forms
from MVC.Model import Users,users_books
from MVC.Model import Sections as SectionTable
from MVC.Model import Requests as RequestsTable
from MVC.Model import Books as BooksTable
from MVC.Model import Feedbacks 
from MVC import db


from flask import render_template, url_for,redirect,flash,request
from flask_login import login_user, logout_user, login_required, current_user, login_manager
from werkzeug.security import generate_password_hash, check_password_hash 
from base64 import b64encode

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




#REGISTER-------------------
# still need to check why form.validate on submit not working
# thats proabably because some validation criteria is not being met check 
#  modifyusers function do that xD
#-------

@app.route("/register" , methods = ['GET','POST'])
def register():
    form = Controller_Forms.RegisterForm()
    print(form.validate_on_submit())


    if form.validate_on_submit() or request.method == "POST":
    # ):
    #if request.method == "POST":
        user = Users.query.filter_by(username = form.username.data).first()
        
        if user:    
            flash("Username is already taken", category="info")
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
                return redirect(url_for("Home"))
            
            else:
                flash("Passwords did not match" , category="warning")
                return redirect(url_for("register"))
   
    return render_template("register.html",form = form)


#--------------------------------------------------------------------------------------
#HOME OR DASHBOARD-------------------------------------------------------------------------------



@app.route("/Home") #LVL 1
@login_required
def Home():
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
    

@login_required
def AdminProcessRequest():
    pass
#--------------
#USER REQUESTING BOOK
#-------
@app.route("/Requesting <int:book_id>" , methods = ["GET","POST"])
@login_required
def UserRequestSubmit(book_id):
    if request.method == "GET":
        if len(current_user.books) < 5:
            try:
                requests = RequestsTable(user_id = current_user.id,book_id = book_id)
                db.session.add(requests)
                db.session.commit()
                flash("Your request has been sumbitted.\n Waiting for confirmation",category="success")
                return redirect(url_for("Books"))
            except:
                flash("You have already requested the book",category="warning")
                return redirect(url_for("Books"))
        else:
            flash("You have 5 books in Library, return a book before you request another",category="warning")
            return redirect(url_for("Books"))
    else:
        render_template("UserRequestprocessing.html")
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


#Accept request 
@app.route("/Requests/Approve<int:request_id>")
@login_required
def AcceptRequest(request_id):
    if (current_user.role == "Administrator"):
        request = RequestsTable.query.filter_by(id = request_id).first()
        user = Users.query.filter_by(id = request.user_id).first()
        book = BooksTable.query.filter_by(id = request.book_id).first()

        if (len(user.books) < 5):
            try:
                db.session.execute(users_books.insert().values(user_id = user.id,book_id = book.id))
            except:
                flash("Book already in Library",category="warning")
                db.session.delete(request)
                db.session.commit() 
                return redirect(url_for("Requests"))
            
            db.session.delete(request)
            flash("Request Approved",category="success")

            db.session.commit() #ITS NEED TO MAKED CHANGES PERMANANT LOL
            return redirect(url_for("Requests"))
        else:
            flash("User can only have a maximum of 5 books in your Personal Library")
            return redirect(url_for("Requests"))

    else:
        return redirect(url_for("Home")) #logut user later
    

#REject request 
@app.route("/Requests/Reject<int:request_id>")
@login_required
def RejectRequest(request_id):
    if (current_user.role == "Administrator"):
        request = RequestsTable.query.filter_by(id = request_id).first()
        db.session.delete(request)
        flash("Request Rejected",category="success")
        db.session.commit()
        return redirect(url_for("Requests"))


    else:
        return redirect(url_for("Home")) #logut user later


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
#USER HOMEPAGE FOR USER
"""
LVL 1
"""
@login_required
@app.route("/Users")
def ALLUsers():
    if current_user.role == "Administrator":
        users = db.session.execute(db.select(Users)).scalars()
        return render_template("AllUserProfiles.html",users = users)
    else:
        logout_user()
        flash("Access Denied", category="danger")
        return redirect(url_for("index"))


#--------
"""
LVL 2
"""
@login_required
@app.route("/Users/<int:user_id>",methods = ["GET","POST"])
def ModifyUser(user_id):

    if current_user.role == "Administrator":
        form = Controller_Forms.EditUserForm()

        if form.validate_on_submit():
            user = Users.query.filter_by(id = user_id).first()
            user.username = form.username.data
            user.name = form.name.data
            if form.profile_pic.data:
                user.profile_pic = form.profile_pic.data.read()
            user.verified = True
            db.session.commit()    
            flash("Update Successfull" , category="success")
            return redirect(url_for("ModifyUser",user_id = user_id))

        elif request.method == "POST":
            for fieldName, errorMessages in form.errors.items():
                for error in errorMessages:
                    flash(error,category="danger")
            return redirect(url_for("ModifyUser",user_id = user_id))


            

        else:

            user = Users.query.filter_by(id = user_id).first()
            Profile_image = None
            try:
                Profile_image = b64encode(user.profile_pic).decode("utf-8")
            except:
                pass
            books = []
            for book in user.books:
                if book.book_pic:
                    books.append((BooksTable.query.filter_by(id = book.id).first(),
                              b64encode(book.book_pic).decode("utf-8")))
                else:
                    books.append((BooksTable.query.filter_by(id = book.id).first(),
                                 None))
                

            return render_template("ModifyUserProfile.html", user=user , books=books,form = form , Profile_image = Profile_image)
    
    #------------
    #USER DASHBOARD
    else:#USER DASHBOARD
        
        """ if form.validate_on_submit: #UPDATE USER
            pass
        elif request.method == "POST":
            pass
        else:"""
        form = Controller_Forms.EditUserForm()
        Profile_image = None
        try:
            Profile_image = b64encode(current_user.profile_pic).decode("utf-8")
        except:
            pass
        books = []
        for book in current_user.books:
            if book.book_pic:
                books.append((BooksTable.query.filter_by(id = book.id).first(),
                        b64encode(book.book_pic).decode("utf-8")))
            else:
                books.append((BooksTable.query.filter_by(id = book.id).first(),
                                    None))
                    
        return render_template("UserProfile.html",form=form,books=books,Profile_image=Profile_image)

#RETURNING AND FEEDBACK-----------
@login_required
@app.route("/Return/<int:book_id>",methods = ["GET","POST"])
def ReturnBook(book_id):
    form = Controller_Forms.UploadFeedBackForm()
    if request.method == "GET":
        db.session.execute(users_books.delete().where(users_books.columns.user_id == current_user.id).where(users_books.columns.book_id==book_id))
        db.session.commit()
        flash("Thanks for returning the Book",category="success")
        return render_template("UserFeedback.html",form=form,book_id = book_id)
    elif form.validate_on_submit:
        feedback = Feedbacks(book_id = book_id,
                                  user_id = current_user.id,
                                  feedback = form.feedback.data,
                                  rating = form.rating.data
                                  )
        db.session.add(feedback)
        db.session.commit()
        flash("Thank you for the feedback",category="success")
        return redirect(url_for("ModifyUser",user_id = current_user.id))
    else:
        for fieldName, errorMessages in form.errors.items():
            for error in errorMessages:
                flash(error,category="danger")
        return redirect(url_for("ModifyUser",user_id = current_user.id))






#-----------
#DELETE USER PROFILE
#-------
@login_required
@app.route("/Users/Delete/<user_id>",methods = ["GET","POST"])
def DeleteUser(user_id):
    if request.method == "GET":
        if current_user.role == "Administrator":
            user = Users.query.filter_by(id = user_id).first()
            if user:
                db.session.delete(user)
                db.session.commit()
                flash(f"Account has been deleted" , 
                category="danger")
                return redirect(url_for("ALLUsers"))
        
        else:
            flash("What you sow you shall reap \n Your account has been deleted" , 
                category="danger")
            user = Users.query.filter_by(id = current_user.id).first()
            logout_user()
            db.session.delete(user)
            db.session.commit()
            return redirect(url_for("index"))

    else:
        render_template("DeleteUser.html") #  never come here but for 
                                        #            testing purposes





#--------------------------------------------------------------------------------------
#SECTIONS-------------------------------------------------------------------------------
"""
LVL 1
"""
@app.route("/Sections" , methods = ['GET' , 'POST'])
@login_required
def Sections():
    form = Controller_Forms.UploadSectionForm()
    sections = db.session.execute(db.select(SectionTable)).scalars()
    if (current_user.role =="Administrator"):
        
        
        if form.validate_on_submit():
            section = SectionTable.query.filter_by(name = form.name.data).first()
        
            if section:    
                flash("Section is already exists", category="warning")
                return redirect(url_for("Sections"))     
        
            else:
                
                
                New_Section = SectionTable(name=form.name.data,
                                          description = form.description.data
                                        )          
                db.session.add(New_Section)
                db.session.commit() 
                flash("Adding New Section Successfull" , category="success")
                return redirect(url_for("Sections")) 
    
        
        elif request.method == "POST":
            for fieldName, errorMessages in form.errors.items():
                for error in errorMessages:
                    flash(error,category="danger")
            return redirect(url_for("Section"))

        
        else:
            return render_template("AdminSections.html",sections = sections,form=form)
    
    else:
        return render_template("UserSections.html",sections = sections)


"""
Lvl 2 
""" 
@app.route("/Sections/<int:section_id>" , methods = ['GET' , 'POST'])
@login_required
def Section(section_id):
    section = SectionTable.query.filter_by(id = section_id).first()
    try:
        books = BooksTable.query.filter_by(section_id = section_id).all()
    except:
        pass
    if (current_user.role == "Administrator"):
        return render_template("AdminParticularSection.html",books = books,section = section)
    else:
        return render_template("UserParticularSection.html",books = books,section = section)
    




#--------------------------------------------------------------------------------------
#Need to update books and blob datatype also need to modify database so save this for 
    # later

#-------------------------------------------------------------------


#BOOKS
    

@app.route("/Books" , methods = ['GET' , 'POST'])
@login_required
def Books():
    books = db.session.execute(db.select(BooksTable)).scalars()
    if current_user.role == "Administrator":
        form = Controller_Forms.UploadBookForm()
        """orderFilter = request.args.get("filter") #makesure correct filter displayes as buttons
        try:
            books = db.engine.execute(f"SELECT * FROM books ORDERBY {orderFilter} ;")
        except:
            pass"""
        
        if form.validate_on_submit() or request.method == "POST":
            book = BooksTable(title = form.title.data , 
                        author = form.author.data ,
                        description =form.description.data ,
                        content=form.content.data.read(),
                        section_id = form.section_id.data
                        )
            db.session.add(book)
            db.session.commit() 
            flash("Upload Successfull" , category="success")
            return redirect(url_for("Books"))
        
        elif request.method=="POST":
            for fieldName, errorMessages in form.errors.items():
                for error in errorMessages:
                    flash(error,category="danger")
            return redirect(url_for("Books"))
        else:
            return render_template("AdminBooks.html",form = form , books = books)
    
    else:
        return render_template("UserBooks.html",books=books)

#Book Info
@app.route("/Books/<int:book_id>" , methods = ['GET' , 'POST']) #get id then book name pass book name in url but better to use id
@login_required
def Book(book_id): 
    if (current_user.role == "Administrator"):
        form = Controller_Forms.EditBookForm()
        if form.validate_on_submit():
            book = BooksTable.query.filter_by(id = book_id).first()
            if form.author.data:
                book.author = form.author.data
            if form.description.data:
                book.description = form.description.data
            if form.content.data:
                book.content = form.content.data.read()
                #also read pdf and put the first page as book_pic
            if form.section_id.data:
                book.section_id = form.section_id.data

            book.verified = True
            db.session.commit()    
            flash("Update Successfull" , category="success")
            return redirect(url_for("Book",book_id = book_id))

        elif request.method == "POST":
            for fieldName, errorMessages in form.errors.items():
                    for error in errorMessages:
                        flash(error,category="danger")
            return redirect(url_for("Book",book_id = book_id))

        else:

            
            book = BooksTable.query.filter_by( id = book_id).first()
            section = SectionTable.query.filter_by(id = book.section_id).first()
            if section:
                section = section.name
            bookFeedback = Feedbacks.query.filter_by(book_id = book_id)
            feedbacks = []
            for feedback in bookFeedback:
                feedbacks.append(( Users.query.filter_by( id = feedback.user_id).first(),
                                BooksTable.query.filter_by( id = feedback.book_id).first() ,
                                feedback.feedback,
                                feedback.rating
                                ))
                return render_template("AdminBookInfo.html",book= book,feedbacks = feedbacks , form = form,section = section)
    else:
        book = BooksTable.query.filter_by( id = book_id).first()
        section = SectionTable.query.filter_by(id = book.section_id).first()
        if section:
            section = section.name
        bookFeedback = Feedbacks.query.filter_by(book_id = book_id)
        feedbacks = []
        for feedback in bookFeedback:
            feedbacks.append(( Users.query.filter_by( id = feedback.user_id).first(),
                                BooksTable.query.filter_by( id = feedback.book_id).first() ,
                                feedback.feedback,
                                feedback.rating
                                ))
          
        return render_template("UserBookInfo.html",book = book,feedbacks = feedbacks,section = section)

#--------------------------------------------------------------------------------------
#Book DELETETION
#-------------------------------------------------------------------------------
@login_required
@app.route("/Books/Delete/<book_id>",methods = ["GET","POST"])
def DeleteBook(book_id):
    if request.method == "GET":
        if current_user.role == "Administrator":
            book = BooksTable.query.filter_by(id = book_id).first()
            if book:
                db.session.delete(book)
                db.session.commit()
                flash(f"Book has been deleted" , 
                category="danger")
                return redirect(url_for("Books"))
        
        else:
            flash(f"You cannot be here {current_user.name}" , 
                category="danger")
            logout_user()
            return redirect(url_for("index"))

    else:
        render_template("DeleteUser.html") #  never come here but for 
                                        #            testing purposes




 #######################################################################

# ALL USER CODE

#####################################################################