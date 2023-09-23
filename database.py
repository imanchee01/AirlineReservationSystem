import mariadb
import os
from dotenv import load_dotenv

load_dotenv()

db_config = {
    'user': os.environ.get("DB_ROOTUSER") or 'root',
    'password': os.environ.get("DB_ROOTPASSWORD") or '',
    'host': os.environ.get("DB_HOST") or 'localhost',
    'database': os.environ.get("DB_DATABASE") or 'airline',
    'port': int(os.environ.get("DB_PORT")) or 3308
}


def get_user_role(user_email, user_password):
    connection = None
    try:
        connection = mariadb.connect(**db_config)
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT user_type FROM airline.user WHERE user_email = %s AND user_password = %s",
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
    connection = None
    try:
        connection = mariadb.connect(**db_config)
        cursor = connection.cursor(dictionary=True)
        cursor.execute(
            "INSERT INTO User(user_password, user_type, user_email, user_name) VALUES (%s, 'Client', %s, %s)",
            (password, email, f'{first_name} {last_name}')
        )
        connection.commit()  # Commit changes to database
    except mariadb.Error as e:
        print(f"Error connecting to MariaDB Platform: {e}")
        connection.rollback()
    finally:
        if connection:
            connection.close()


def get_all_emails():
    connection = None
    try:
        connection = mariadb.connect(**db_config)
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT user_email FROM User")
        results = cursor.fetchall()
        return results
    except mariadb.Error as e:
        print(f"Error connecting to MariaDB Platform: {e}")
        return None
    finally:
        if connection:
            connection.close()


def email_list():
    email_list = get_all_emails()
    emails = [entry['user_email'] for entry in email_list]
    return emails


if __name__ == "__main__":
    userId = 28  # Replace with an actual user_id you want to test.
    client_data = get_data_for_client(userId)
    print(client_data)  # This will print the data returned by the function
