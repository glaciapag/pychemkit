from pychemkit.foundations.compound import Compound


class SimpleChemicalReaction:

    def __init__(self, reactants=None, products=None, *args, **kwargs):
        if isinstance(reactants, str):
            self._reactants = [Compound(reactants)]
        elif isinstance(reactants, list):
            self._reactants = [Compound(react) for react in reactants]
        if isinstance(products, str):
            self._products = [Compound(products)]
        elif isinstance(products, list):
            self._products = [Compound(prod) for prod in products]

    @property
    def reactants(self):
        return self._reactants

    @property
    def products(self):
        return self._products

    @staticmethod
    def _stringify(comp_list):
        return " + ".join([comp.formula for comp in comp_list])

    def __str__(self):
        return f'{self._stringify(self._reactants)} ==> {self._stringify(self._products)}'


if __name__ == '__main__':
    water_formation = SimpleChemicalReaction(
        reactants=['H2', 'O2'],
        products=['H2O']
    )
    print(water_formation)
