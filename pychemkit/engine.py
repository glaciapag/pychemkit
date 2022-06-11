import sqlite3
import os

import pandas as pd
from pychemkit.utils import get_query_string
from pychemkit.queries import *


class DBEngine:

    def __init__(self):
        self._conn = self._create_connection()
        self._data = self.get_data()
        self._cursor = self._conn.cursor()

    @property
    def elements(self):
        return self._data

    @staticmethod
    def _create_connection():
        root_path = os.getcwd()
        db_file = 'elements.db'
        db_path = os.path.join(root_path, db_file)
        _connection = sqlite3.connect(db_path)
        return _connection

    def create_table(self, table_name, dev=True):
        try:
            query_str = f'{CREATE_TABLE} {table_name} {ELEMENTS_FIELD}'
            self._cursor.execute(query_str)
            print(f'element table crated')
        except sqlite3.OperationalError:
            if dev:
                self.drop_table('element')
                print(f'element table already exists and dropped for development purposes')
            else:
                print(f'element table already exists')

    def insert_value(self, table_name, symbol, attr):
        values = get_query_string(symbol, attr)
        query_str = f'{INSERT_TABLE} {table_name} VALUES {values}'
        print(query_str)
        self._cursor.execute(query_str)

    def get_data(self, table_name):
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


if __name__ == '__main__':
    pass