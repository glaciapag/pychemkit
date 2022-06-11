import re
from collections import Counter
from pychemkit.element import Element
from pychemkit.utils import get_elements_array


class Compound:

    def __init__(self, formula_str):
        self._formula = formula_str
        self._composition = self.parse_formula()
        self._molecular_mass = self.compute_molecular_mass()

    @property
    def mass(self):
        return self._molecular_mass

    def compute_molecular_mass(self):
        mass = 0
        for elem, coeff in self._composition.items():
            mass += (elem.atomic_mass * coeff)
        return mass

    def parse_formula(self):
        elems_array = get_elements_array(self._formula)
        elems_count_map_list = []

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
            elems_count_map_list.append(symb * num_elems)

        elem_str_coeff_map = Counter(''.join(elems_count_map_list))
        elems_coeff_map = {}

        for elem, coeff in elem_str_coeff_map.items():
            elem_instance = Element(elem)
            elems_coeff_map[elem_instance] = coeff

        return elems_coeff_map

    def __str__(self):
        return f'{self._composition}'


if __name__ == '__main__':
    formula = 'CH3COOH'
    acetic_acid = Compound(formula)
    print(acetic_acid.mass)