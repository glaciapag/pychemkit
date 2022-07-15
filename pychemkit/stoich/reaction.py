import pandas as pd
import numpy as np

from pychemkit.foundations.compound import Compound
from pychemkit.utils.utils import separate_compound_coeff, listify_strings, determine_sign, solve_equation


class SimpleChemicalReaction:

    def __init__(self,
                 reactants=None,
                 products=None,
                 react_coeff=None,
                 prod_coeff=None,
                 *args,
                 **kwargs):

        if not react_coeff:
            self._reactants = self.transform_compound_inputs(reactants)
            self._react_coeff = [c for c in self._reactants.values()]
        else:
            react_list = listify_strings(reactants)
            self._reactants = self.update_coefficients(react_list, react_coeff)
            self._react_coeff = react_coeff

        if not prod_coeff:
            self._products = self.transform_compound_inputs(products)
            self._prod_coeff = [c for c in self._products.values()]
        else:
            prod_list = listify_strings(products)
            self._products = self.update_coefficients(prod_list, prod_coeff)
            self._prod_coeff = prod_coeff

    @property
    def reactants(self):
        return {comp: coeff for comp, coeff in self._reactants.items()}

    @property
    def products(self):
        return {comp: coeff for comp, coeff in self._products.items()}

    def get_elements_list(self):
        r = [el for el in self.get_all_reactants_elements().keys()]
        p = [el for el in self.get_all_products_elements().keys()]
        assert set(r) == set(p)
        return r

    def get_all_reactants_elements(self):
        return self._get_elements_per_participants(self._reactants)

    def get_all_products_elements(self):
        return self._get_elements_per_participants(self._products)

    def get_reactant_elements_per_compound(self):
        return self._get_elements_per_compound(self._reactants)

    def get_product_elements_per_compound(self):
        return self._get_elements_per_compound(self._products)

    # TODO
    def balance(self):
        eq_mat = self.create_reaction_matrix()
        return solve_equation(eq_mat)


    @staticmethod
    def _get_elements_per_participants(component):
        elem_list = {}
        for comp, coeff in component.items():
            for elem, amt in comp.composition.items():
                elem_list[elem.symbol] = coeff * amt
        return elem_list

    @staticmethod
    def _get_elements_per_compound(component):
        comp_list = [item for item in component.items()]
        elem_per_cpd = {}
        for comp in comp_list:
            elem_per_cpd[comp[0]] = {el.symbol: coeff for el, coeff in comp[0].composition.items()}
        return elem_per_cpd

    @staticmethod
    def _stringify_reaction(comp_list, coeff_list):
        return " + ".join([f'{coeff}{comp.formula}' if coeff > 1 else comp.formula for comp, coeff in zip(comp_list, coeff_list)])

    @staticmethod
    def _combine_formula_coeff(comp_list, coeff_list):
        combined_list = []
        for comp, coeff in zip(comp_list, coeff_list):
            if coeff > 1:
                formula = f'{coeff}{comp.formula}'
            else:
                formula = comp.formula
            combined_list.append(formula)
        return combined_list

    @staticmethod
    def _compoundify(comp_coeff_map):
        compoundified_map = {}
        for comp, coeff in comp_coeff_map.items():
            compound_obj = Compound(comp)
            compoundified_map[compound_obj] = coeff
        return compoundified_map

    def transform_compound_inputs(self, comp_list):
        comp_str_list = listify_strings(comp_list)
        separated_map = separate_compound_coeff(comp_str_list)
        transformed_map = self._compoundify(separated_map)
        return transformed_map

    def update_coefficients(self, comp_list, coeff_list):

        if len(comp_list) == len(coeff_list):
            updated_dict = {}
            for index, (comp, coeff) in enumerate(self.transform_compound_inputs(comp_list).items()):
                updated_dict[comp] = coeff_list[index]
                index += 1
            return updated_dict
        else:
            raise TypeError('Number of coefficients must be equal to the number of compounds entered')

    def __str__(self):
        return f'{self._stringify_reaction(self._reactants, self._react_coeff)} ==> {self._stringify_reaction(self._products, self._prod_coeff)}'

    def create_reaction_matrix(self):
        reacts = self.get_reactant_elements_per_compound()
        prods = self.get_product_elements_per_compound()
        all_elems = self.get_elements_list()
        compound_matrix = []

        for comp, elems_coeff in reacts.items():
            for elem in all_elems:
                if elem in comp.formula:
                    compound_matrix.append(['reactant', comp, elem, elems_coeff[elem]])
                else:
                    compound_matrix.append(['reactant', comp, elem, 0])

        for comp, elems_coeff in prods.items():
            for elem in all_elems:
                if elem in comp.formula:
                    compound_matrix.append(['product', comp, elem, elems_coeff[elem]])
                else:
                    compound_matrix.append(['product', comp, elem, 0])

        matrix = pd.DataFrame(data=compound_matrix, columns=['role', 'compound', 'element', 'amount'])
        matrix['amount'] = np.vectorize(determine_sign)(matrix['amount'], matrix['role'])
        matrix_pivot = matrix.pivot(index='element', columns='compound', values='amount')
        return matrix_pivot.reset_index()


if __name__ == '__main__':

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

    print(reaction1.balance())
    print(reaction2.balance())
    print(reaction3.balance())
    print(reaction4.balance())
