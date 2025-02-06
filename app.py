from flask import Flask, render_template, request, redirect, url_for, session
from flask_pymongo import PyMongo
from config import Config  # Import configuration class

app = Flask(__name__)
app.config.from_object(Config)  # Load configuration from config.py

# Initialize PyMongo for MongoDB connection
mongo = PyMongo(app)


# Define the login model
class Login:
    def __init__(self, username, password):
        self.username = username
        self.password = password


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        new_user = Login(username=username, password=password)

        # Insert the user into the 'test' collection in MongoDB
        db = mongo.cx["test"]  # Replace 'test' with your MongoDB database name
        collection = db["test"]  # Replace 'test' with your collection name
        collection.insert_one({"username": username, "password": password})

        return redirect(url_for("login"))

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        # Query the user from the MongoDB Atlas database
        db = mongo.cx["test"]  # Replace 'test' with your database name
        collection = db["test"]  # Replace 'test' with your collection name
        user = collection.find_one({"username": username, "password": password})

        if user:
            session["account"] = {"username": user["username"]}
            return redirect(url_for("dashboard"))
        else:
            return "Login failed. Incorrect username or password."

    return render_template("login.html")


@app.route("/logout")
def logout():
    session.pop("account", None)
    return redirect(url_for("login"))


@app.route("/dashboard")
def dashboard():
    if "account" in session:
        return render_template("dashboard.html", user=session["account"])
    else:
        return "You are not logged in."


@app.route("/test")
def test():
    return render_template("test.html")


if __name__ == "__main__":
    app.run(debug=True)
