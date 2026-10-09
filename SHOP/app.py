from http.client import CREATED

from flask import Flask, request, render_template, render_template_string, redirect, session, url_for
import sqlite3
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)
app.secret_key = "change-this-to-a-random-secret"

with sqlite3.connect("usersinfo.db") as connection:
    connection.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password_hash TEXT NOT NULL
        )
    """)

@app.route("/")
def welcome():
    return render_template("index.html")


@app.route("/login", methods = ["GET", "POST"])
def login():

    
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        
        
        with sqlite3.connect("usersinfo.db") as connection:
            user = connection.execute(
                "SELECT password_hash FROM users WHERE username = ?",
                (username,)
            ).fetchone()


        if username and check_password_hash(user[0], password):
            session["username"] = username
            print("you have enterd seccusfully")
            return redirect(url_for("home"))

        else:
            return render_template("login.html",error="Username or password is incorrect!")


    return render_template("login.html")

@app.route("/home")
def home():
    return render_template("home.html")



@app.route("/register", methods = ["GET", "POST"])
def register():

    if request.method == "POST":

        username = request.form.get("username", "").strip()
        pass1 = request.form.get("password1", "")
        pass2 = request.form.get("password2", "")


        if pass1 != pass2:
            return render_template("signup.html", error_signup = "your Passwords does not match!! ")
        
       
        try:
            with sqlite3.connect("usersinfo.db") as connection:
                connection.execute(
                    "INSERT INTO users (username, password_hash) VALUES (?, ?)",
                    (username, generate_password_hash(pass1))
                )

            return render_template(
                "login.html",
                error="Registration successful! Please log in."
            )

        except sqlite3.IntegrityError:
            return render_template(
                "signup.html",
                error_signup="Username already exists!"
            )

        
    return render_template("signup.html")
        


if __name__ == "__main__":
    app.run(debug=True)
