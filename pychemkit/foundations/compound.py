import re
from pychemkit.foundations.element import Element
from pychemkit.utils.utils import get_elements_array, is_number
from pychemkit.foundations.constants import AVOGADRO_NUM


class Compound:

    def __init__(self, formula_str):
        self._formula = formula_str
        self._composition = self.parse_formula()

    def get_molecular_mass(self):
        mass = 0
        for elem, coeff in self._composition.items():
            mass += (elem.atomic_mass * coeff)
        return mass

    def get_moles(self, mass):
        if is_number(mass):
            return mass / self.get_molecular_mass()
        else:
            return 'Enter a valid mass in grams'

    def get_atoms(self, mass):
        if is_number(mass):
            mole = self.get_moles(mass)
            return mole * AVOGADRO_NUM
        else:
            return 'Enter a valid mass in grams'

    def parse_formula(self):
        elems_array = get_elements_array(self._formula)
        elems_count_map = {}

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
            elem_instance = Element(symb)
            elems_count_map[elem_instance] = num_elems

        return elems_count_map

    def get_element_percentage(self, element):
        element = Element(element)
        compound_mass = self.get_molecular_mass()
        element_mass = element.atomic_mass
        return (element_mass / compound_mass) * 100

    def __str__(self):
        return f'{self._composition}'


if __name__ == '__main__':
    cufes2 = Compound('CuFeS2')
    print(cufes2.get_element_percentage('Fe'))

