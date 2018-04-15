"""
Author: RedFantom
License: MIT License
Copyright (C) 2018 RedFantom
"""
from datetime import datetime
from database import open_database, execute_query


"""Open database"""
connection = open_database("parking.db")
fmt = "%d-%m-%Y"


"""Determine name of the owner of the car that is parked the longest"""
query1 = """
    SELECT name 
    FROM Customer 
    WHERE id IN (
      SELECT owner FROM (
        SELECT MAX(DATE('end') - DATE('start')), owner
        FROM Assignment
          INNER JOIN Vehicle ON Assignment.vehicle_id = Vehicle.id
      )
    );
"""
customer, = execute_query(connection, query1)[0]


"""Determine car type and how long for that customer"""
query2 = """
    SELECT start, Assignment.end, type, spot_id
    FROM Assignment
      INNER JOIN Vehicle ON Assignment.vehicle_id = Vehicle.id
      INNER JOIN Customer ON Vehicle.owner = Customer.id
    WHERE Customer.name = "{}";
""".format(customer)
start, end, car_type, spot_id = execute_query(connection, query2)[0]
duration = (datetime.strptime(end, fmt) - datetime.strptime(start, fmt)).days
print("{} owns a {} and it is staying for {} days in spot {}.".format(customer, car_type, duration, spot_id))
