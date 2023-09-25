from flask import Flask, jsonify, request
import mysql.connector

app = Flask(__name__)
@app.route('/')
def hello_world():
    return jsonify(message = 'Hello, World!')

db_config = {
    'user': 'root',
    'password': '',
    'host': 'localhost',
    'database': 'airline'
}
connection = mysql.connector.connect(**db_config)
cursor = connection.cursor()

@app.route('/flights', methods = ['GET'])

def get_flights():
    destination = request.args.get('flight_destination')

    if destination:

        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor(dictionary = True)
        cursor.execute("SELECT * FROM airline.flights WHERE flight_destination = %s", (destination,))
        result = cursor.fetchall()
        cursor.close()
        connection.close()
        return jsonify(result)

    else:
        return jsonify({'error': 'Destination parameter is missing'}), 400


if __name__ == '__main__':
    app.run(port = 3008)