"""
Author: RedFantom
License: MIT License
Copyright (C) 2018 RedFantom
"""
import os


def get_file_path():
    """Return absolute path to the directory this file is in"""
    return os.path.dirname(os.path.abspath(os.path.realpath(__file__)))


def get_databases_path():
    """Return absolute path to databases directory"""
    return os.path.join(get_file_path(), "databases")
