import mariadb
import os
from dotenv import load_dotenv
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from werkzeug.security import generate_password_hash, check_password_hash

# We use environment variables to configure the database.
# Values on the right (or ...) are default values.
# Values on the left (... or) are values fetched from a .env file.
# See https://github.com/theskumar/python-dotenv
load_dotenv()
db_config = {
    'user': os.environ.get("DB_ROOTUSER") or 'dbuser',
    'password': os.environ.get("DB_ROOTPASSWORD") or '1111',
    'host': os.environ.get("DB_HOST") or 'localhost',
    'database': os.environ.get("DB_DATABASE") or 'airline',
    'port': os.environ.get("DB_PORT") or 3307
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


def get_db_connection():
    try:
        conn = mariadb.connect(**db_config)
        return conn
    except mariadb.Error as e:
        print(f"Error connecting to MariaDB Platform: {e}")
        return None

# The get_user_role method is only responsible for returning the user role.
# It should not be called before the user has been authenticated (not before a password check).
def get_user_role(user_email, user_password):
    connection = get_db_connection()
    if connection:
        cursor = connection.cursor(dictionary=True)
        try:
            cursor.execute("SELECT user_type FROM airline.user WHERE user_email = %s AND user_password = %s",
                           (user_email, user_password))
            result = cursor.fetchone()
            return result['user_type'] if result else None
        finally:
            connection.close()
    return None


def get_data_for_employee():
    connection = get_db_connection()
    if connection:
        cursor = connection.cursor(dictionary=True)
        try:
            cursor.execute("SELECT * FROM airline.request")
            results = cursor.fetchall()
            return results
        finally:
            connection.close()
    return None


# returns miles and tier after figuring out that user is client
def get_data_for_client(userId):
    def get_data_for_client(userId):
        connection = get_db_connection()
        if connection:
            cursor = connection.cursor(dictionary=True)
            try:
                cursor.execute("""SELECT clientId, miles, tier
                                  FROM client
                                  WHERE clientId = %s;""", (userId, ))
                results = cursor.fetchall()
                return results
            finally:
                connection.close()
        return None


def get_flights_by_destination(destination):
    connection = get_db_connection()
    if connection:
        cursor = connection.cursor(dictionary=True)
        try:
            cursor.execute("SELECT * FROM flights WHERE flight_destination = %s", (destination,))
            results = cursor.fetchall()
            return results
        finally:
            connection.close()
    return None


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

if __name__ == "__main__":
    userId = 28  # Replace with an actual user_id you want to test.
    client_data = get_data_for_client(userId)
    print(client_data)  # This will print the data returned by the function
    print(add_flight(409, "AMS", "ARN", "monday", "09:20:00", "12:20:00", 28))