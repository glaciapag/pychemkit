from typing import Union, List

import numpy as np
from pychemkit.exceptions.invalids import NotAValidCompoundException, NotAValidElementException
from pychemkit.foundations.element import Element
from pychemkit.foundations.compound import Compound
from pychemkit.foundations.constants import AVOGADRO_NUM
from pychemkit.utils.utils import is_number
from pychemkit.exceptions.handlers import entity_handler, amount_handler, selection_handler


class StoichConverter:

    def convert_mass(self, entity: Union[str, Element, Compound], mass: float, to: str) -> float:
        """
        Converts mass in grams to mole, given a compound
        :param Compound: An instance of a compound
        :param mass: mass in grams
        """

        selection_handler(to, ['moles', 'atoms'])
        entity, ent_type = entity_handler(entity)

        mass = amount_handler(mass)

        if ent_type == Element:
            ent_mass = entity.atomic_mass
        elif ent_type == Compound:
            ent_mass = entity.molecular_mass

        moles = mass / ent_mass

        if to == 'moles':
            return moles
        elif to == 'atoms':
            return np.round(moles * AVOGADRO_NUM, 1)
