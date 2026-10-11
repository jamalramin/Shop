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
    # return render_template("index.html")

   return render_template("products.html")


@app.route("/index")
def logout():
    return render_template("index.html")


@app.route("/login", methods = ["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        
        with sqlite3.connect("usersinfo.db") as connection:
            username = connection.execute(
                "SELECT password_hash FROM users WHERE username = ?",
                (username,)
            ).fetchone()


        if username and check_password_hash(username[0], password):
            session["username"] = username
            print("you have enterd seccusfully")
            return redirect(url_for("index"))

        else:
            return render_template("login.html",error="Username or password is incorrect!")


    return render_template("login.html")



@app.route("/products")
def index():
    return render_template("products.html")

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

        
@app.route("/products")
def products():
    return render_template("products.html")

@app.route("/sell")
def sell():
    return render_template("sell.html")

@app.route("/buy")
def buy():
    return render_template("buy.html")

@app.route("/history")
def history():
    return render_template("history.html")



if __name__ == "__main__":
    app.run(debug=True)


