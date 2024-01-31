from MVC import app
from MVC import Controller_Forms
from MVC.Model import Users,users_books
from MVC.Model import Sections as SectionTable
from MVC.Model import Requests as RequestsTable
from MVC.Model import Books as BooksTable
from MVC.Model import Feedbacks 
from MVC import db
from io import BytesIO

from flask import render_template, url_for,redirect,flash,request
from flask_login import login_user, logout_user, login_required, current_user, login_manager
from werkzeug.security import generate_password_hash, check_password_hash 
from base64 import b64encode,b64decode


#NAV BAR SEARCH FORM
@app.context_processor
def base():
    form1 = Controller_Forms.SearchForm()
    return dict(form1 = form1)

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
                
                current_user.logins = current_user.logins + 1
                current_user.verified = True
                db.session.commit()

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




#REGISTER-------------------IMPORTANT
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


#--------------------------
#SEARCH
#-----------
    
@app.route("/Search",methods = ["POST","GET"])
def Search():
    form1 = Controller_Forms.SearchForm()
    if form1.validate_on_submit:
        search = f"%{form1.search.data}%"
        search_in = form1.lookfor.data
        print(search_in) 
        if search_in == "Books":
            data = BooksTable.query.filter((BooksTable.title.like(search))).all()
            return render_template("Search.html",search = form1.search.data , data = data,search_in=search_in)
            
        
        if search_in == "Authors":
            data = BooksTable.query.filter( (BooksTable.author.like(search))).all()
            return render_template("Search.html",search = form1.search.data , data = data,search_in = search_in)

        if search_in == "Sections":
            data = SectionTable.query.filter((SectionTable.name.like(search))).all()
            return render_template("Search.html",search = form1.search.data , data = data,search_in = search_in )  
        
          
    elif request.method == "POST":
        for fieldName, errorMessages in form1.errors.items():
            for error in errorMessages:
                flash(error,category="danger")
        return redirect(url_for("Home"))
    else:
        
        return render_template ("Search.html",search = "Something went wrong \n not supposed to come here",
                                form1 = form1)






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
                book = BooksTable.query.filter_by(id = book_id).first()
                book.requests = book.requests + 1
                book.verified = True
                current_user.no_books_requested += 1
                if book.section_id:
                    section = SectionTable.query.filter_by(id = book.section_id).first()
                    section.requests += 1
                    section.verified = True

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

#----------------------
#Revoke access to Book for user no need restict user and book id 
    
#Revoke access for one or multiple e-book(s) from a user (not for a user so just remove)
#---------
@login_required
@app.route("/Revoke/<int:book_id><int:user_id>",methods = ["GET","POST"])
def RevokeBook(book_id,user_id):
    if request.method == "GET":
        db.session.execute(users_books.delete().where(users_books.columns.user_id == user_id).where(users_books.columns.book_id==book_id))
        db.session.commit()
        flash("Access Denied, You have successfully witheld knowledge",category="success")        
        return redirect(url_for("ModifyUser",user_id = user_id))
    



#--------------------------------------------------------------------------------------
#ANALYTICS-------------------------------------------------------------------------------
#-------

import matplotlib.pyplot as plt
import numpy as np

"""
LVL 1
"""
@app.route("/Analytics" , methods = ['GET' , 'POST'])
@login_required
def Analytics():
    if (current_user.role == "Administrator"):
        return render_template("AdminAnalytics.html")
    else:
        return render_template("Analytics_for_User.html")

"""
LVL 2
"""  
#ALL USERS ANALYTICS
@app.route("/Analytics/Users" , methods = ['GET' , 'POST'])
@login_required
def UsersAnalytics():
    if current_user.role == "Administrator":
        pass #Show all USer data
    else:
        user_login_data = None
        users = db.session.execute(db.select(Users)).scalars()
        feedbacks = Feedbacks.query.filter_by(user_id = current_user.id).all()
        user_feedback = 0
        sum = [0,0,0]
        f=0
        if feedbacks:
            for feedback in feedbacks:
                user_feedback += feedback.rating
            user_feedback /= len(feedbacks)
            feedbacks = db.session.execute(db.select(Feedbacks)).scalars()
            for feedback in feedbacks:
                sum[2] += feedback.rating
        n = db.session.query(Users).count() - 1 
        f = db.session.query(Feedbacks).count()
        if f == 0:
            f = 1
        #compare user login with avg user login--> categorical bargraph

        
        
        if n > 0 :
            for user in users:
                
                if user.role != "Administrator":
                    sum[0] += user.logins
                    sum[1]+=user.no_books_requested
            All_info = ["User Logins","User Book Requests","User Feedbacks Rating"]
            Some_data = {
                "You":(current_user.logins ,current_user.no_books_requested,user_feedback ),
                "Avg_User":(round(sum[0]/n),round(sum[1]/n),round(sum[2]/f))
            }
            
            
            plt.style.use('dark_background')
            """fig, ax = plt.subplots()

            ax.plot([1,2])
            user_axis = [current_user.name , "Other Users Average"]
            login_axis = [current_user.logins , sum/n ]
            bar_container = ax.bar(user_axis, login_axis)
            ax.set(ylabel='Logins', title='Login Comparison', ylim=(0,max(current_user.logins  ,sum/n ) ))
            ax.bar_label(bar_container, fmt='{:,.0f}')"""

            x = np.arange(len(All_info))  # the label locations
            width = 0.25  # the width of the bars
            multiplier = 0

            fig, ax = plt.subplots(layout='constrained')

            for attribute, measurement in Some_data.items():
                offset = width * multiplier
                rects = ax.bar(x + offset, measurement, width, label=attribute)
                ax.bar_label(rects, padding=3)
                multiplier += 1

            # Add some text for labels, title and custom x-axis tick labels, etc.
            ax.set_ylabel('No of ')
            ax.set_title('You Vs Average User')
            ax.set_xticks(x + width, All_info)
            ax.legend(loc='upper left', ncols=3)
            ax.set_ylim(0,max(sum))


            buf = BytesIO()

            fig.savefig(buf , format = "png")

            user_login_data = b64encode(buf.getbuffer()).decode("ascii")
            return render_template ("SingleUserProfileAnalytics.html", user_login_data= user_login_data)


        #compare user books requested with avg user books requested --> categorical bargraph
        # users feed backs of books bookname-->x axis , rating --> y axis


#System Analytics Visits CLicks etc
@app.route("/Analytics/System" , methods = ['GET' , 'POST'])
@login_required
def SystemAnalytics():
    pass
#Book Analytics highest rating, most requested etc
@app.route("/Analytics/Books" , methods = ['GET' , 'POST'])
@login_required
def BooksAnalytics(): #ALL BOOKS
    if current_user.role == "Administrator":
        pass #Same as user
    else:
        requests = []
        visits = []
        rating = []
        books = db.session.execute(db.select(BooksTable)).scalars()
        for book in books:
            requests.append(book.requests)
            visits.append(book.visits)
            rating.append(book.rating)

        requests = np.array(requests)
        visits = np.array(visits)
        rating = np.array(rating)

        n = db.session.query(BooksTable).count() 
            
            
        plt.style.use('dark_background') 
        fig, ax = plt.subplots(layout='constrained')
        colors = np.random.rand(n)
        plt.scatter(requests, visits, c=colors)
        ax.set_title('Vists Vs Requests for all the Books')
        ax.set_ylabel('Vists ')
        ax.set_xlabel('Requests ')

        buf = BytesIO()

        fig.savefig(buf , format = "png")

        book_data1 = b64encode(buf.getbuffer()).decode("ascii")

        plt.style.use('dark_background') 
        fig, ax = plt.subplots(layout='constrained')
        colors = np.random.rand(n)
        plt.scatter(requests, rating, c=colors)
        ax.set_title('Ratings Vs Requests for all the Books')
        ax.set_ylabel('Ratings ')
        ax.set_xlabel('Requests ')

        buf = BytesIO()

        fig.savefig(buf , format = "png")

        book_data2 = b64encode(buf.getbuffer()).decode("ascii")

        plt.style.use('dark_background') 
        fig, ax = plt.subplots(layout='constrained')
        colors = np.random.rand(n)
        plt.scatter( rating, visits ,c=colors)
        ax.set_title('Visits Vs Ratings for all the Books')
        ax.set_ylabel('Visits ')
        ax.set_xlabel('Rating ')

        buf = BytesIO()

        fig.savefig(buf , format = "png")

        book_data3 = b64encode(buf.getbuffer()).decode("ascii")



        return render_template ("Books_ANAlytics.html",book_data1 = book_data1 
                                                        ,book_data2= book_data2
                                                        ,book_data3= book_data3)

#Section Analytics highest rating, most visted etc
@app.route("/Analytics/Sections" , methods = ['GET' , 'POST'])
@login_required
def SectionsAnalytics():
    sections = db.session.execute(db.select(SectionTable)).scalars()
    if sections:
        names = []
        visits = []
        requests = []
        for section in sections:
            names.append(section.name)
            visits.append(section.visits)
            requests.append(section.requests)        



        All_info = [name for name in names]
        Some_data = {
            "Visits":visits,
            "Requests":requests 
        }
                    
        plt.style.use('dark_background')
        """fig, ax = plt.subplots()
            ax.plot([1,2])
            user_axis = [current_user.name , "Other Users Average"]
            login_axis = [current_user.logins , sum/n ]
            bar_container = ax.bar(user_axis, login_axis)
            ax.set(ylabel='Logins', title='Login Comparison', ylim=(0,max(current_user.logins  ,sum/n ) ))
            ax.bar_label(bar_container, fmt='{:,.0f}')"""

        x = np.arange(len(All_info))  # the label locations
        width = 0.25  # the width of the bars
        multiplier = 0
        fig, ax = plt.subplots(layout='constrained')

        for attribute, measurement in Some_data.items():
            offset = width * multiplier
            rects = ax.bar(x + offset, measurement, width, label=attribute)
            ax.bar_label(rects, padding=3)
            multiplier += 1

        # Add some text for labels, title and custom x-axis tick labels, etc.
        ax.set_ylabel('Count')
        ax.set_title('Sectionwise Visits and Requests')
        ax.set_xticks(x + width, All_info)
        ax.legend(loc='upper left', ncols=3)
        ax.set_ylim(0,max(max(visits),max(requests)) + 30)


        buf = BytesIO()

        fig.savefig(buf , format = "png")

        user_login_data = b64encode(buf.getbuffer()).decode("ascii")
        return render_template ("SingleUserProfileAnalytics.html", user_login_data= user_login_data)
    
    
    else:
        flash("There no Sections to Display Analytics",category="warning")
        return redirect(url_for("Analytics"))
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
        book = BooksTable.query.filter_by(id = book_id).first()
        n = Feedbacks.query.filter_by(book_id = book_id).count()
        ratings = Feedbacks.query.filter_by(book_id = book_id).all()
        sum = 0
        for rating in ratings:
            sum += rating.rating


        if n == 0:
            book.rating = form.rating.data 
        else:
            book.rating = (form.rating.data + sum)/n
        book.verified = True
        db.session.add(feedback)
        db.session.commit()
        flash("Thank you for the feedback",category="success")
        return redirect(url_for("ModifyUser",user_id = current_user.id))
    else:
        for fieldName, errorMessages in form.errors.items():
            for error in errorMessages:
                flash(error,category="danger")
        return redirect(url_for("ModifyUser",user_id = current_user.id))
    
@login_required
@app.route("/Taken/<int:book_id>",methods = ["GET","POST"])
def TakeBook(book_id):
    db.session.execute(users_books.delete().where(users_books.columns.user_id == current_user.id).where(users_books.columns.book_id==book_id))
    db.session.commit()
    flash("You have exceeded the time Limit for you Book",category="warning")
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
                db.session.execute(users_books.delete().where(users_books.columns.user_id == user.id))
                db.session.delete(user)
                db.session.commit()
                flash(f"Account has been deleted" , 
                category="danger")
                return redirect(url_for("ALLUsers"))
        
        else:
            flash("What you sow you shall reap \n Your account has been deleted" , 
                category="danger")
            user = Users.query.filter_by(id = current_user.id).first()
            db.session.execute(users_books.delete().where(users_books.columns.user_id == current_user.id))
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
    section.visits += 1
    section.verified = True
    db.session.commit() 
    try:
        books = BooksTable.query.filter_by(section_id = section_id).all()
    except:
        pass
    if (current_user.role == "Administrator"):
        return render_template("AdminParticularSection.html",books = books,section = section)
    else:
        
        return render_template("UserParticularSection.html",books = books,section = section)
    


@app.route("/Sections/DELETE <int:section_id>" , methods = ['GET' , 'POST'])
@login_required
def DeleteSection(section_id):
    if (current_user.role == "Administrator"):
        section = SectionTable.query.filter_by(id = section_id).first()
        try:
            books = BooksTable.query.filter_by(section_id = section_id).all()
            for book in books:
                book.section_id = None
        except:
            flash("SOME ERROR IN DELTETING SECTION",category = "warning")
        db.session.delete(section)
        db.session.commit()
        flash(f"Section has been deleted",category="danger")
        return redirect(url_for("Sections"))



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
            readers = book.current_readers
            print("Test 1 ------ \n --------\n")
            section = SectionTable.query.filter_by(id = book.section_id).first()
            print("Test  2------ \n --------\n")
            if section:
                section = section.name
                print("Test  3 ------ \n --------\n")
            bookFeedback = Feedbacks.query.filter_by(book_id = book_id)
            feedbacks = []
            print("Test  4 ------ \n --------\n")
            for feedback in bookFeedback:
                feedbacks.append(( Users.query.filter_by( id = feedback.user_id).first(),
                                BooksTable.query.filter_by( id = feedback.book_id).first() ,
                                feedback.feedback,
                                feedback.rating
                                ))
            print("Test  5 ------ \n --------\n")
            return render_template("AdminBookInfo.html",book= book,feedbacks = feedbacks , form = form,section = section)
    else:
        
        book = BooksTable.query.filter_by( id = book_id).first()
        book.visits = book.visits + 1
        book.verified = True
        section = SectionTable.query.filter_by(id = book.section_id).first()
        if section:
            section.visits += 1
            section.verified = True
        
        db.session.commit()

        
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

#--------------------
#READ A BOOK
#---------
@app.route('/ReadPDF/<book_id>')
def ReadinBrowser(book_id):
    if book_id is not None:
        book = BooksTable.query.filter_by(id = book_id).first()
        pdf = book.content
        response = make_response(pdf)
        response.headers['Content-Type'] = 'application/pdf'
        response.headers['Content-Disposition'] = \
            'inline; filename=%s.pdf' % 'yourfilename'
        return response
    
from datetime import date
from flask import make_response
@app.route("/Books/<int:book_id>/Read" , methods = ['GET' , 'POST'])
@login_required
def ReadBook(book_id):
        
        
        entry = db.session.execute(users_books.select().where(users_books.columns.user_id == current_user.id).where(users_books.columns.book_id==book_id)).first()
        """
        for row in entries:
            print("---------- \n ------------\n ------------ \n")
            print(date.today())
            x = row[2].rsplit("/")
            doi = date(int(x[2]),int(x[1]),int(x[0]))
            dor = date(int(x[2]),int(x[1]),int(x[0]) + 7)
            print( date.today().strftime("%d/%m/%Y") > "22/02/2024")
            print( date.today() > doi)
            print(dor)
            print(doi)
            print("---------- \n ------------\n ------------ \n")
         
           """
        if entry:
            x = entry[2].rsplit("/")

            dor = date(int(x[2]),int(x[1]),int(x[0]) + 7)
            if dor > date.today():
                book = BooksTable.query.filter_by(id = book_id).first()
                
                pdf_blob = book.content


                if pdf_blob[0:4] != b'%PDF':
                    flash('Missing the PDF file signature,Data is corrupted \n Please Remove this book and report it to the Librarian')
                    return redirect(url_for("ModifyUser",user_id = current_user.id))
                
                return render_template("ReadingBook.html",book_id = book_id)
            else:
                return redirect(url_for("TakeBook",book_id = book_id))

        else:
            flash("You dont have access to this Book." , category="warning")
            return redirect(url_for("ModifyUser",user_id = current_user.id))

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
                db.session.execute(users_books.delete().where(users_books.columns.book_id==book_id))
                feedbacks = Feedbacks.query.filter_by(book_id = book_id)
                db.session.delete(feedbacks)
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