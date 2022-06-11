from pychemkit.database.engine import ELEMENTS_DATA


class Element:

    elements_data = ELEMENTS_DATA.copy(deep=True)

    def __init__(self, symbol):
        self._symbol = symbol
        self._symbol_filter = self.elements_data['symbol'] == symbol

        self._name = self.filter_column('element_name')
        self._electrons = self.filter_column('num_electrons')
        self._protons = self.filter_column('num_protons')
        self._neutrons = self.filter_column('num_neutrons')
        self._atomic_mass = self.filter_column('atomic_mass')
        self._period = self.filter_column('period')
        self._phase = self.filter_column('phase')
        self._type = self.filter_column('type')
        self._num_shells = self.filter_column('num_shells')

    def filter_column(self, prop):
        return self.elements_data.loc[self._symbol_filter, prop].values[0]

    @property
    def symbol(self):
        return self._symbol

    @property
    def name(self):
        return self._name

    @property
    def electrons(self):
        return self._electrons

    @property
    def protons(self):
        return self._protons

    @property
    def neutrons(self):
        return self._neutrons

    @property
    def atomic_mass(self):
        return self._atomic_mass

    def __str__(self):
        return f'{self._symbol}'

    def __repr__(self):
        return f"Element('{self._symbol}')"
