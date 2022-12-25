from pychemkit.database.engine import DBQuery

db = DBQuery('PUBCHEMDB')
ELEMENTS_DATA = db.get_all_data('elements')