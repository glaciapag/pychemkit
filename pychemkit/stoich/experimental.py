import numpy as np
from pychemkit.foundations.compound import Compound


class EmpiricalFormula:

    def __init__(self, elements=None, percentages=None, **kwargs):
        if not kwargs:
            self._compound = self._instantiate_compound(elements)
            self._percentages = percentages
        else:
            elements = [elem for elem in kwargs.keys()]
            self._compound = self._instantiate_compound(elements)
            self._percentages = [mass for mass in kwargs.values()]

        self._total_compound_mass = np.sum(self._percentages)
        self._normalized_percentages = [(p / self._total_compound_mass) * 100 for p in self._percentages]
        self._components = self._get_components()
        self._formula = self._get_formula()

    @property
    def em_components(self):
        return self._components

    @property
    def em_formula(self):
        return self._formula

    @property
    def em_mass(self):
        compound = Compound(self._formula)
        return compound.get_molecular_mass()

    def _get_components(self):
        elem_percentages_map = {}
        elem_components = {}
        for index, (elem, coeff) in enumerate(self._compound.parse_formula().items()):
            mole = elem.get_moles(coeff * self._normalized_percentages[index])
            elem_percentages_map[elem] = mole

        mole_ratio = self._get_min_mole_ratio(elem_percentages_map)
        for index, (elem, coeff) in enumerate(elem_percentages_map.items()):
            elem_components[elem] = mole_ratio[index]
        return elem_components

    def _get_formula(self):
        components = self._components
        elems_mole_list = []
        for elem, mole in components.items():
            elems_mole_list.append(elem.symbol)
            if mole > 1:
                elems_mole_list.append(str(mole))
        return ''.join(elems_mole_list)



    @staticmethod
    def _get_min_mole_ratio(elem_mol_map):
        smallest_mol = np.min([v for v in elem_mol_map.values()])
        moles = [int(np.round((e / smallest_mol), 0)) for e in elem_mol_map.values()]
        return moles

    @staticmethod
    def _instantiate_compound(elements):
        if isinstance(elements, str):
            compound = Compound(elements)
        elif isinstance(elements, list):
            elem_str = ''.join(elements)
            compound = Compound(elem_str)
        else:
            compound = None
        return compound


class MolecularFormula(EmpiricalFormula):

    def __init__(self, elements=None, percentages=None, mass=None, **kwargs):
        super().__init__(elements=elements, percentages=percentages, **kwargs)
        self._molecular_mass = mass
        self._fm_mass_ratio = int(np.round(self._get_mass_ratio(), 0))

    def _get_mass_ratio(self):
        return self._molecular_mass / self.em_mass


if __name__ == '__main__':
    ef = MolecularFormula(K=60.1, C=18.4, N=21.5, mass=130.2)
