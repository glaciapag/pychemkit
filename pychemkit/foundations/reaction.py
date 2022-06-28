from pychemkit.foundations.compound import Compound
from pychemkit.utils.utils import separate_compound_coeff, listify_strings


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

    def get_reactant_elements(self):
        return self._get_elements(self._reactants)

    def get_product_elements(self):
        return self._get_elements(self._products)

    def balance(self):
        reactants = self.get_reactant_elements()
        products = self.get_product_elements()

        react_weights = 0
        prod_weights = 0

        for elem, w in reactants.items():
            react_weights += (w['subs'] * w['coeff'])

        for elem, w in products.items():
            prod_weights += (w['subs'] * w['coeff'])

        if react_weights == prod_weights:
            return 'Balanced'
        else:
            diff = react_weights - prod_weights
            new_coeffs = {}
            if diff > 0:
                for elem, w in products.items():
                    if w['subs'] * w['coeff'] != diff:
                        new_coeffs[elem] = {
                            'subs': w['subs'],
                            'coeff': w['coeff'] * diff
                        }
                    else:
                        pass
            return 'Not balanced'

    @staticmethod
    def _get_elements(component):
        elem_list = {}
        for comp, coeff in component.items():
            for elem, amt in comp.composition.items():
                elem_list[elem] = {'subs': amt, 'coeff': coeff}
        return elem_list

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


if __name__ == '__main__':

    nacl_formation2 = SimpleChemicalReaction(
        reactants=['Na', 'Cl2'],
        products=['NaCl']
    )
    print(nacl_formation2.balance())