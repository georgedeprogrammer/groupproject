"""Compatibility import for the customer OOP class.

Importing this module does not prompt for terminal input or write to MySQL.
Use Customers(...).save() from a Flask route or another application module.
"""
from backend.customers import Customers

__all__ = ["Customers"]
