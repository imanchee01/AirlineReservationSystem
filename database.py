import mariadb
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
            SELECT T.ticketId, T.ticket_date, T.ticket_name, T.ticket_flightcode, T.ticket_class, T.ticket_miles, F.flight_destination, F.flight_source, F.flight_arrTime, F.flight_depTime
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
            SELECT T.ticket_date, T.ticket_name, T.ticket_flightcode, T.ticket_class, T.ticket_miles, F.flight_destination, F.flight_source, F.flight_arrTime, F.flight_depTime
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

def create_ticket_cancellation_request(ticket_id, client_id):
    try:
        # Erstellen Sie eine neue Anfrage zur Stornierung des Tickets in der Datenbank.
        new_request = Request(
            request_status="pending",
            request_ticketId=ticket_id,
            request_clientId=client_id,
            request_information="ticket cancellation"
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


if __name__ == "__main__":
    userId = 28  # Replace with an actual user_id you want to test.
    client_data = get_client_data(userId)
    print(client_data)  # This will print the data returned by the function
