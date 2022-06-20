import unittest
from pychemkit.foundations.element import Element


class TestElementMethods(unittest.TestCase):

    def setUp(self) -> None:
        hydrogen = Element('H')
        mercury = Element('Hg')
        cobalt = Element('Co')
        rutherfordium = Element('Rf')
        radon = Element('Rn')
        lead = Element('Pb')
        calcium = Element('Ca')
        francium = Element('Fr')
        seaborgium = Element('Sg')
        promethium = Element('Pr')

        self.random_elements = [
            hydrogen,
            mercury,
            cobalt,
            rutherfordium,
            radon,
            lead,
            calcium,
            francium,
            seaborgium,
            promethium
        ]

    def test_symbol(self):
        res = ['H', 'Hg', 'Co', 'Rf', 'Rn', 'Pb', 'Ca', 'Fr', 'Sg', 'Pr']
        for i, elems in enumerate(self.random_elements):
            self.assertEqual(elems.symbol, res[i])

    def test_name(self):
        res = ['Hydrogen', 'Mercury', 'Cobalt', 'Rutherfordium', 'Radon', 'Lead', 'Calcium', 'Francium', 'Seaborgium', 'Praseodymium']
        for i, elems in enumerate(self.random_elements):
            self.assertEqual(elems.name, res[i])

    def test_electrons(self):
        res = [1, 80, 27, 104, 86, 82, 20, 87, 106, 59]
        for i, elems in enumerate(self.random_elements):
            self.assertEqual(elems.electrons, res[i])

    def test_protons(self):
        res = [1, 80, 27, 104, 86, 82, 20, 87, 106, 59]
        for i, elems in enumerate(self.random_elements):
            self.assertEqual(elems.electrons, res[i])

    def test_atomic_mass(self):
        res = [1.0080, 200.59, 58.93319, 267.122, 222.01758, 207, 40.08, 223.01973, 269.128, 140.90766]
        for i, elems in enumerate(self.random_elements):
            self.assertAlmostEqual(elems.atomic_mass, res[i], 2)

    def test_neutrons(self):
        res = [0, 121, 32, 157, 136, 125, 20, 136, 157, 82]
        for i, elems in enumerate(self.random_elements):
            self.assertAlmostEqual(elems.neutrons, res[i], delta=4)


if __name__ == '__main__':
    unittest.main()
