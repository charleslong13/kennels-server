import sqlite3
import json
from models import Customer

CUSTOMERS = [
    {
      "id": 3,
      "animalId": 3,
      "userId": 16
    },
    {
      "id": 4,
      "animalId": 4,
      "userId": 17
    },
    {
      "id": 5,
      "animalId": 5,
      "userId": 18
    },
    {
      "id": 6,
      "animalId": 5,
      "userId": 19
    },
    {
      "animalId": 6,
      "userId": 20,
      "id": 7
    },
    {
      "animalId": 7,
      "userId": 18,
      "id": 8
    },
    {
      "animalId": 8,
      "userId": 17,
      "id": 9
    },
    {
      "animalId": 10,
      "userId": 16,
      "id": 10
    },
    {
      "animalId": 10,
      "userId": 15,
      "id": 11
    },
    {
      "userId": 15,
      "animalId": 1,
      "id": 12
    },
    {
      "userId": 16,
      "animalId": 3,
      "id": 14
    },
    {
      "userId": 24,
      "animalId": 4,
      "id": 15
    },
    {
      "userId": 19,
      "animalId": 1,
      "id": 16
    },
    {
      "userId": 16,
      "animalId": 9,
      "id": 17
    },
    {
      "userId": 18,
      "animalId": 6,
      "id": 18
    },
    {
      "userId": 24,
      "animalId": 7,
      "id": 19
    },
    {
      "userId": 24,
      "animalId": 9,
      "id": 20
    },
    {
      "animalId": 8,
      "userId": 16,
      "id": 23
    }
  ]

def get_all_customers():
    # Open a connection to the database
    with sqlite3.connect("./kennel.sqlite3") as conn:

        # Just use these. It's a Black Box.
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Write the SQL query to get the information you want
        db_cursor.execute("""
        SELECT
            a.id,
            a.name,
            a.address,
            a.email,
            a.password
            
        FROM customer a
        """)

        # Initialize an empty list to hold all animal representations
        customers = []

        # Convert rows of data into a Python list
        dataset = db_cursor.fetchall()

        # Iterate list of data returned from database
        for row in dataset:

            # Create an animal instance from the current row.
            # Note that the database fields are specified in
            # exact order of the parameters defined in the
            # Animal class above.
            customer = Customer(row['id'], row['name'], row['address'], row['email'], row['password'])
                            

            customers.append(customer.__dict__)

    # Use `json` package to properly serialize list as JSON
    return json.dumps(customers)

def get_single_customer(id):
    with sqlite3.connect("./kennel.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Use a ? parameter to inject a variable's value
        # into the SQL statement.
        db_cursor.execute("""
        SELECT
            a.id,
            a.name,
            a.address,
            a.email,
            a.password
        FROM customer a
        WHERE a.id = ?
        """, ( id, ))

        # Load the single result into memory
        data = db_cursor.fetchone()

        # Create an animal instance from the current row
        customer = Customer(data['id'], data['name'], data['address'], data['email'], data['password'])

        return json.dumps(customer.__dict__)

def create_customer(customer):
    # Get the id value of the last animal in the list
    max_id = CUSTOMERS[-1]["id"]

    # Add 1 to whatever that number is
    new_id = max_id + 1

    # Add an `id` property to the animal dictionary
    customer["id"] = new_id

    # Add the animal dictionary to the list
    CUSTOMERS.append(customer)

    # Return the dictionary with `id` property added
    return customer

def delete_customer(id):
    # Initial -1 value for animal index, in case one isn't found
    customer_index = -1

    # Iterate the ANIMALS list, but use enumerate() so that you
    # can access the index value of each item
    for index, customer in enumerate(CUSTOMERS):
        if customer["id"] == id:
            # Found the animal. Store the current index.
            customer_index = index

    # If the animal was found, use pop(int) to remove it from list
    if customer_index >= 0:
        CUSTOMERS.pop(customer_index)

def update_customer(id, new_customer):
    # Iterate the ANIMALS list, but use enumerate() so that
    # you can access the index value of each item.
    for index, customer in enumerate(CUSTOMERS):
        if customer["id"] == id:
            # Found the animal. Update the value.
            CUSTOMERS[index] = new_customer
            break

def get_customers_by_email(email):

    with sqlite3.connect("./kennel.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Write the SQL query to get the information you want
        db_cursor.execute("""
        select *
        from Customer c
        WHERE c.email = ?
        """, ( email, ))

        customers = []
        dataset = db_cursor.fetchall()

        for row in dataset:
            customer = Customer(row['id'], row['name'], row['address'], row['email'] , row['password'])
            customers.append(customer.__dict__)

    return json.dumps(customers)