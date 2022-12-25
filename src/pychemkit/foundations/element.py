from pychemkit.database.loader import ELEMENTS_DATA
from pychemkit.utils.utils import is_number


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

    def __eq__(self, other):
        return self.symbol == other.symbol

    def __hash__(self):
        return hash(str(self))

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

    def get_moles(self, mass):
        if is_number(mass):
            return mass / self._atomic_mass
        else:
            return 'Enter a valid mass in grams'

    def __str__(self):
        return f'{self._symbol}'

    def __repr__(self):
        return f"Element('{self._symbol}')"


if __name__ == '__main__':
    h1 = Element('H')
    h2 = Element('H')
    print(h1 == h2)