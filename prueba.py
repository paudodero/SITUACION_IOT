from flask import Flask, request
from datetime import datetime
import mysql.connector

app = Flask(__name__)

def createConnection(user_name, database_name, user_password, host, port):
    """Creates a connection to the MySQL database
   
    Parameters
    -----------
        user_name {string} -- The username for the database
        database_name {string} -- The name of the database
        user_password {string} -- The password for the database
        host {string} -- The host of the database
        port {string} -- The port of the database

    Returns
    --------
        tuple -- A tuple containing the connection and the cursor
    """
    cnx = mysql.connector.connect(user=user_name, database=database_name, password=user_password, host=host, port=port)
    cursor = cnx.cursor()
    return (cnx, cursor)

def insert_data(humidity, temperature, date_time):
    """Inserts sensor data into the database"""
    try:
        # Create a connection to the database
        cnx, cursor = createConnection('root', 'IoT_situacion_problema', 'CONTRASEÑA', 'localhost', '3306')

        # Insert the data into the database
        query = ("INSERT INTO new_table (humidity, temperature, date_time) VALUES (%s, %s, %s)")
        data = (humidity, temperature, date_time)

        cursor.execute(query, data)

        # Commit the changes
        cnx.commit()

        print("Data inserted successfully")

    except mysql.connector.Error as err:
        """Handle possible errors"""
        if err.errno == mysql.connector.errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == mysql.connector.errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
    finally:
        """Close the connection"""
        if ('cnx' in locals() or 'cnx' in globals()) and ('cursor' in locals() or 'cursor' in globals()):
            cnx.close()
            cursor.close()

@app.route("/sensor_data", methods=["POST"])
def receive_data():
    """
    This function handles POST requests at '/sensor_data' to process JSON data.
    """
    if request.headers["Content-Type"] == "application/json":
        data = request.json

        humidity = data.get("humidity")
        print("Humidity:", humidity)

        temperature = data.get("temperature")
        print("Temperature:", temperature)

        date_time = data.get("date_time")
        print("Date and Time:", date_time)

        # Call the insert_data() function with the received data
        insert_data(humidity, temperature, date_time)

        return "Data received and inserted into the database", 200
    else:
        return "Invalid Content-Type", 400

if __name__ == "__main__":
    app.run(debug=True, port=5000)
