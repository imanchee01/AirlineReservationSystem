from flask import Flask, request, session, redirect
from flask import render_template

app = Flask(__name__)

# Set the secret key to some random bytes. Keep this really secret!
app.secret_key = b"cvobidrnsuerbsifurf34ads"


@app.route("/")
def home():
    if "username" in session:
        return render_template("flight_search.html", username=session["username"])
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


@app.route("/search", methods=["POST"])
def search_flights():
    departure_date = request.form["departure-date"]
    return_date = request.form["return-date"]

    # Hier solltest du die Flugdaten aus deiner Datenquelle abrufen.
    # Dies ist ein Dummy-Beispiel, in dem wir statische Daten verwenden:
    flights = [
        {
            "flight_number": "ABC123",
            "departure_city": "New York",
            "destination_city": "Los Angeles",
            "departure_date": "2023-10-15",
            "return_date": "2023-10-20",
        },
        # Weitere Flugdaten hier
    ]

    return render_template("search_results.html", flights=flights)


# ... (deine anderen Routen)

if __name__ == "__main__":
    app.run(debug=True)
