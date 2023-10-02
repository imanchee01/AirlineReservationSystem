import mariadb
import os
from dotenv import load_dotenv
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from werkzeug.security import generate_password_hash, check_password_hash

load_dotenv()

db_config = {
    'user': 'root',
    'password': '',
    'host': 'localhost',
    'database': 'airline',
    'port': 3306
}


app = Flask(__name__)

# Set the secret key to some random bytes. Keep this really secret!
app.secret_key = b"cvobidrnsuerbsifurf34ads"


class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)

app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+mysqlconnector://" + db_config['user'] + ":" + db_config[
    "password"] + "@" + db_config["host"] + ":" + str(db_config["port"]) + "/" + db_config["database"]

db.init_app(app)


class Request(db.Model):
    __tablename__ = "request"

    # Fügen Sie Ihre Modellspalten hier hinzu
    request_id = db.Column(db.Integer, primary_key=True)
    request_status = db.Column(db.String(50), nullable=False)
    request_ticketId = db.Column(db.Integer, nullable=False)
    request_clientId = db.Column(db.Integer, nullable=False)
    request_information = db.Column(db.String(255), nullable=False)

    # Weitere Modellspalten hinzufügen, wenn nötig

    def __init__(self, request_status, request_ticketId, request_clientId, request_information):
        self.request_status = request_status
        self.request_ticketId = request_ticketId
        self.request_clientId = request_clientId
        self.request_information = request_information


class User(db.Model):
    __tablename__ = "user"

    userId = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(80), unique=True, nullable=False)
    user_email = db.Column(db.String(120), unique=True, nullable=False)
    user_password = db.Column(db.String(256), nullable=False)
    user_type = db.Column(db.String(8), nullable=False)

    def __init__(self, user_name, user_email, user_password, user_type):
        self.user_name = user_name
        self.user_email = user_email
        self.user_type = user_type
        self.set_password(user_password)

    def set_password(self, user_password):
        self.user_password = generate_password_hash(user_password)

    def check_password(self, user_password):
        return check_password_hash(self.user_password, user_password)

    def __repr__(self):
        return f"<User {self.user_name}>"


class Flight(db.Model):
    __tablename__ = "flights"

    flightcode = db.Column(db.Integer, primary_key=True, autoincrement=True)
    flight_miles = db.Column(db.Float, unique=False, nullable=False)
    flight_source = db.Column(db.String(4), unique=True, nullable=False)
    flight_destination = db.Column(db.String(4), unique=True, nullable=False)
    flight_weekday = db.Column(db.String(10), nullable=False)
    flight_arrTime = db.Column(db.String(10), nullable=False)
    flight_depTime = db.Column(db.String(10), nullable=False)
    flight_aircraftId = db.Column(db.Integer, db.ForeignKey('aircraft.aircraftId'),
                                  nullable=False)

    def __init__(self,
                 flight_miles,
                 flight_source,
                 flight_destination,
                 flight_weekday,
                 flight_arrTime,
                 flight_depTime,
                 flight_aircraftId,
                 ):
        self.flight_miles = flight_miles
        self.flight_source = flight_source
        self.flight_destination = flight_destination
        self.flight_weekday = flight_weekday
        self.flight_arrTime = flight_arrTime
        self.flight_depTime = flight_depTime
        self.flight_aircraftId = flight_aircraftId

    def __repr__(self):
        return f"<Flight {self.flightcode}>"


class Ticket(db.Model):
    __tablename__ = "tickets"

    ticket_name = db.Column(db.String(100), unique=True, nullable=False)
    ticket_date = db.Column(db.Date, unique=False, nullable=False)
    ticket_miles = db.Column(db.Float, nullable=False)
    ticketId = db.Column(db.Integer, primary_key=True)
    ticket_purchaseDate = db.Column(db.Date, nullable=False)
    ticket_userId = db.Column(db.Integer, db.ForeignKey('user.userId'), nullable=False)
    ticket_flightcode = db.Column(db.Integer, db.ForeignKey('flights.flightcode'), nullable=False)
    ticket_class = db.Column(db.String(10), nullable=False)

    def __init__(self,
                 ticket_name,
                 ticket_date,
                 ticket_miles,
                 ticket_purchaseDate,
                 ticket_userId,
                 ticket_flightcode,
                 ticket_class
                 ):
        self.ticket_name = ticket_name
        self.ticket_date = ticket_date
        self.ticket_miles = ticket_miles
        self.ticket_purchaseDate = ticket_purchaseDate
        self.ticket_userId = ticket_userId
        self.ticket_flightcode = ticket_flightcode
        self.ticket_class = ticket_class

    def __repr__(self):
        return f"<Ticket {self.ticketId}>"
    def add_ticket(ticket_name, ticket_date, ticket_miles, ticket_purchaseDate, ticket_userId, ticket_flightcode,
                   ticket_class):
        # add new ticket to the database
        new_ticket = Ticket(
            ticket_name=ticket_name,
            ticket_date=ticket_date,
            ticket_miles=ticket_miles,
            ticket_purchaseDate=ticket_purchaseDate,
            ticket_userId=ticket_userId,
            ticket_flightcode=ticket_flightcode,
            ticket_class=ticket_class
        )
        db.session.add(new_ticket)
        db.session.commit()


def get_db_connection():
    try:
        conn = mariadb.connect(**db_config)
        return conn
    except mariadb.Error as e:
        print(f"Error connecting to MariaDB Platform: {e}")
        return None


def get_user(user_email):
    return User.query.filter_by(user_email=user_email).first()



# The get_user_role method is only responsible for returning the user role.
# It should not be called before the user has been authenticated (not before a password check).
def get_user_role(user_email, user_password):
    connection = None
    try:
        connection = mariadb.connect(**db_config)
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT user_type FROM airline.user WHERE user_email = %s",
                       (user_email, user_password))
        result = cursor.fetchone()

        if result:
            return result['user_type']

        else:
            return None

    except mariadb.Error as e:
        print(f"Error connecting to MariaDB Platform: {e}")
        return None
    finally:
        if connection:
            connection.close()


def get_data_for_employee():
    connection = None
    try:
        connection = mariadb.connect(**db_config)
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM airline.request")
        results = cursor.fetchall()
        return results
    except mariadb.Error as e:
        print(f"Error connecting to MariaDB Platform: {e}")
        return None
    finally:
        if connection:
            connection.close()


# returns miles and tier after figuring out that user is client
def get_data_for_client(userId):
    connection = None
    try:
        connection = mariadb.connect(**db_config)
        cursor = connection.cursor(dictionary=True)
        cursor.execute("""SELECT clientId, miles, tier
                          FROM client
                          WHERE clientId = %s;""", (userId,))

        results = cursor.fetchall()
        return results
    except mariadb.Error as e:
        print(f"Error connecting to MariaDB Platform: {e}")
        return None
    finally:
        if connection:
            connection.close()


def get_flights_by_destination(destination):
    connection = None
    try:
        connection = mariadb.connect(**db_config)
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM flights WHERE flight_destination = %s", (destination,))
        results = cursor.fetchall()
        return results
    except mariadb.Error as e:
        print(f"Error connecting to MariaDB Platform: {e}")
        return None
    finally:
        if connection:
            connection.close()


def save_signup_information(first_name, last_name, email, password):
    # Create a new user and add it to the database
    new_user = User(user_name=f'{first_name} {last_name}', user_email=email, user_password=password, user_type="Client")
    db.session.add(new_user)
    db.session.commit()

    # connection = None
    # try:
    #     connection = mariadb.connect(**db_config)
    #     cursor = connection.cursor(dictionary=True)
    #     cursor.execute(
    #         "INSERT INTO User(user_password, user_type, user_email, user_name) VALUES (%s, 'Client', %s, %s)",
    #         (password, email, f'{first_name} {last_name}')
    #     )
    #     connection.commit()  # Commit changes to database
    # except mariadb.Error as e:
    #     print(f"Error connecting to MariaDB Platform: {e}")
    #     connection.rollback()
    # finally:
    #     if connection:
    #         connection.close()


def user_with_email_exists(email):
    existing_email = User.query.filter_by(user_email=email).first()
    if existing_email:
        return True
    return False


def add_flight(miles, source, destination, weekday, arrival, departure, aircraft_id):
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor()
        query = """INSERT INTO flights (flight_miles, flight_source, flight_destination, flight_weekday, flight_arrTime, flight_depTime, flight_aircraftId) 
                   VALUES (%s, %s, %s, %s, %s, %s, %s)"""
        params = (miles, source, destination, weekday, arrival, departure, aircraft_id)
        try:

            cursor.execute(query, params)
            conn.commit()
        except mariadb.Error as e:
            print(f"Error: {e}")
            return False
        finally:
            cursor.close()
            conn.close()
    return True


def aircraft_exists(aircraft_id):
    conn = get_db_connection()
    if not conn:
        return False

    try:
        cursor = conn.cursor()
        cursor.execute("SELECT 1 FROM aircraft WHERE aircraftId = %s", (aircraft_id,))
        return bool(cursor.fetchone())
    except mariadb.Error as e:
        print(f"Error: {e}")
        return False
    finally:
        conn.close()


def get_all_aircrafts():
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("SELECT * FROM aircraft")
            return cursor.fetchall()
        finally:
            conn.close()


def get_aircraft_by_id(id):
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("SELECT * FROM aircraft WHERE aircraftId = %s", (id,))
            return cursor.fetchone()
        finally:
            conn.close()


def update_aircraft(id, model, capacity, firstclass):
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute("""UPDATE aircraft SET 
                              aircraft_model = %s,
                              aircraft_capacity = %s,
                              aircraft_firstclass = %s 
                              WHERE aircraftId = %s""", (model, capacity, firstclass, id))
            conn.commit()
            return True
        except mariadb.Error as e:
            print(f"Error: {e}")
            return False
        finally:
            conn.close()


def get_client_data(userId):
    connection = None
    try:
        connection = mariadb.connect(**db_config)
        cursor = connection.cursor(dictionary=True)
        cursor.execute("""SELECT user_name, user_email, miles, tier 
                          FROM client
                          JOIN user on clientId = userId
                          WHERE clientId = %s;""", (userId,))
        results = cursor.fetchall()
        return results
    except mariadb.Error as e:
        print(f"Error connecting to MariaDB Platform: {e}")
        return None
    finally:
        if connection:
            connection.close()


def get_flighthistory(userId):
    connection = None
    try:
        connection = mariadb.connect(**db_config)
        cursor = connection.cursor(dictionary=True)
        cursor.execute("""
            SELECT T.ticketId, T.ticket_date, T.ticket_name, T.ticket_flightcode, T.ticket_class, T.ticket_miles, T.offer, 
                    F.flight_destination, F.flight_source, F.flight_arrTime, F.flight_depTime
            FROM tickets T
            LEFT JOIN flights F ON T.ticket_flightcode = F.flightcode
            WHERE T.ticket_date>= CURDATE()  and ticket_userId = %s
            ORDER BY T.ticket_date
        """, (userId,))
        results = cursor.fetchall()
        return results
    except mariadb.Error as e:
        print(f"Error connecting to MariaDB Platform: {e}")
        return None
    finally:
        if connection:
            connection.close()


def get_flighthistory_ofOldFlights(userId):
    connection = None
    try:
        connection = mariadb.connect(**db_config)
        cursor = connection.cursor(dictionary=True)
        cursor.execute("""
            SELECT T.ticket_date, T.ticket_name, T.ticket_flightcode, T.ticket_class, T.ticket_miles, 
                F.flight_destination, F.flight_source, F.flight_arrTime, F.flight_depTime
            FROM tickets T
            LEFT JOIN flights F ON T.ticket_flightcode = F.flightcode
            WHERE T.ticket_date< CURDATE()  and ticket_userId = %s
            ORDER BY T.ticket_date
        """, (userId,))
        results = cursor.fetchall()
        return results
    except mariadb.Error as e:
        print(f"Error connecting to MariaDB Platform: {e}")
        return None
    finally:
        if connection:
            connection.close()


def create_ticket_cancellation_request(ticket_id, client_id, cancellation_reason):
    try:
        # Erstellen Sie eine neue Anfrage zur Stornierung des Tickets in der Datenbank.
        new_request = Request(
            request_status="pending",
            request_ticketId=ticket_id,
            request_clientId=client_id,
            request_information=cancellation_reason
        )
        print(new_request)

        # Fügen Sie die neue Anfrage zur Datenbank hinzu und commiten Sie die Änderungen.
        db.session.add(new_request)
        db.session.commit()

        return True  # Erfolgreich erstellt
    except Exception as e:
        # Behandeln Sie Fehler, wenn die Anfrage nicht erstellt werden kann.
        print("Error creating cancellation request:", str(e))
        db.session.rollback()
        return False  # Fehler bei der Erstellung


def get_cancellation_requests():
    connection = None
    try:
        connection = mariadb.connect(**db_config)
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT request_ticketId FROM request")
        results = cursor.fetchall()
        return results
    except mariadb.Error as e:
        print(f"Error connecting to MariaDB Platform: {e}")
        return None
    finally:
        if connection:
            connection.close()


def all_airports():
    connection = None
    try:
        connection = mariadb.connect(**db_config)
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT airportId FROM airport")
        results = cursor.fetchall()
        return results
    except mariadb.Error as e:
        print(f"Error connecting to MariaDB Platform: {e}")
        return None
    finally:
        if connection:
            connection.close()


def airport_exists(airport):
    airports = [entry['airportId'] for entry in all_airports()]
    if airport in airports:
        return True
    return False


def get_pricecategory(miles):
    list = []
    for i in miles:
        if i > 450:
            list.append('short distance')
        elif i < 450 and i > 800:
            list.append('middle distance')
        else:
            list.append('long distance')

    return list


def get_prices(pricecategory):
    connection = None
    try:
        connection = mariadb.connect(**db_config)
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM ticketprice WHERE pricecategory =%s",
                       (pricecategory,))
        results = cursor.fetchone()
        return results
    except mariadb.Error as e:
        print(f"Error connecting to MariaDB Platform: {e}")
        return None
    finally:
        if connection:
            connection.close()


def get_flights(source, destination):
    connection = None
    try:
        connection = mariadb.connect(**db_config)
        cursor = connection.cursor(dictionary=True)
        cursor.execute(
            "SELECT flightcode, flight_miles, flight_source, flight_destination, flight_weekday, flight_arrTime, flight_depTime, flight_aircraftId, aircraft_firstclass  FROM flights JOIN aircraft ON flight_aircraftId = aircraftId WHERE flight_source = %s AND flight_destination = %s",
            (source, destination))
        results = cursor.fetchall()
        return results
    except mariadb.Error as e:
        print(f"Error connecting to MariaDB Platform: {e}")
        return None
    finally:
        if connection:
            connection.close()


def get_all_items_by_name__from_directionary(directionary, item_name):
    list = []

    for item in directionary:
        if item_name in item:
            list.append(item[item_name])

    return list


def get_pending_requests():
    conn = get_db_connection()
    if not conn:
        return None
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT * FROM request WHERE request_status='pending'
    """)

    requests = cursor.fetchall()
    conn.close()

    return requests


def get_ticket_cancellation_requests():
    try:
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        cursor.execute("""
            SELECT U.user_name, T.ticketId, T.ticket_date, F.flightcode, R.requestId, R.request_information
            FROM request R
            JOIN tickets T ON R.request_ticketId = T.ticketId
            JOIN flights F ON T.ticket_flightcode = F.flightcode
            JOIN client C ON R.request_clientId = C.clientId
            JOIN user U ON C.clientId = U.userId
            WHERE R.request_status = 'pending'
        """)
        requests = cursor.fetchall()
        return requests
    except Exception as e:
        print(f"Error: {e}")
        return None
    finally:
        if connection:
            connection.close()


def update_request_status_and_delete_ticket(request_id, status):
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        print(f"Trying to update request_status to: {status}")
        cursor.execute("""
            UPDATE request 
            SET request_status = %s 
            WHERE requestId = %s;
        """, (status, request_id))

        if status == 'accepted':
            cursor.execute("""
                DELETE T FROM tickets T
                JOIN request R ON T.ticketId = R.request_ticketId
                WHERE R.requestId = %s;
            """, (request_id,))

        connection.commit()
        return True
    except Exception as e:
        print(f"Error: {e}")
        return False
    finally:
        if connection:
            connection.close()


def delete_request(request_id):
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute("""
            DELETE FROM request 
            WHERE requestId = %s;
        """, (request_id,))
        connection.commit()
        return True
    except Exception as e:
        print(f"Error: {e}")
        return False
    finally:
        if connection:
            connection.close()

def update_request_status(request_id, status):
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute("""
            UPDATE request 
            SET request_status = %s 
            WHERE requestId = %s;
        """, (status, request_id))

        connection.commit()
        return True
    except Exception as e:
        print(f"Error: {e}")
        return False
    finally:
        if connection:
            connection.close()


def get_user_name(user_Id):
    connection = None
    try:
        connection = mariadb.connect(**db_config)
        cursor = connection.cursor(dictionary=True)
        cursor.execute(" SELECT user_name FROM user WHERE userId= %s", (user_Id))
        results = cursor.fetchall()
        return results
    except mariadb.Error as e:
        print(f"Error connecting to MariaDB Platform: {e}")
        return None
    finally:
        if connection:
            connection.close()


def get_user_tier(user_id):
    connection = None
    try:
        connection = mariadb.connect(**db_config)
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT tier FROM client WHERE clientId = %s", (user_id,))
        result = cursor.fetchone()
        if result:
            return result['tier']
        else:
            return None
    except mariadb.Error as e:
        print(f"Error connecting to MariaDB Platform: {e}")
        return None
    finally:
        if connection:
            connection.close()


def update_offers(ticket_flightcode, ticket_class, offer):
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        query = """
                    UPDATE tickets 
                    SET offer = %s 
                    WHERE ticket_flightcode = %s AND ticket_class = %s
                """
        print(f"Executing query: {query} with parameters: {offer}, {ticket_flightcode}, {ticket_class}")

        cursor.execute(query, (offer, ticket_flightcode, ticket_class))
        connection.commit()
        return True
    except Exception as e:
        print(f"Error: {e}")
        return False
    finally:
        if connection:
            connection.close()


def get_flight_codes():
    try:
        connection = get_db_connection()  # assuming you have a function to get a db connection
        cursor = connection.cursor()
        cursor.execute("SELECT flightcode FROM flights")
        results = cursor.fetchall()
        print(results)
        flight_codes = [row[0] for row in results]
        print(flight_codes)
        return flight_codes
    except Exception as e:
        print(f"Error: {e}")
        return []
    finally:
        if connection:
            connection.close()


def add_aircraft(model, capacity, firstclass):
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor()
        query = """INSERT INTO aircraft (aircraft_model, aircraft_capacity, aircraft_firstclass) 
                   VALUES (%s, %s, %s)"""
        params = (model, capacity, firstclass)
        try:
            cursor.execute(query, params)
            #print(cursor.execute(query, params))
            conn.commit()
        except mariadb.Error as e:
            print(f"Error: {e}")
            return False
        finally:
            cursor.close()
            conn.close()
    return True


def delete_aircraft_by_id(id):
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor()
        query = """DELETE FROM aircraft WHERE aircraftId = %s"""
        try:
            cursor.execute(query, (id,))
            conn.commit()
            return True
        except mariadb.Error as e:
            print(f"Error: {e}")
        finally:
            cursor.close()
            conn.close()
    return False


def get_all_flights():
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("SELECT * FROM flights")
            flights = cursor.fetchall()
            return flights
        except Exception as e:
            print(f"Error: {e}")
        finally:
            cursor.close()
            conn.close()


def delete_flight_by_id(id):
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor()
        query = """DELETE FROM flights WHERE flightcode = %s"""
        try:
            cursor.execute(query, (id,))
            conn.commit()
            return True
        except mariadb.Error as e:
            print(f"Error: {e}")
        finally:
            cursor.close()
            conn.close()
    return False


def get_flight_by_id(id):
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("SELECT * FROM flights WHERE flightcode = %s", (id,))
            return cursor.fetchone()
        finally:
            conn.close()


def update_flight(id, miles, source, destination, weekday, arrival, departure, aircraft_id):
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute("""
                UPDATE flights SET
                flight_miles = %s,
                flight_source = %s,
                flight_destination = %s,
                flight_weekday = %s,
                flight_arrTime = %s,
                flight_depTime = %s,
                flight_aircraftId = %s
                WHERE flightcode = %s
            """, (miles, source, destination, weekday, arrival, departure, aircraft_id, id))
            conn.commit()
            return True
        except mariadb.Error as e:
            print(f"Error: {e}")
            return False
        finally:
            conn.close()


def get_checkinstatus():
    connection = None
    try:
        connection = mariadb.connect(**db_config)
        cursor = connection.cursor(dictionary=True)
        cursor.execute(" SELECT ticketId, checkinstatus FROM checkin_status ",)
        results = cursor.fetchall()
        return results
    except mariadb.Error as e:
        print(f"Error connecting to MariaDB Platform: {e}")
        return None
    finally:
        if connection:
            connection.close()


def create_checkIn(ticket_id):
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute("""
            UPDATE checkin_status 
            SET checkinstatus = 'checkedin'
            WHERE ticketId = %s;
        """, (ticket_id,))
        connection.commit()
        return True
    except Exception as e:
        print(f"Error: {e}")
        return False
    finally:
        if connection:
            connection.close()


def get_remaining_capacity(flightcode, flightdate):
    connection = None
    try:
        connection = mariadb.connect(**db_config)
        cursor = connection.cursor(dictionary=True)

        # Execute the SQL function to get remaining capacity
        cursor.execute("SELECT GetRemainingCapacity(%(flightcode)s, %(flightdate)s)",
                       {'flightcode': flightcode, 'flightdate': flightdate})

        # Retrieve the result from the stored procedure
        result = cursor.fetchone()
        remaining_capacity = result[next(iter(result))]

        return remaining_capacity


    except mariadb.Error as e:
        print(f"Error connecting to MariaDB Platform: {e}")
        return None
    finally:
        if connection:
            connection.close()



if __name__ == "__main__":
    userId = 28  # Replace with an actual user_id you want to test.
    client_data = get_client_data(userId)
    print(client_data)  # This will print the data returned by the function
    print(update_offers(1, "economy", "free meal"))