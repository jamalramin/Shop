from flask import Flask, request, render_template, render_template_string

app = Flask(__name__)

@app.route("/")
def welcome():
    return render_template("index.html")


@app.route("/login", methods = ["GET", "POST"])
def login():
    username = request.form.get("username")
    password = request.form.get("password")

    if request.method == "POST":
        if username == "ramin" and password == "123":
            print("you have enterd seccusfully")

        else :
            return render_template("login.html", error = "Login Failed!! You didn't enter the username or password correctly")
    return render_template("login.html")


@app.route("/home")
def home():
    return render_template("home.html")



@app.route("/register", methods = ["GET", "POST"])
def register():
    if request.method == "POST":
    
        pass1 = request.form.get("password1")
        pass2 = request.form.get("password2")

    
        if pass1 != pass2:
            return render_template("signup.html", error_signup = "your Passwords does not match!! ")
        
        else:
            print("thanks god")
    return render_template("signup.html")
        
    