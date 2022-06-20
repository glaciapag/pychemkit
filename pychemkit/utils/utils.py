import re
from typing import List
from pychemkit.resources.pubchem_data import ELEMENTS_DATA


def get_query_string(symbol: str, attr: dict) -> str:
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
    flattened = []
    for row in multi_dim_list:
        for col in row:
            flattened.append(col)
    return flattened


def get_coeff_multiplier(str_pattern: str) -> int:
    try:
        mult = str_pattern[1][-1]
        mult = int(mult)
    except ValueError:
        mult = 1
    except IndexError:
        mult = 1
    return mult


def get_elements_array(formula_str: str) -> []:
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
    if isinstance(num, float) or isinstance(num, int):
        return True
    else:
        return False


if __name__ == '__main__':

    for symb, attr in ELEMENTS_DATA.items():
        print(get_query_string(symb, attr))

