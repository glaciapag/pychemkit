import sqlite3
import os
import pandas as pd
from sqlalchemy import create_engine

from pychemkit.database.elements_data import ELEMENTS_DATA
from pychemkit.database import DATABASE_ROOT
from pychemkit.utils.utils import get_query_string, populate_columns
from pychemkit.database.queries import *


class DBEngine:

    def __init__(self, db_name):
        self._db = db_name
        self._conn = self._create_connection()
        self._cursor = self._conn.cursor()

    def _create_connection(self):
        root_path = DATABASE_ROOT
        db_file = f'{self._db}.db'
        db_path = os.path.join(root_path, db_file)
        _connection = sqlite3.connect(db_path)
        return _connection

    def create_table(self, table_name, dev=True):
        try:
            query_str = f'{CREATE_TABLE} {table_name} {ELEMENTS_FIELD}'
            self._cursor.execute(query_str)
            print(f'{table_name} table crated')
        except sqlite3.OperationalError:
            if dev:
                self.drop_table(table_name)
                print(f'{table_name} table already exists and dropped for development purposes')
            else:
                print(f'{table_name} table already exists')

    def insert_value(self, table_name, symbol, attr):
        values = get_query_string(symbol, attr)
        query_str = f'{INSERT_TABLE} {table_name} VALUES {values}'
        print(query_str)
        self._cursor.execute(query_str)

    def get_all_data(self, table_name):
        with self._conn:
            query_str = f'{SELECT_ALL} {table_name}'
            elements = pd.read_sql_query(query_str, self._conn)
            return elements

    def drop_table(self, table_name):
        try:
            query_str = f'{DROP_TABLE}{table_name}'
            self._cursor.execute(query_str)
        except sqlite3.OperationalError:
            print(f'no such table: {table_name}')


def create_and_populate_db(db_name, table_name, data):
    db = DBEngine(db_name)
    db.create_table(table_name)
    populate_columns(db, table_name, data)
    return db


def get_elements_data(db_name, table_name):
    db = DBEngine(db_name)
    data = db.get_all_data(table_name)
    return data


ELEMENTS_DATA = get_elements_data('ELEMENTSDB', 'elements')

if __name__ == '__main__':
    db = DBEngine('ELEMENTSDB')
