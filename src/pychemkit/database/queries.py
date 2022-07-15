from enum import Enum, unique


@unique
class Queries(Enum):
    CREATE_TABLE = 'CREATE TABLE'
    DROP_TABLE = 'DROP TABLE'
    INSERT_TABLE = 'INSERT INTO'
    SELECT_ALL = 'SELECT * FROM'


PUBCHEM_ELEMENTS_FIELD = """(
        symbol VARCHAR(5),
        atomic_number REAL,
        element_name VARCHAR(50),
        atomic_mass REAL,
        electron_configuration VARCHAR(200),
        electronegativity REAL,
        atomic_radius REAL,
        ionization_energy REAL,
        electron_affinity REAL,
        oxidation_states REAL,
        standard_state VARCHAR(30),
        melting_point REAL,
        boiling_point REAL,
        density REAL,
        group_block VARCHAR(50),
        year_discovered REAL,
        num_neutrons REAL,
        num_protons REAL,
        num_electrons REAL
    )
"""


