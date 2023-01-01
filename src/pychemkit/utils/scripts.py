import json
import os

from pychemkit.engine.conn import DBQuery
from pychemkit._resources.pubchem_data import ELEMENTS_DATA


def create_and_populate_db(db_name, table_name, data):
    db = DBQuery(db_name)
    db.create_table(table_name)
    populate_columns(db, table_name, data)
    return db


def populate_columns(db_instance, table, data):
    assert isinstance(data, dict)
    for symb, attr in data.items():
        db_instance.insert_value(table, symb, attr)


def get_elements_data(db_instance, table_name):
    data = db_instance.get_all_data(table_name)
    return data


def transform_pubchem_data(json_filepath):

    elems_map = {}

    with open(json_filepath, 'r') as js:
        json_obj = json.load(js)
        cols = json_obj['Table']['Columns']['Column']
        cols = cols + ['num_neutrons', 'num_protons', 'num_electrons']
        rows = json_obj['Table']['Row']

        for row in rows:
            elems_map[row['Cell'][1]] = row['Cell']

    elems_map_transformed = {}
    for symb, attr in elems_map.items():
        neut = ELEMENTS_DATA[symb]['num_neutrons']
        prot = ELEMENTS_DATA[symb]['num_protons']
        el = ELEMENTS_DATA[symb]['num_electrons']

        attr = attr + [neut, prot, el]
        attr_map = {}
        for i, att in enumerate(attr):
            try:
                att = float(att)
            except ValueError:
                att = str(att)
            attr_map[cols[i]] = att
        elems_map_transformed[symb] = attr_map

    return elems_map_transformed


if __name__ == '__main__':
    # Run this initially to create and populate the database
    create_and_populate_db('PUBCHEMDB', 'elements', ELEMENTS_DATA)
