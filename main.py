from flask import request, session, redirect, flash, url_for, jsonify, render_template
from database import *
import re
import json
import datetime
from datetime import timedelta


# Custom JSON encoder to handle timedelta objects
class TimedeltaEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, timedelta):
            return str(obj)
        return super().default(obj)


# Custom JSON decoder to handle timedelta strings
def custom_decoder(obj):
    if "__timedelta__" in obj:
        return timedelta(seconds=obj["__timedelta__"])
    return obj


def check_flight_availability(date, flight_schedule):
    input_date = datetime.datetime.strptime(date, "%Y-%m-%d").date()  # Parse the string into a date
    weekday = input_date.strftime("%A").lower()  # Get the full weekday name
    #check for every flight if its on the same weekday as the selected date, if not remove the flight
    valid_flights = []
    for flight_info in flight_schedule:
        if flight_info['flight_weekday'] == weekday:
            valid_flights.append(flight_info)
    return valid_flights

@app.route("/")
def home():
    if "user_name" in session:
        return render_template("user-home.html", user_name=session["user_name"])
    return render_template("no-session.html")


@app.route("/flight-search", methods=["GET", "POST"])
def flight_search():
    departure = request.form["departure"]
    destination = request.form["destination"]
    departure_date = request.form['departure_date']
    return_date = request.form['return_date']

    # cheking if tho chosen airport exists
    if airport_exists(f"{departure}") and airport_exists(f"{destination}"):

        # if it exists get the flight data
        outward_flights_data = check_flight_availability(f'{departure_date}', get_flights(departure, destination))
        return_flights_data = check_flight_availability(f'{return_date}', get_flights(destination, departure))

        # checking if there are any flights available
        if outward_flights_data is None or return_flights_data is None:
            flash('no flights found')
            return redirect(url_for("search_flights"))

        if outward_flights_data == []:
            flash('No flights found on the selected departure date. Please select a different date.')
            return redirect(url_for("search_flights"))

        if return_flights_data == []:
            flash('No flights found on the selected return date. Please select a different date.')
            return redirect(url_for("search_flights"))

        # getting the flight miles to check if flight is short, middle or long distance
        flight_miles = get_all_items_by_name__from_directionary(outward_flights_data, 'flight_miles')
        # getting the prices for the pricecategory the flights are in
        price_category = get_pricecategory(flight_miles)


        prices = []
        for i in price_category:
            prices.append(get_prices(i))

        direction = None

        # adding the prices to the flight information dictionaries
        outward_flights = []
        for i in range(0, len(outward_flights_data)):
            combined_data_out = {}
            combined_data_out.update(outward_flights_data[i])
            combined_data_out.update(prices[i])
            outward_flights.append(combined_data_out)

        return_flights = []
        for i in range(0, len(return_flights_data)):
            combined_data_ret = {}
            combined_data_ret.update(return_flights_data[i])
            combined_data_ret.update(prices[i])
            return_flights.append(combined_data_ret)

        # saving the flight information
        session['outward_flights'] = json.dumps(outward_flights, cls=TimedeltaEncoder)
        session['return_flights'] = json.dumps(return_flights, cls=TimedeltaEncoder)

        return render_template(
            "select-flight.html",
            flights=outward_flights,
            direction=direction,
            departure=departure,
            destination=destination,
            departure_date=departure_date,
            return_date=return_date,
        )

    else:
        flash('The selected airport was not found. Please try again with a different airport.')
        return render_template("flight-search.html")


@app.route("/client-account", methods=["GET"])
def client_account():
    user_id = session["userId"]

    # Rufen Sie die persönlichen Daten des Clients und die Flugdaten aus der Datenbank ab.
    client_data2 = get_client_data(user_id)
    cancellation_requests = [i["request_ticketId"] for i in get_cancellation_requests()]
    flight_history = get_flighthistory(user_id)
    old_flight_history = get_flighthistory_ofOldFlights(user_id)

    return render_template("client-account.html", client_data=client_data2,
                               flight_history=flight_history, cancellation_requests=cancellation_requests, old_flight_history=old_flight_history)



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
        session["userId"] = user.userId
        # Password is correct.
        if user.user_type == "Client":
            # Redirect to the flight search page if the user is a client.
            return redirect(url_for("search_flights"))
        if user.user_type == "Employee":
            # Redirect to the manage requests page if the user is an employee.
            return redirect(url_for("employee_home"))

    # Username or password is incorrect (or we have a user who is not a client nor an employee).
    flash('Invalid login credentials. Please try again or sign up.', 'error')
    return redirect(url_for("login"))


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


@app.route('/search-flights')
def search_flights():
    return render_template("flight-search.html")


@app.route("/select-flight", methods=["GET"])
def select_flight():
    flight_code = request.args.get("flightcode")
    direction = request.args.get("direction")
    departure = request.args.get("departure")
    destination = request.args.get("destination")
    departure_date = request.args.get("departure_date")
    return_date = request.args.get("return_date")
    selected_class = request.args.get("selected_class")
    extra_luggage = request.args.get("extra_luggage")
    # Save departure and return date and number of passengers into session.
    session["departure_date"] = departure_date
    session["return_date"] = return_date

    # loading the flight information
    outward_flights = json.loads(session.get('outward_flights', '[]'), object_hook=custom_decoder)
    return_flights = json.loads(session.get('return_flights', '[]'), object_hook=custom_decoder)


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

    #pass flight data to the template
    return render_template(
        "select-flight.html",
        flights=return_flights if direction == "outward" else outward_flights,
        direction=direction,
        departure=departure,
        destination=destination,
        departure_date=departure_date,
        return_date=return_date,
    )

@app.route("/booking-summary", methods=["GET"])
def booking_summary():
    user_id = session["userId"]
    user_tier = get_user_tier(user_id)
    print(user_tier)
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
        user_tier=user_tier,
        user_id=user_id
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


@app.route("/employee-home", methods=["GET"])
def employee_home():
    return render_template('employee-home.html')


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

'''
@app.route("/add-flight", methods=["GET", "POST"])
def add_flight_route():
    if request.method == 'GET':
        return render_template("edit-flights.html")

    if not request.form or not all(key in request.form for key in (
        "miles",
        "source",
        "destination",
        "weekday",
        "arrival",
        "departure",
        "aircraft"
    )):
        return 'All fields are required', 400

    aircraft_id = request.form['aircraft']
    if not aircraft_exists(aircraft_id):
        return 'Invalid aircraft_id', 400

    miles = request.form['miles']
    source = request.form['source']
    destination = request.form['destination']
    weekday = request.form['weekday']
    arrival = request.form['arrival']
    departure = request.form['departure']
    aircraft_id = request.form['aircraft']

    try:
        add_flight(miles, source, destination, weekday, arrival, departure, aircraft_id)
        flash('Flight created successfully.')
        return redirect(url_for("add_flight_route"))
    except Exception as e:
        app.logger.error("Error! " + str(e))
        flash('Failed to add flight.', 'error')

    return redirect(url_for("add_flight_route"))
'''

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


@app.route("/cancel-ticket", methods=["POST"])
def cancel_ticket():
    client_id = session["userId"]
    data = request.get_json()
    ticket_id = data["ticket_id"]
    if "ticket_id" in data:
        create_ticket_cancellation_request(ticket_id, client_id)
        return jsonify({"message": "Ticket cancellation request submitted successfully"}), 200
    else:
        return jsonify({"message": "Invalid data"}), 400

@app.route('/view-requests', methods=['GET'])
def view_requests():
    requests = get_pending_requests()
    return render_template('cancellation-requests.html', requests=requests)



if __name__ == "__main__":
    app.run(debug=True)