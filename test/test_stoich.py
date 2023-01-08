import unittest

from pychemkit.foundations.element import Element
from pychemkit.foundations.compound import Compound
from pychemkit.foundations.constants import AVOGADRO_NUM
from pychemkit.stoich.converter import StoichConverter


class TestStoich(unittest.TestCase):

    def setUp(self) -> None:

        el1 = Element('C')
        el2 = Element('Hg')
        el3 = 'Po'

        cpd1 = Compound('CH3COOH')
        cpd2 = Compound('NaCl')
        cpd3 = 'MgSO4'

        self.test_elements = [el1, el2, el3]
        self.test_compounds = [cpd1, cpd2, cpd3]

        self.test_elem_masses = [12.01, 200.59, 208.98243]
        self.test_cpd_masses = [60.025, 58.44, 120.366]

        self.converter = StoichConverter()

    def test_mass_to_moles(self):

        convert_to_list = ['moles']

        expected_moles = {
            'moles': [1, 1, 1],
            'atoms': [AVOGADRO_NUM] * 3
        }

        for to in convert_to_list:
            for i, (el, cpd) in enumerate(zip(self.test_elements, self.test_compounds)):
                expected = expected_moles.get(to)[i]
                actual_el = self.converter.convert_mass(
                    entity=el,
                    mass=self.test_elem_masses[i],
                    to=to
                )

                actual_cpd = self.converter.convert_mass(
                    entity=cpd,
                    mass=self.test_cpd_masses[i],
                    to=to
                )

                self.assertAlmostEqual(actual_el, expected, 1)
                self.assertAlmostEqual(actual_cpd, expected, 1)


if __name__ == '__main__':
    unittest.main()
