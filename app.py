from flask import Flask,render_template

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/Admin<ID>") #LVL 1
def AdminHomePage(ID):
    return render_template("AdminHome.html", 
                        Link_To_Books = f"/Admin{ID}/Books",
                        Link_To_Sections = f"/Admin{ID}/Sections",
                        Link_To_Requests = f"/Admin{ID}/Requests",
                        Link_To_Analytics = f"/Admin{ID}/Analytics",
                        Link_To_Users = f"/Admin{ID}/Users")


#Requests Page From Admin LVL 2
@app.route("/Admin<ID>/Requests")
def AdminRequestsPage(ID):
    return render_template("AdminRequests.html", 
                        Link_To_PendingRequests = f"/Admin{ID}/Requests/Pending",
                        Link_To_RequestHistory = f"/Admin{ID}/Requests/History")

#PenindingRequests Page From Admin #LVL 3
@app.route("/Admin<ID>/Requests/Pending")
def AdminPendingRequestsPage(ID):
    return render_template("AdminPendingRequests.html")

#Requests History Page From Admin#LVL 3
@app.route("/Admin<ID>/Requests/History")
def AdminHistoryRequestsPage(ID):
    return render_template("AdminRequestsHistory.html")

#Request Analytics #LVL 3







#Analytics Page From Admin
@app.route("/Admin<ID>/Analytics")
def AdminAnalyticsPage(ID):
    return render_template("AdminAnalytics.html")

#Overall User Analytics
# Indivdual
#Book Analytics
#Section Analytics
#Request Analytics #LVL 3







# Users Page From Admin
@app.route("/Admin<ID>/Users") #LVL 2
def AdminUserPage(ID):
    #From DB Sent All user data to display
    return render_template("AdminUsers.html")

@app.route("/Admin<ID>/Users/User<User_ID>")
def AdminUserProfile(ID,User_ID):
    return render_template("UserProfile.html")


#Overall User Analytics #LVL 3








#Sections Page From Admin
@app.route("/Admin<ID>/Sections") #LVL2
def AdminSectionsPage(ID):
    return render_template("AdminSections.html")

@app.route("/Admin<ID>/Sections/<SectionID>") #LVL 3 
def AdminParticularSection(ID,SectionID):
    return render_template("AdminParticularSection.html")






#Books Page From Admin
@app.route("/Admin<ID>/Books") #LVL 2
def AdminBooksPage(ID):
    return render_template("AdminBooks.html")


#Book Info Page From Admin
@app.route("/Admin<ID>/Books/<BookID>") #LVL 3
def AdminBooksInfoPage(ID,BookID):
    #Have to send DataFrom DB HERE and use for loop to render all books in DB
    return render_template("AdminBookInfo.html")




 #######################################################################

# ALL USER CODE

#####################################################################



@app.route("/User<ID>")
def UserHomePage(ID):
    return render_template("UserHome.html",
                           Link_to_Sections=f"/User{ID}/Sections",
                           Link_to_UserAnalytics= f"/User{ID}/Analytics",
                           Link_to_Books = f"/User{ID}/Books")


#Requests and Books Page From User
@app.route("/User<ID>/Books")
def UserRequestsPage(ID):
    return render_template("UserBooks.html")

@app.route("/User<ID>/Books/<Book_ID>")
def UserBookInfoPage(ID,Book_ID):
    return render_template("UserBookInfo.html")



#Analytics Page From User
@app.route("/User<ID>/Analytics")
def UserAnalyticsPage(ID):
    return render_template("UserAnalytics.html")






#Sections Page From User
@app.route("/User<ID>/Sections")
def UserSectionsPage(ID):
    return render_template("UserSections.html")

@app.route("/User<ID>/Sections/<Section_ID>")
def UserParticularSectionsPage(ID,Section_ID):
    return render_template("UserParticularSection.html")





if (__name__ == "__main__"):
    app.run(debug= True)