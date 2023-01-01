from pychemkit.engine.conn import DBQuery

db = DBQuery('PUBCHEMDB')
ELEMENTS_DATA = db.get_all_data('elements')
