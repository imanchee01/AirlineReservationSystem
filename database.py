import mariadb




db_config = {
    'user': 'dbuser',
    'password': '1111',
    'host': 'localhost',
    'database': 'airline',
    'port': 3307
}

def get_user_role(username, password):
    try:
        connection = mariadb.connect(**db_config)
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT user_type FROM airline.user WHERE user_name = %s AND user_password = %s", (username, password))
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
    try:
        connection = mariadb.connect(**db_config)
        cursor = connection.cursor(dictionary=True)
        cursor.execute("""SELECT miles, tier
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
    try:
        connection = mariadb.connect(**db_config)
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM flights WHERE destination = %s", (destination,))
        results = cursor.fetchall()
        return results
    except mariadb.Error as e:
        print(f"Error connecting to MariaDB Platform: {e}")
        return None
    finally:
        if connection:
            connection.close()

if __name__ == "__main__":
    userId = 28  # Replace with an actual user_id you want to test.
    client_data = get_data_for_client(userId)
    print(client_data)  # This will print the data returned by the function