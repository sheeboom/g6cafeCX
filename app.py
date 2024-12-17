from flask import Flask, jsonify
from flask_cors import CORS
import mysql.connector
from mysql.connector import Error
import logging

app = Flask(__name__)
CORS(app)

# Database configuration
db_config = {
    'host': 'localhost',         # Database host
    'user': 'admin',             # Your MySQL username
    'password': 'MySql.Admin',   # Your MySQL password
    'database': 'g6cafe'         # Your database name
}

# Enable logging
logging.basicConfig(level=logging.DEBUG)

# Root route
@app.route('/')
def home():
    return "Welcome to G6 Cafe API!"  # This will show up when you access http://127.0.0.1:5000/

# Menu route
@app.route('/menu', methods=['GET'])
def menu():
    global connection,cursor
    try:
        connection = mysql.connector.connect(**db_config)
        if connection.is_connected():
            cursor = connection.cursor(dictionary=True)
            query = "SELECT item_id, item_name, category_name, photo, unit_price FROM menu_details"
            cursor.execute(query)
            menu = cursor.fetchall()
            return jsonify(menu)
    except Error as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'connection' in locals() and connection.is_connected():
            connection.close()

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)
