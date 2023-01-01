import unittest
import pandas as pd
import numpy as np

from pychemkit.utils import get_percentage
from pychemkit import Element
from pychemkit import Compound


class TestElementMethods(unittest.TestCase):

    def setUp(self) -> None:
        acetic_acid = Compound('CH3COOH')
        acetone = Compound('CH3(CO)CH3')
        glucose = Compound('C6H12O6')
        dmt = Compound('C12H16N2')
        sodium_bicarbonate = Compound('NaHCO3')

        self.test_compounds = [
            acetic_acid,
            acetone,
            glucose,
            dmt,
            sodium_bicarbonate
        ]

        self.mmass = [
            60.050,
            58.080,
            180.160,
            188.270,
            84.007
        ]

    def test_composition(self):
        expected_hcounts = [4, 6, 12, 16, 1]
        expected_ccounts = [2, 3, 6, 12, 1]
        expected_ocounts = [2, 1, 6, 0, 3]

        for index, tc in enumerate(self.test_compounds):
            h_count = tc.composition.get(Element('H'), 0)
            c_count = tc.composition.get(Element('C'), 0)
            o_count = tc.composition.get(Element('O'), 0)

            self.assertEqual(h_count, expected_hcounts[index])
            self.assertEqual(c_count, expected_ccounts[index])
            self.assertEqual(o_count, expected_ocounts[index])

    def test_mass_to_moles(self):
        mass_test_grams = [128, 150, 400, 0.4, 10.9]
        expected_moles = [x / z for x, z in zip(mass_test_grams, self.mmass)]

        for index, tc in enumerate(self.test_compounds):
            moles = tc.mass_to_moles(mass_test_grams[index])
            self.assertAlmostEqual(moles, expected_moles[index], 3)

    def test_get_element_percentage(self):

        mass_c = [24.02, 36.03, 72.06, 144.12, 12.01]
        mass_h = [4.04, 6.06, 12.12, 16.16, 1.01]
        mass_o = [32, 16, 96, 0, 48]

        expected_cpercent = [get_percentage(x, z)
                             for x, z in zip(mass_c, self.mmass)]
        expected_hpercent = [get_percentage(x, z)
                             for x, z in zip(mass_h, self.mmass)]
        # expected_opercent = [get_percentage(x, z) for x, z in zip(self.mmass, mass_o)]

        method_cpercent = [tc.get_element_percentage(
            'C') for tc in self.test_compounds]
        method_hpercent = [tc.get_element_percentage(
            'H') for tc in self.test_compounds]
        # method_opercent = [tc.get_element_percentage('O') for tc in self.test_compounds]

        for i in range(4):
            # self.assertAlmostEqual(expected_opercent[i], method_opercent[i], 3)
            self.assertAlmostEqual(expected_hpercent[i], method_hpercent[i], 1)
            self.assertAlmostEqual(expected_cpercent[i], method_cpercent[i], 1)

    def test_compound_equality(self):

        new_instance_compounds = []

        for compound in self.test_compounds:
            new_compound = Compound(compound.formula)
            new_instance_compounds.append(new_compound)

        for cpd1, cpd2 in zip(self.test_compounds, new_instance_compounds):
            self.assertEqual(cpd1, cpd2)


if __name__ == '__main__':
    unittest.main()
