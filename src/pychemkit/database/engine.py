import sqlite3
import os
import sys
import json
import pandas as pd
from sqlalchemy import create_engine

from pychemkit.database import DATABASE_ROOT
from pychemkit.database.queries import PUBCHEM_ELEMENTS_FIELD
from pychemkit.utils.utils import get_query_string
from pychemkit.database.queries import Queries


class DBQuery:

    def __init__(self, db_name):
        self._db = DBConn(db_name)
        self._conn = self._db.conn
        self._cursor = self._db.cursor

    def create_table(self, table_name, dev=True):
        try:
            query_str = f'{Queries.CREATE_TABLE.value} {table_name} {PUBCHEM_ELEMENTS_FIELD}'
            self._cursor.execute(query_str)
            print(f'{table_name} table created')
        except sqlite3.OperationalError as e:
            if dev:
                print(f'{table_name} table already exists')
            else:
                print(e)

    def insert_value(self, table_name, symbol, attr):
        values = get_query_string(symbol, attr)
        query_str = f'{Queries.INSERT_TABLE.value} {table_name} VALUES {values}'
        try:
            self._cursor.execute(query_str)
            self._conn.commit()
            print(query_str)
        except sqlite3.OperationalError as e:
            print(e)

    def get_all_data(self, table_name):
        with self._conn:
            query_str = f'{Queries.SELECT_ALL.value} {table_name}'
            try:
                elements = pd.read_sql_query(query_str, self._conn)
                return elements
            except sqlite3.OperationalError as e:
                print(e)

    def drop_table(self, table_name):
        try:
            query_str = f'{Queries.DROP_TABLE.value} {table_name}'
            self._cursor.execute(query_str)
            print(f'{table_name} table deleted')
        except sqlite3.OperationalError as e:
            print(f'no such table: {table_name}')


class DBConn:

    def __init__(self, db_name):
        self._db = db_name
        self._conn = self._create_connection()
        self._cursor = self._conn.cursor()

    @property
    def cursor(self):
        return self._cursor

    @property
    def conn(self):
        return self._conn

    def _create_connection(self):
        root_path = DATABASE_ROOT
        db_file = f'{self._db}.db'
        db_path = os.path.join(root_path, db_file)
        _connection = sqlite3.connect(db_path)
        return _connection
