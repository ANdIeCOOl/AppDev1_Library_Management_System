from flask import Flask,render_template

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/Admin<ID>")
def AdminHomePage(ID):
    return render_template("Admin.html")


#Requests Page From Admin
@app.route("/Admin<ID>/Requests")
def AdminRequestsPage(ID):
    return render_template("Requests.html")

#Analytics Page From Admin
@app.route("/Admin<ID>/Analytics")
def AdminAnalyticsPage(ID):
    return render_template("Analytics.html")


# Users Page From Admin
@app.route("/Admin<ID>/Users")
def AdminUserPage(ID):
    return render_template("Users.html")


#Sections Page From Admin
@app.route("/Admin<ID>/Sections")
def AdminSectionsPage(ID):
    return render_template("Sections.html")


#Books Page From Admin
@app.route("/Admin<ID>/Books")
def AdminBooksPage(ID):
    return render_template("Books.html")


if (__name__ == "__main__"):
    app.run()