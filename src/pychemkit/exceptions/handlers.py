from typing import List, Union

from pychemkit.foundations.element import Element
from pychemkit.foundations.compound import Compound
from pychemkit.exceptions.invalids import NotAValidCompoundException, NotAValidElementException
from pychemkit.utils.utils import is_number


def entity_handler(entity: Union[str, Element, Compound]) -> Union[str, Element, Compound]:
    """
    Handler for string inputs (not an instance of element, or a compound) 
    :param entity: string input of an  element or a compound
    :return: if valid, an instance of element of a compound, raises an exception if not
    """
    if isinstance(entity, str):
        try:
            entity = Element(entity)
        except NotAValidElementException:
            try:
                entity = Compound(entity)
            except NotAValidCompoundException:
                raise ValueError(
                    f'{entity} is not a valid Element of Compound'
                )

    return (entity, type(entity))


def amount_handler(amount: float) -> float:
    """
    Handler for amount inputs 
    :param amount: float or int input representing valid amounts in grams, moles, etc 
    :return: raises a TypeError if not a valid amount 
    """
    if is_number(amount):
        return amount
    else:
        raise TypeError('Enter a valid amount')


def selection_handler(input: str, selection: List[str]):
    """
    Handler for selections
    :param input: input string 
    :param selection: list of valid selections 
    :return: raises a ValueError if the selection is not in the list 
    """
    if input not in selection:
        raise ValueError(
            f'Invalid input: {input}. Valud options are {selection}'
        )
