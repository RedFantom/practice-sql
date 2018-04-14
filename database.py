"""
Author: RedFantom
License: MIT License
Copyright (C) 2018 RedFantom
"""
# Standard Library
import os
import sqlite3
# Packages
import pandas as pd
from tabulate import tabulate
# Project Modules
from utils import get_databases_path


def open_database(file: str)->sqlite3.Connection:
    """Return a database connection object for a file"""
    return sqlite3.connect(os.path.join(get_databases_path(), file))


def execute_query(connection: sqlite3.Connection, query: str)->list:
    """Return the results of a query executed on a database"""
    cursor = connection.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    cursor.close()
    return results


def print_dataframe(header: str, df: pd.DataFrame, indent: int=4):
    print(header.upper())
    string = df.to_string()
    lines = string.split("\n")
    indent = " " * indent
    print(indent, lines[0])
    print(indent, "-" * len(lines[0]))
    for line in lines[1:]:
        print(indent, line)
    print()
