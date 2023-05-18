from flask import Flask, request, jsonify
import mysql.connector

# Establish connection to the MySQL database
conn = mysql.connector.connect(
    host="your_host",
    user="your_username",
    password="your_password",
    database="your_database"
)

# Create a Flask application
app = Flask(__name__)

# Define routes and their corresponding actions
@app.route('/add_item', methods=['POST'])
def add_item():
    data = request.get_json()
    cursor = conn.cursor()
    insert_query = """
        INSERT INTO items (listTage, itemName, addedDate, expierdDate)
        VALUES (%s, %s, %s, %s)
    """
    values = (data['listTage'], data['itemName'], data['addedDate'], data['expierdDate'])
    cursor.execute(insert_query, values)
    conn.commit()
    cursor.close()
    return jsonify({'message': 'Item added successfully'})

@app.route('/remove_item', methods=['POST'])
def remove_item():
    data = request.get_json()
    cursor = conn.cursor()
    delete_query = "DELETE FROM items WHERE id = %s"
    cursor.execute(delete_query, (data['id'],))
    conn.commit()
    cursor.close()
    return jsonify({'message': 'Item removed successfully'})

@app.route('/update_item', methods=['POST'])
def update_item():
    data = request.get_json()
    cursor = conn.cursor()
    update_query = """
        UPDATE items
        SET listTage = %s, itemName = %s, addedDate = %s, expierdDate = %s
        WHERE id = %s
    """
    values = (data['listTage'], data['itemName'], data['addedDate'], data['expierdDate'], data['id'])
    cursor.execute(update_query, values)
    conn.commit()
    cursor.close()
    return jsonify({'message': 'Item updated successfully'})

# Run the Flask application
if __name__ == '__main__':
    app.run()

# Close the database connection when the application shuts down
conn.close()
