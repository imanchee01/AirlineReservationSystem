from flask import request, session, redirect, flash, url_for
from flask import render_template
from database import *
import re

outward_flights = [
    {
        "flightcode": "ABC123",
        "flight_source": "New York",
        "flight_destination": "Los Angeles",
        "flight_depTime": "09:00 AM",
        "flight_arrtime": "02:00 PM",
        "flight_economy_price": 300,
        "flight_business_price": 600,
        "flight_first_class_price": 1000,
    }
]

return_flights = [
    {
        "flightcode": "XYZ456",
        "flight_source": "Los Angeles",
        "flight_destination": "New York",
        "flight_depTime": "03:00 PM",
        "flight_arrtime": "08:00 PM",
        "flight_economy_price": 300,
        "flight_business_price": 600,
        "flight_first_class_price": 1000,
    }
]


@app.route("/")
def home():
    if "user_name" in session:
        return render_template("user-home.html", user_name=session["user_name"])
    return render_template("no-session.html")


@app.route("/flight-search", methods=["GET"])
def flight_search():
    return render_template("flight-search.html")


@app.route("/client-account", methods=["GET"])
def client_account():
    return render_template("client-account.html")


def is_valid_registration_data(firstName, lastName, email, password):
    if not firstName or not lastName:
        return False

    email_pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    if not re.match(email_pattern, email):
        return False

    if len(password) < 8:
        flash('Password must be 8 characters or longer')
        return False

    # if useremail already exists throw an error
    if user_with_email_exists(email):
        flash('Email already in use')
        return False

    return True


@app.route("/sign-up", methods=["GET", "POST"])
def sign_up():
    if request.method == "POST":
        firstName = request.form["firstName"]
        lastName = request.form["lastName"]
        email = request.form["email"]
        password = request.form["password"]

        try:
            if is_valid_registration_data(firstName, lastName, email, password):
                save_signup_information(firstName, lastName, email, password)
                return redirect(url_for("flight_search"))

        except Exception as e:
            app.logger.error("Error! " + str(e))
            flash('Failed to sign up.', 'error')

        return redirect(url_for("sign_up"))

    return render_template("sign-up.html")


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')

    user_email = request.form['user_email']
    user_password = request.form['user_password']

    # Query the user with the provided username from the database.
    user = get_user(user_email)

    if user and user.check_password(user_password):
        session['user_name'] = user.user_name
        # Password is correct.
        if user.user_type == "Client":
            # Redirect to the flight search page if the user is a client.
            return redirect(url_for("search_flights"))
        if user.user_type == "Employee":
            # Redirect to the manage requests page if the user is an employee.
            return redirect(url_for("manage_requests"))

    # Username or password is incorrect (or we have a user who is not a client nor an employee).
    flash('Invalid login credentials. Please try again or sign up.', 'error')
    return redirect(url_for("login"))


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


@app.route('/search-flights')
def search_flights():
    # Your logic for flight search
    return render_template("flight-search.html")


@app.route("/select-flight", methods=["GET"])
def select_flight():
    flight_code = request.args.get("flightcode")
    direction = request.args.get("direction")
    departure = request.args.get("departure")
    destination = request.args.get("destination")
    departure_date = request.args.get("departure_date")
    return_date = request.args.get("return_date")
    person_count = request.args.get("person_count")
    selected_class = request.args.get("selected_class")
    extra_luggage = request.args.get("extra_luggage")
    # Save departure and return date and number of passengers into session.
    session["departure_date"] = departure_date
    session["return_date"] = return_date
    session["person_count"] = person_count

    if direction == "outward":
        # Save outward flight data (code, pirce, luggage) into session.
        session["outward_flight"] = flight_code
        session["outward_selected_class"] = selected_class
        session["outward_extra_luggage"] = extra_luggage

    if direction == "return":
        # Save return flight data(code, pirce, luggage) into session.
        session["return_flight"] = flight_code
        session["return_selected_class"] = selected_class
        session["return_extra_luggage"] = extra_luggage

        return redirect("booking-summary")

    return render_template(
        "select-flight.html",
        flights=outward_flights,
        direction=direction,
        departure=departure,
        destination=destination,
        departure_date=departure_date,
        return_date=return_date,
        person_count=person_count,
    )


@app.route("/booking-summary", methods=["GET"])
def booking_summary():
    # TODO: get price for flight and luggage from DB
    return render_template(
        "booking-summary.html",
        outward_flight=session["outward_flight"],
        return_flight=session["return_flight"],
        outward_selected_class=session["outward_selected_class"],
        return_selected_class=session["return_selected_class"],
        outward_extra_luggage=session["outward_extra_luggage"],
        return_extra_luggage=session["return_extra_luggage"],
        departure_date=session["departure_date"],
        return_date=session["return_date"],
        person_count=session["person_count"],
    )


@app.route("/check-out", methods=["GET", "POST"])
def check_out():
    if request.method == 'GET':
        return render_template('check-out.html')

    salutation = request.form.get("salutation")
    last_name = request.form.get("last_name")
    first_name = request.form.get("first_name")
    email = request.form.get("email")
    address = request.form.get("address")
    phone = request.form.get("phone")
    payment_option = request.form.get("payment_option")

    return redirect(url_for("order_confirnation"))


@app.route("/order-confirmation", methods=["GET", "POST"])
def order_confirmation():
    return render_template("order-confirmation.html")

# manage request opens employee home
@app.route('/manage-requests')
def manage_requests():
    return render_template('employee-home.html', user_name=session.get("user_name"))

@app.route('/edit-aircrafts', methods=['GET'])
def edit_aircrafts():
    aircrafts = get_all_aircrafts()
    return render_template('edit-aircrafts.html', aircrafts=aircrafts)
@app.route('/edit-aircraft/<int:id>', methods=['GET'])
def edit_aircraft(id):
    # Your logic here, for example:
    aircraft = get_aircraft_by_id(id)
    if aircraft:
        return render_template('edit-aircraft-form.html', aircraft=aircraft)
    else:
        return 'Aircraft not found', 404



@app.route('/save_aircraft/<int:id>', methods=['POST'])
def save_aircraft(id):
    model = request.form['aircraft_model']
    capacity = request.form['aircraft_capacity']
    firstclass = request.form['firstclass']

    if update_aircraft(id, model, capacity, firstclass):  # Define this method in database.py to update the aircraft.
        return redirect(url_for('edit_aircrafts'))
    else:
        return 'Error updating aircraft', 500


@app.route("/edit-flights", methods=["GET", "POST"])
def edit_flights():
    return render_template("edit-flights.html")

@app.route("/cancellation-requests", methods=["GET", "POST"])
def cancellation_requests():
    return render_template("cancellation-requests.html")
@app.route('/add_flight_route', methods=["GET", "POST"])
def add_flight_route():
    if not request.form or not all(key in request.form for key in ('miles', 'source', 'destination', 'weekday', 'arrival', 'departure', "aircraft_id")):
        return 'All fields are required', 400
    aircraft_id = request.form['aircraft_id']
    if not aircraft_exists(aircraft_id):
        return 'Invalid aircraft_id', 400
    miles = request.form['miles']
    source = request.form['source']
    destination = request.form['destination']
    weekday = request.form['weekday']
    arrival = request.form['arrival']
    departure = request.form['departure']
    aircraft_id = request.form['aircraft_id']

    if add_flight(miles, source, destination, weekday, arrival, departure, aircraft_id):
        return 'Flight added successfully', 201
    else:
        return 'Internal Server Error', 500




if __name__ == "__main__":
    app.run(debug=True)
