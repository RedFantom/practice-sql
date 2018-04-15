"""
Author: RedFantom
License: MIT License
Copyright (C) 2018 RedFantom
"""
from database import open_database, execute_query


"""Open the Database"""
connection = open_database("northwind.db")


"""List all tables"""
query1 = """SELECT name FROM sqlite_master WHERE type='table';"""
tables = execute_query(connection, query1)
for table, in tables:
    print(table, end=", ")
print()


"""Find the category with the most products"""
query2 = """
    SELECT MAX(count), name, description
    FROM (
        SELECT COUNT(*) AS count, CategoryName AS name, Category.Description AS description
        FROM Product
            INNER JOIN Category 
                ON Product.CategoryId = Category.id
        GROUP BY Product.CategoryId
    );
"""
_, name, description = execute_query(connection, query2)[0]
print("The largest category is {} containing {}.".format(name, description))


"""Find the Category with the most customers"""
query3 = """
    SELECT MAX(count), name
    FROM (
        SELECT COUNT(*) AS count, Country AS name
        FROM Customer
        GROUP BY Country
    );
"""
n, country = execute_query(connection, query3)[0]
print("The country with the most customers is {} with {} customers.".format(country, n))


"""Find the most popular shipping method"""
query4 = """
    SELECT MAX(count), name
    FROM (
        SELECT COUNT(*) AS count, Shipper.CompanyName AS name
        FROM 'Order'
            INNER JOIN Shipper
                ON Shipper.Id = 'Order'.ShipVia
        GROUP BY Shipper.Id
    );
"""
_, company = execute_query(connection, query4)[0]
print("The most popular shipping company is {}.".format(company))


"""Determine the customer who ordered the biggest order"""
query5 = """
    SELECT CompanyName FROM 'Customer' WHERE id IN(
    SELECT CustomerId FROM 'Order' WHERE 'Order'.id IN(
        SELECT order_id FROM (SELECT MAX(items), order_id
        FROM (
            SELECT SUM(Quantity) as items, 'Order'.Id as order_id
            FROM OrderDetail
            INNER JOIN 'Order'
                ON 'Order'.Id = OrderDetail.OrderId
        ))
    ));
"""
result, = execute_query(connection, query5)[0]
print("{} made the order with most items.".format(result))
