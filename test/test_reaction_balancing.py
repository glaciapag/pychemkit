import unittest
from pychemkit import SimpleChemicalReaction


class TestSimpleChemicalReaction(unittest.TestCase):

    def setUp(self) -> None:
        reaction1 = SimpleChemicalReaction(
            reactants=['KNO3', 'C'],
            products=['K2CO3', 'CO', 'N2']
        )

        reaction2 = SimpleChemicalReaction(
            reactants=['C6H6', 'O2'],
            products=['CO2', 'H2O']
        )

        reaction3 = SimpleChemicalReaction(
            reactants=['Al', 'O2'],
            products=['Al2O3']
        )

        reaction4 = SimpleChemicalReaction(
            reactants=['N2', '3H2'],
            products=['2NH3']
        )

        self.reactions = [
            reaction1,
            reaction2,
            reaction3,
            reaction4
        ]

    def test_balance(self):
        expected_results = [
            [2, 4, 1, 3, 1],
            [2, 15, 12, 6],
            [4, 3, 2],
            [1, 3, 2]
        ]

        for res, reaction in enumerate(self.reactions):
            self.assertEqual(reaction.balance(), expected_results[res])
