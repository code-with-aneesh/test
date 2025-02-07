from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    session,
    flash,
    jsonify,
)
from config import Config
from werkzeug.security import generate_password_hash, check_password_hash
from pymongo import MongoClient
from bson.objectid import ObjectId

app = Flask(__name__)
app.config.from_object(Config)

# Initialize MongoDB
client = MongoClient(app.config["MONGO_URI"])
db = client["test"]  # Use the 'test' database


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
        hashed_password = generate_password_hash(password, method="pbkdf2:sha256")
        new_user = Login(username=username, password=hashed_password)

        try:
            users_collection = db["test"]  # Use the 'test' collection
            users_collection.insert_one(
                {"username": username, "password": hashed_password}
            )
            flash("Registration successful! Please log in.", "success")
            return redirect(url_for("login"))
        except Exception as e:
            flash(f"An error occurred: {e}", "danger")

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        try:
            users_collection = db["test"]  # Use the 'test' collection
            user = users_collection.find_one({"username": username})
            if user and check_password_hash(user["password"], password):
                session["account"] = {"username": username, "user_id": str(user["_id"])}
                return redirect(url_for("dashboard"))
            else:
                flash("Login failed. Incorrect username or password.", "danger")
        except Exception as e:
            flash(f"An error occurred: {e}", "danger")

    return render_template("login.html")


@app.route("/logout")
def logout():
    session.pop("account", None)
    flash("You have been logged out.", "info")
    return redirect(url_for("login"))


@app.route("/dashboard")
def dashboard():
    if "account" in session:
        user_id = session["account"]["user_id"]
        todos = db["todos"].find({"user_id": user_id})
        return render_template("dashboard.html", user=session["account"], todos=todos)
    else:
        flash("You are not logged in.", "warning")
        return redirect(url_for("login"))


@app.route("/add_todo", methods=["POST"])
def add_todo():
    if "account" in session:
        user_id = session["account"]["user_id"]
        todo_text = request.form["todo"]
        db["todos"].insert_one({"user_id": user_id, "text": todo_text, "done": False})
        return redirect(url_for("dashboard"))
    else:
        flash("You are not logged in.", "warning")
        return redirect(url_for("login"))


@app.route("/delete_todo/<todo_id>")
def delete_todo(todo_id):
    if "account" in session:
        db["todos"].delete_one({"_id": ObjectId(todo_id)})
        return redirect(url_for("dashboard"))
    else:
        flash("You are not logged in.", "warning")
        return redirect(url_for("login"))


@app.route("/toggle_todo/<todo_id>")
def toggle_todo(todo_id):
    if "account" in session:
        todo = db["todos"].find_one({"_id": ObjectId(todo_id)})
        new_status = not todo["done"]
        db["todos"].update_one(
            {"_id": ObjectId(todo_id)}, {"$set": {"done": new_status}}
        )
        return redirect(url_for("dashboard"))
    else:
        flash("You are not logged in.", "warning")
        return redirect(url_for("login"))


if __name__ == "__main__":
    app.run(debug=True)
