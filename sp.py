from flask import Flask, request, render_template, jsonify
from datetime import date, datetime, timedelta
import mysql.connector
from flask import Flask, render_template
import matplotlib.pyplot as plt
from io import BytesIO
import base64

app = Flask(__name__)


def createConnection(user_name, database_name, user_password, host, port):
    cnx = mysql.connector.connect(
        user=user_name, database=database_name, password=user_password, host=host, port=port)
    cursor = cnx.cursor()
    return (cnx, cursor)


@app.route('/', methods=['GET'])
def get_sensor_data():
    # Create a connection to the database
    cnx, cursor = createConnection(
            'sql10652554', 'sql10652554', 'AI989QAABC', 'sql10.freemysqlhosting.net', '3306')

    # Query the database
    query = ("SELECT * FROM dht_data")

    # Execute the query
    cursor.execute(query)

    # Get the data
    data = cursor.fetchall()

    # Close the connection
    cursor.close()
    cnx.close()
    print(data)

        # Obtener los valores de x e y desde los datos
    x = [item[0] for item in data]
    y1 = [item[1] for item in data]
    y2 = [item[2] for item in data]
    y3 = [item[3] for item in data]
    y4 = [item[4] for item in data]


@app.route('/sensor_data', methods=['POST'])
def receive_sensor_data():
    if request.headers['Content-Type'] == 'application/json':
        data = request.json

        humidity = data.get('humidity')
        temperature = data.get('temperature')
        date_time = data.get('date_time')
        mq135Value = data.get('mq135Value')

        print("Received humidity:", humidity)
        print("Received temperature:", temperature)
        print("Received mq135Value:", mq135Value)
        print("recieved date_time:", date_time)

        cnx, cursor = createConnection(
            'sql10652554', 'sql10652554', 'AI989QAABC', 'sql10.freemysqlhosting.net', '3306')

        add_data = (
            "INSERT INTO dht_data (humidity, temperature, mq135Value, date_time) VALUES (%s, %s, %s, %s)")
        cursor.execute(add_data, (humidity, temperature, mq135Value, date_time))
        cnx.commit()
        cursor.close()
        cnx.close()
        print

        return 'Data received successfully.', 200
    else:
        return 'Invalid content type. Expected application/json.', 400

