from flask import Flask,render_template

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/Admin<ID>")
def AdminHomePage(ID):
    return render_template("AdminHome.html", Link_To_Books = f"/Admin{ID}/Books")


#Requests Page From Admin
@app.route("/Admin<ID>/Requests")
def AdminRequestsPage(ID):
    return render_template("AdminRequests.html")

#Analytics Page From Admin
@app.route("/Admin<ID>/Analytics")
def AdminAnalyticsPage(ID):
    return render_template("AdminAnalytics.html")


# Users Page From Admin
@app.route("/Admin<ID>/Users")
def AdminUserPage(ID):
    return render_template("Admin_Users.html")


#Sections Page From Admin
@app.route("/Admin<ID>/Sections")
def AdminSectionsPage(ID):
    return render_template("AdminSections.html")


#Books Page From Admin
@app.route("/Admin<ID>/Books")
def AdminBooksPage(ID):
    return render_template("AdminBooks.html")


#Book Infor Page From Admin
@app.route("/Admin<ID>/Books/<BookID>")
def AdminBooksInfoPage(ID):
    #Have to send DataFrom DB HERE and use for loop to render all books in DB
    return render_template("AdminBookInfo.html")



 #######################################################################

# ALL USER CODE

#####################################################################



@app.route("/User<ID>")
def UserHomePage(ID):
    return render_template("UserHome.html")


#Requests Page From Admin
@app.route("/User<ID>/Books")
def UserRequestsPage(ID):
    return render_template("UserBooks.html")

#Analytics Page From Admin
@app.route("/User<ID>/Analytics")
def UserAnalyticsPage(ID):
    return render_template("UserAnalytics.html")


# Users Page From Admin
#@app.route("/Admin<ID>/Users")
#def AdminUserPage(ID):
#    return render_template("Users.html")


#Sections Page From Admin
@app.route("/User<ID>/Sections")
def UserSectionsPage(ID):
    return render_template("UserSections.html")


#Books Page From Admin
#@app.route("/Admin<ID>/Books")
#def AdminBooksPage(ID):
#    return render_template("Books.html")


if (__name__ == "__main__"):
    app.run(debug= True)