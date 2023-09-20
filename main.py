from flask import Flask, request, session, redirect
from flask import render_template
import re

app = Flask(__name__)

# Set the secret key to some random bytes. Keep this really secret!
app.secret_key = b"cvobidrnsuerbsifurf34ads"


# Statische Flugdaten (für Demonstrationszwecke)
outward_flights = [
    {
        "flight_number": "ABC123",
        "departure_city": "New York",
        "destination_city": "Los Angeles",
        "departure_time": "09:00 AM",
        "arrival_time": "02:00 PM",
        "economy_price": 300,
        "business_price": 600,
        "first_class_price": 1000,
    }
    # Weitere Hinflugdaten
]

return_flights = [
    {
        "flight_number": "XYZ456",
        "departure_city": "Los Angeles",
        "destination_city": "New York",
        "departure_time": "03:00 PM",
        "arrival_time": "08:00 PM",
        "economy_price": 300,
        "business_price": 600,
        "first_class_price": 1000,
    }
    # Weitere Rückflugdaten
]


@app.route("/")
def home():
    if "username" in session:
        return render_template("user-home.html", username=session["username"])
    return render_template("no-session.html")


@app.route("/flight_search", methods=["GET"])
def flight_search():
    return render_template("flight_search.html")


def is_valid_registration_data(firstName, lastName, email, password):
    # Prüfe, ob Vorname und Nachname nicht leer sind
    if not firstName or not lastName:
        return False

    # Prüfe, ob die E-Mail-Adresse ein gültiges E-Mail-Format hat
    email_pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    if not re.match(email_pattern, email):
        return False

    # Prüfe, ob das Passwort bestimmte Anforderungen erfüllt, z. B. Mindestlänge
    if len(password) < 8:
        return False

    # Hier kannst du weitere Validierungen hinzufügen, wie z. B. Passwortstärke oder eindeutige E-Mail-Adressen

    # Wenn alle Validierungen erfolgreich sind, gibt die Funktion True zurück
    return True


@app.route("/sign_up", methods=["GET", "POST"])
def sign_up():
    if request.method == "POST":
        firstName = request.form["firstName"]
        lastName = request.form["lastName"]
        email = request.form["email"]
        password = request.form["password"]

        if is_valid_registration_data(firstName, lastName, email, password):
            return redirect("/flight_search")

    return render_template("sign_up.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        # TODO: check if user exists and password is valid
        session["username"] = request.form["username"]
        return redirect("/flight_search")
    return render_template("login.html")


@app.route("/logout")
def logout():
    # remove the username from the session if it's there
    session.pop("username", None)
    return redirect("/")


@app.route("/search", methods=["POST"])
def search():
    # Hier könntest du eine Datenbankabfrage oder andere Suchlogik durchführen
    # Für dieses Beispiel verwenden wir statische Flugdaten
    return render_template("search_results.html", outward_flights=outward_flights)


@app.route("/select-outward-flight", methods=["POST"])
def select_outward_flight():
    selected_outward_flight = request.form["selected-outward-flight"]
    # Hier könntest du die ausgewählten Flugdaten in der Sitzung speichern
    session["selected_outward_flight"] = selected_outward_flight
    return render_template("select-return-flight.html", return_flights=return_flights)


@app.route("/select-return-flight", methods=["POST"])
def select_return_flight():
    selected_return_flight = request.form["selected-return-flight"]
    session["selected_return_flight"] = selected_return_flight
    return render_template("booking-summary.html")


if __name__ == "__main__":
    app.run(debug=True)
