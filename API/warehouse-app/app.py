from flask import Flask, request, jsonify
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)

# MySQL Database Connection
def create_connection():
    return mysql.connector.connect(
        host='localhost',
        user='root',
        password='your_mysql_password',  # Replace with your MySQL password
        database='warehouse'
    )

# Route to store RFID data
@app.route('/api/rfid', methods=['POST'])
def store_rfid():
    try:
        data = request.get_json()  # Get JSON data from the request
        uid = data['uid']  # Extract UID from the JSON data
        connection = create_connection()  # Establish a database connection
        cursor = connection.cursor()  # Create a cursor object to interact with the database
        sql = 'INSERT INTO tracking (uid, timestamp) VALUES (%s, NOW())'
        cursor.execute(sql, (uid,))  # Execute the SQL query
        connection.commit()  # Commit the transaction
        cursor.close()  # Close the cursor
        connection.close()  # Close the database connection
        return 'RFID data stored successfully', 200
    except Error as e:
        print(e)  # Print any database error
        return 'Failed to store RFID data', 500

# Route to retrieve stored RFID data
@app.route('/api/tracking', methods=['GET'])
def get_tracking():
    try:
        connection = create_connection()  # Establish a database connection
        cursor = connection.cursor(dictionary=True)  # Create a cursor with dictionary output
        sql = 'SELECT * FROM tracking ORDER BY timestamp DESC'
        cursor.execute(sql)  # Execute the SQL query
        results = cursor.fetchall()  # Fetch all results
        cursor.close()  # Close the cursor
        connection.close()  # Close the database connection
        return jsonify(results), 200  # Return the results as JSON
    except Error as e:
        print(e)  # Print any database error
        return 'Failed to retrieve data', 500

if __name__ == '__main__':
    app.run(port=3000)  # Run the Flask application on port 3000
