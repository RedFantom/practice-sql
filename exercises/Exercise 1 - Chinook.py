"""
Author: RedFantom
License: MIT License
Copyright (C) 2018 RedFantom
"""
import pandas as pd
from database import open_database, print_dataframe, execute_query

connection = open_database("chinook.db")

"""Database Inspection"""
query1 = """SELECT name "Name" FROM sqlite_master WHERE type = 'table';"""
tables = pd.read_sql_query(query1, connection)
print_dataframe("Tables", tables)

"""List all media types"""
query2 = """SELECT Name "Type" FROM media_types;"""
media_types = pd.read_sql_query(query2, connection)
print_dataframe("Media Types", media_types)

"""Count all tracks with each media type"""
for media_type in media_types["Type"]:
    query3 = """
        SELECT COUNT(TrackId) FROM tracks WHERE MediaTypeId IN 
        (SELECT MediaTypeId FROM media_types WHERE media_types.Name = '{}');
    """.format(media_type)
    number, = execute_query(connection, query3)[0]
    print("Tracks, {}: {}".format(media_type, number))
print()

"""Display amount of tracks and name for playlists"""
query4 = """
    SELECT playlists.Name, COUNT(*), SUM(tracks.UnitPrice)
    FROM tracks 
      INNER JOIN playlist_track ON tracks.TrackId = playlist_track.TrackId
      INNER JOIN playlists ON playlist_track.PlaylistId = playlists.PlaylistId
    GROUP BY playlist_track.PlaylistId; 
"""
playlists = execute_query(connection, query4)
for playlist in playlists:
    print("Playlist {} with {} items costs €{:.2f}".format(*playlist))
print()

"""Determine average amount of items per invoice"""
query5 = """
    SELECT AVG(Count) FROM (
      SELECT COUNT(*) AS Count FROM invoice_items GROUP BY InvoiceId);
"""
result, = execute_query(connection, query5)[0]
print("Average number of items per invoice: {:.02f}".format(result))

"""Determine the maximum amount of items on a single invoice"""
query6 = """
    SELECT MAX(Count) FROM (SELECT COUNT(*) AS Count FROM invoice_items GROUP BY InvoiceId);    
"""
result, = execute_query(connection, query6)[0]
print("Maximum amount of items on a single invoice:", result)

"""Determine the Employee with the customer who bought the most items"""
query7 = """
  SELECT employees.FirstName, employees.LastName FROM (
      SELECT MAX(Sum), customers.FirstName, customers.LastName, customers.SupportRepId FROM
        (SELECT SUM(Count) AS Sum, customer FROM
            (SELECT 
                COUNT(*) AS Count, 
                invoices.InvoiceId, 
                invoices.CustomerId AS customer 
            FROM invoices 
                INNER JOIN invoice_items 
                    ON invoices.InvoiceId = invoice_items.InvoiceId 
                    GROUP BY invoices.InvoiceId)
                INNER JOIN customers
            ON customers.CustomerId = customer
        )
        INNER JOIN customers ON customers.CustomerId = customer)
  INNER JOIN employees ON employees.EmployeeId = SupportRepId;
"""
first_name, last_name = execute_query(connection, query7)[0]
print("{} {} is the most successful employee!".format(first_name, last_name))

"""Determine the most successful artist - most tracks"""
query8 = """
  SELECT MAX(Count), name FROM (
    SELECT COUNT(*) AS Count, artists.Name AS name
    FROM tracks
      INNER JOIN albums
        ON tracks.AlbumId = albums.AlbumId
      INNER JOIN artists
        ON albums.ArtistId = artists.ArtistId
    GROUP BY artists.ArtistId
  );
"""
number, name = execute_query(connection, query8)[0]
print("Artist {} has the most songs with {} tracks.".format(name, number))


"""Determine the most successful artist - most sales"""
query9 = """
    SELECT MAX(Count), name FROM (
      SELECT COUNT(*) AS Count, artists.Name AS name
      FROM invoice_items
        INNER JOIN tracks 
          ON invoice_items.TrackId = tracks.TrackId
        INNER JOIN albums
          ON tracks.AlbumId = albums.AlbumId
        INNER JOIN artists
          ON albums.ArtistId = artists.ArtistId 
      GROUP BY artists.Name
    );
"""
number, name = execute_query(connection, query9)[0]
print("Artist {} has the most sales with {} sales".format(name, number))

