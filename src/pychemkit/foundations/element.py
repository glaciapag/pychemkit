from pychemkit.data import ELEMENTS_DATA
from pychemkit.utils.utils import is_number
from pychemkit.exceptions import NotAValidElementException


class Element:

    elements_data = ELEMENTS_DATA.copy(deep=True)

    def __init__(self, symbol):
        self._symbol = symbol
        self._symbol_filter = self.elements_data['symbol'] == symbol

        self._name = self._filter_column('element_name')
        self._electrons = self._filter_column('num_electrons')
        self._protons = self._filter_column('num_protons')
        self._neutrons = self._filter_column('num_neutrons')
        self._atomic_mass = self._filter_column('atomic_mass')
        self._electron_configuration = self._filter_column(
            'electron_configuration')
        self._electronegativity = self._filter_column('electronegativity')
        self._atomic_radius = self._filter_column('atomic_radius')
        self._ionization_energy = self._filter_column('ionization_energy')
        self._electron_affinity = self._filter_column('electron_affinity')
        self._oxidation_states = self._filter_column('oxidation_states')
        self._standard_states = self._filter_column('standard_state')
        self._melting_point = self._filter_column('melting_point')
        self._boiling_point = self._filter_column('boiling_point')
        self._density = self._filter_column('density')
        self._group_block = self._filter_column('group_block')
        self._year_discovered = self._filter_column('year_discovered')

    def __eq__(self, other):
        return self.symbol == other.symbol

    def __hash__(self):
        return hash(str(self))

    def _filter_column(self, prop):
        try:
            return self.elements_data.loc[self._symbol_filter, prop].values[0]
        except IndexError:
            raise NotAValidElementException(f'{self.symbol} is not a valid Element')

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

    @property
    def electronegativity(self):
        return self._electronegativity

    @property
    def atomic_radius(self):
        return self._atomic_radius

    @property
    def ionization_energy(self):
        return self._ionization_energy

    @property
    def electron_affinity(self):
        return self._electron_affinity

    @property
    def oxidation_states(self):
        return self._oxidation_states

    @property
    def standard_states(self):
        return self._standard_states

    @property
    def melting_point(self):
        return self._melting_point

    @property
    def boiling_point(self):
        return self._boiling_point

    @property
    def density(self):
        return self._density

    @property
    def group_block(self):
        return self._group_block

    @property
    def year_discovered(self):
        return self._year_discovered

    def get_moles(self, mass):
        if is_number(mass):
            return mass / self._atomic_mass
        else:
            return 'Enter a valid mass in grams'

    def __str__(self):
        return f'{self._symbol}'

    def __repr__(self):
        return f"Element('{self._symbol}')"
