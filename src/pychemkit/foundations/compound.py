import re
from pychemkit.foundations.element import Element
from pychemkit.utils.utils import get_elements_array, is_number, get_percentage
from pychemkit.foundations.constants import AVOGADRO_NUM
from pychemkit.exceptions import NotAValidElementException, NotAValidCompoundException


class Compound:

    def __init__(self, formula_str):
        self._formula = formula_str
        try:
            self._composition = self._parse_formula()
        except NotAValidCompoundException as e:
            raise NotAValidCompoundException(f'{formula_str} is {e}')

    @property
    def formula(self):
        return self._formula

    @property
    def composition(self):
        return self._composition

    @property
    def molecular_mass(self):
        return self._get_molecular_mass()

    def moles_to_mass(self, moles):
        if is_number(moles):
            return moles * self._get_molecular_mass()
        else:
            return 'Enter a valid mole value'

    def moles_to_atoms(self, moles):
        if is_number(moles):
            return moles * AVOGADRO_NUM
        else:
            return 'Enter a valid mole value'

    def atoms_to_moles(self, atoms):
        if is_number(atoms):
            return atoms / AVOGADRO_NUM
        else:
            return 'Enter a valid number of atoms'

    def atoms_to_mass(self, atoms):
        if is_number(atoms):
            moles = self.atoms_to_moles(atoms)
            mass = self.moles_to_mass(moles)
            return mass
        else:
            return 'Enter a valid number of atoms'

    def _get_molecular_mass(self):
        mass = 0
        for elem, coeff in self.composition.items():
            mass += (elem.atomic_mass * coeff)
        return mass

    def _get_moles(self, mass):
        if is_number(mass):
            return mass / self._get_molecular_mass()
        else:
            return 'Enter a valid mass in grams'

    def _get_atoms(self, mass):
        if is_number(mass):
            mole = self._get_moles(mass)
            return mole * AVOGADRO_NUM
        else:
            return 'Enter a valid mass in grams'

    def _parse_formula(self):
        elems_array = get_elements_array(self._formula)
        elems_count_list = []
        elems_count_map = {}
        elementified_map = {}

        for elems in elems_array:
            mult = int(elems[0])
            coeff_pt = re.compile('\d+')
            coeff_res = coeff_pt.findall(elems[1:])
            if coeff_res:
                coeff = coeff_res[0]
                num_elems = int(coeff) * mult
            else:
                coeff = ''
                num_elems = 1 * mult
            symb = elems[1:].replace(coeff, '')
            elems_count_list.append([symb, num_elems])

        for elem in elems_count_list:
            elems_count_map[elem[0]] = elems_count_map.get(
                elem[0], 0) + elem[1]

        for elem, coeff in elems_count_map.items():
            try:
                elem_instance = Element(elem)
                elementified_map[elem_instance] = coeff
            except NotAValidElementException:
                raise NotAValidCompoundException('not a valid Compound')

        return elementified_map

    def get_element_percentage(self, element):
        element = Element(element)
        coeff = self.composition.get(element)
        compound_elements = [elem for elem in list(self.composition.keys())]
        if element in compound_elements:
            compound_mass = self._get_molecular_mass()
            element_mass = element.atomic_mass * coeff
            return get_percentage(element_mass, compound_mass)
        else:
            return f'{element} is not present in {self._formula}'

    def __str__(self):
        return f'{self._formula}'

    def __repr__(self):
        return f'Compound({self._formula})'

    def __eq__(self, other):
        return self.composition == other.composition

    def __hash__(self):
        return hash(str(self))
        