import unittest
from pychemkit import EmpiricalFormula
from pychemkit import Element


class TestEmpiricalFormula(unittest.TestCase):

    def setUp(self):

        # 13.5 g Ca, 10.8 g O, and 0.675 g H
        self.em1 = EmpiricalFormula(Ca=13.5, O=10.8, H=0.675)

        # 1.52 g of nitrogen (N) and 3.47 g of oxygen (O) 
        self.em2 = EmpiricalFormula(N=1.52, O=3.47)


    def test_empirical_components(self):
        
        self.assertEqual(self.em1.em_components, {Element('Ca'): 1, Element('O'): 2, Element('H'): 2})
        self.assertEqual(self.em2.em_components, {Element('N'): 1, Element('O'): 2})


    def test_empirical_components(self):

        self.assertEqual(self.em1.em_formula, "CaO2H2")
        self.assertEqual(self.em2.em_formula, "NO2")
        