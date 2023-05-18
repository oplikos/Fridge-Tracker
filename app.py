from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import mysql.connector
from dotenv import load_dotenv
import os

# load credentials for connection to database
load_dotenv("../credentials.env")
db_config = {
    "host" : os.environ['MYSQL_HOST'],
    "user" : os.environ['MYSQL_USER'],
    "password" : os.environ['MYSQL_PASSWORD'],
    "database" : os.environ['MYSQL_DATABASE']
}

# Establish connection to the MySQL database
conn = mysql.connector.connect(**db_config)

# Create a FastAPI application
app = FastAPI()

# Define a Pydantic model for the item data
class Item(BaseModel):
    listTage: str
    itemName: str
    addedDate: str
    expierdDate: str

# Add item to the database
@app.post('/add_item')
def add_item(item: Item):
    cursor = conn.cursor()
    insert_query = """
        INSERT INTO items (listTage, itemName, addedDate, expierdDate)
        VALUES (%s, %s, %s, %s)
    """
    values = (item.listTage, item.itemName, item.addedDate, item.expierdDate)
    cursor.execute(insert_query, values)
    conn.commit()
    cursor.close()
    return {'message': 'Item added successfully'}

# Remove item from the database
@app.post('/remove_item')
def remove_item(item_id: int):
    cursor = conn.cursor()
    delete_query = "DELETE FROM items WHERE id = %s"
    cursor.execute(delete_query, (item_id,))
    if cursor.rowcount == 0:
        raise HTTPException(status_code=404, detail='Item not found')
    conn.commit()
    cursor.close()
    return {'message': 'Item removed successfully'}

# Update item in the database
@app.put('/update_item/{item_id}')
def update_item(item_id: int, item: Item):
    cursor = conn.cursor()
    update_query = """
        UPDATE items
        SET listTage = %s, itemName = %s, addedDate = %s, expierdDate = %s
        WHERE id = %s
    """
    values = (item.listTage, item.itemName, item.addedDate, item.expierdDate, item_id)
    cursor.execute(update_query, values)
    if cursor.rowcount == 0:
        raise HTTPException(status_code=404, detail='Item not found')
    conn.commit()
    cursor.close()
    return {'message': 'Item updated successfully'}

# Run the FastAPI application
if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=8000)

# Close the database connection when the application shuts down
conn.close()
