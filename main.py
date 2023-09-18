from flask import Flask, request, session, redirect
from flask import render_template

app = Flask(__name__)

# Set the secret key to some random bytes. Keep this really secret!
app.secret_key = b"cvobidrnsuerbsifurf34ads"


@app.route("/")
def home():
    if "username" in session:
        return render_template("user-home.html", username=session["username"])
    return render_template("no-session.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        # TODO: check if user exists and password is valid
        session["username"] = request.form["username"]
        return redirect("/")
    return render_template("login.html")


@app.route("/logout")
def logout():
    # remove the username from the session if it's there
    session.pop("username", None)
    return redirect("/")
