import re
from typing import List, Dict, Union


def get_query_string(symbol: str, attr: Dict) -> str:
    """
    Utility function that forms a query string to be inserted into a 'INSERT INTO' SQL query
    :param symbol: symbol of an element e.g., 'H'
    :param attr: a dictionary with the corresponding attributes e.g., {'num_protons': 1, 'atomic_number': 2}
    :return: a query string formed in the form of ('H', 1, 0, ....., etc) which will be used in the SQL Query
    """
    query_items = [f"'{symbol}'"]
    for key, att in attr.items():
        if key != 'symbol' and key != 'CPKHexColor':
            if isinstance(att, str):
                query_items.append(rf"'{att}'")
            else:
                query_items.append(str(att))

    query_str = ', '.join(query_items)
    query_str = f'({query_str});'
    return query_str


def flatten(multi_dim_list: List[List[str]]) -> List[str]:
    """
    Utility function that flattens a list of list n-d into a 1-d array
    :param multi_dim_list: a list of list [[1, 2], [3, 4]]
    :return: flattened list [1, 2, 3, 4]
    """
    flattened = []
    for row in multi_dim_list:
        for col in row:
            flattened.append(col)
    return flattened


def get_coeff_multiplier(formula_str: str) -> int:
    """
    Utility function that takes the coefficient multiplier from a string pattern
    :param formula_str: a formula string pattern with parenthesis '(CO)2'
    :return: int multiplier ex: 2 for the above input
    """
    try:
        mult = formula_str[1][-1]
        mult = int(mult)
    except ValueError:
        mult = 1
    except IndexError:
        mult = 1
    return mult


def get_elements_array(formula_str: str) -> List[str]:
    """
    Utility function that parses the compound formula and turn it into a list of elements
    :param formula_str: a string of compound formula example: CH3COOH
    :return: a list of strings that corresponds to the element [2C, 4H, 2O]
    """
    elems_pt = '\([A-Za-z0-9]*\)\d*'  # Everything inside a parenthesis and the coeff ex: (CH3)2
    elems_pt_compiled = re.compile(elems_pt)

    elems_inside_parens = elems_pt_compiled.findall(formula_str)
    elems_outside_parens = re.split(elems_pt, formula_str)

    elems_count_list = []

    for elems in elems_inside_parens:
        el_pt = '\(*[A-Z][a-z]*\d*\)*\d*'
        el = re.compile(el_pt)
        res = el.findall(elems)
        res = [r.replace('(', '') for r in res]
        if res:
            multiplier = get_coeff_multiplier(res)

            res = [f'{multiplier}{r}' for r in res]
            res = [r.replace(f'){multiplier}', '') if multiplier > 1 else r.replace(')', '') for r in res]
            elems_count_list.append(res)

    for elems in elems_outside_parens:
        el_pt = '[A-Z][a-z]*\d*'
        el = re.compile(el_pt)
        res = el.findall(elems)
        if res:
            res = [f'1{r}' for r in res]
            elems_count_list.append(res)

    elems_count_list = flatten(elems_count_list)
    return elems_count_list


def is_number(num) -> bool:
    """
    Utility function that checks whether or not an input is an instance of common number data type (float, int)
    :param num: an input value which can be of any type (str, int, float)
    :return: bool value that checks whether the input is a number or not
    """
    if isinstance(num, float) or isinstance(num, int):
        return True
    else:
        return False


def separate_compound_coeff(compound_list: List[str]) -> Dict:
    """
    Utility function that separates the coefficient from the compound
    :param compound_list: a list of compounds either from reactants/products class e.g., ['2H2O', 'O2', '2NaCl']
    :return: a dictionary in the form of {'compound_name' : coeff} -> {str, int} e.g., {'H2O': 2, 'O2': 1, 'NaCl': 2}
    """

    compound_coeff_map = {}
    for compound in compound_list:
        coeff_pt = r'\b\d{1,1000000}'
        coeff = re.compile(coeff_pt)
        res = coeff.findall(compound)

        if res:
            coeff = int(res[0])
            cpd = compound.replace(f'{coeff}', '', 1)  # Replace the first occurence of the integer coeff with nothing
        else:
            coeff = 1
            cpd = compound
        compound_coeff_map[cpd] = coeff

    coefficients = [v for k, v in compound_coeff_map.items()]
    return compound_coeff_map


def listify_strings(str_list_input: Union[str, List[str]]) -> List[str]:
    if isinstance(str_list_input, str):
        return [str_list_input]
    elif isinstance(str_list_input, list):
        return str_list_input


def determine_sign(amount, participation):
    if participation == 'product':
        return amount * -1
    else:
        return amount


def get_percentage(x, y):
    return x / y * 100


if __name__ == '__main__':

    print(separate_compound_coeff(['2H2', 'O2', '2H2O']))


