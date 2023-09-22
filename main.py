from flask import Flask, request, session, redirect, render_template, url_for, flash
import re
from database import *

app = Flask(__name__)

# Set the secret key to some random bytes. Keep this really secret!
app.secret_key = b"cvobidrnsuerbsifurf34ads"

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
]


@app.route("/")
def home():
    if "username" in session:
        return render_template("user-home.html", username=session["username"])
    return render_template("no-session.html")


@app.route("/flight-search", methods=["GET"])
def flight_search():
    return render_template("flight-search.html")


def is_valid_registration_data(firstName, lastName, email, password):
    if not firstName or not lastName:
        return False

    email_pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    if not re.match(email_pattern, email):
        return False

    if len(password) < 8:
        flash('Password must be 8 characters or longer')
        return False

    return True


@app.route("/sign-up", methods=["GET", "POST"])
def sign_up():
    if request.method == "POST":
        firstName = request.form["firstName"]
        lastName = request.form["lastName"]
        email = request.form["email"]
        password = request.form["password"]

        if is_valid_registration_data(firstName, lastName, email, password):
            save_signup_information(firstName, lastName, email, password)
            return redirect(url_for('flight_search'))

    return render_template("sign-up.html")


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user_type = get_user_role(username, password)

        if user_type:
            session['user_type'] = user_type  # Store user_role in session to recognize the user across requests.

            if user_type == 'Client':
                return redirect(
                    url_for('search_flights'))  # Redirect to the flight search page if the user is a client.
            elif user_type == 'Employee':
                return redirect(
                    url_for('manage_requests'))  # Redirect to the manage requests page if the user is an employee.
        else:
            flash('Invalid login credentials. Please try again or sign up.', 'error')
            return redirect(url_for('login'))
    return render_template('login.html')

@app.route('/search_flights')
def search_flights():
    # Your logic for flight search
    return render_template('flight-search.html')

@app.route('/manage_requests')
def manage_requests():
    # Your logic for managing requests
    return render_template('employee-home.html')



@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


@app.route("/select-flight", methods=["GET"])
def select_flight():
    flight_number = request.args.get("flight_number")
    direction = request.args.get("direction")
    departure = request.args.get("departure")
    destination = request.args.get("destination")
    departure_date = request.args.get("departure_date")
    return_date = request.args.get("return_date")
    person_count = request.args.get("person_count")

    if direction == "outward":
        # Save outward flight data into session.
        session["outward_flight"] = flight_number

    if direction == "return":
        # Save return flight data into session.
        session["return_flight"] = flight_number
        return redirect("/booking-summary")

    return render_template(
        "select-flight.html",
        outward_flights=outward_flights,
        direction=direction,
        departure=departure,
        destination=destination,
        departure_date=departure_date,
        return_date=return_date,
        person_count=person_count,
    )


@app.route("/booking-summary", methods=["GET"])
def booking_summary():
    return render_template(
        "booking-summary.html",
        outward_flight=session["outward_flight"],
        return_flight=session["return_flight"],
    )


if __name__ == "__main__":
    app.run(debug=True)
