import re
import json
import pandas as pd
from typing import List


def get_query_string(symbol: str, attr: dict) -> str:
    query_str = f"""(
        '{symbol}',
        {attr['atomic_number']},
        '{attr['element_name']}',
        {attr['atomic_mass']},
        {attr['num_neutrons']},
        {attr['num_protons']},
        {attr['num_electrons']},
        {attr['period']},
        '{attr['phase']}',
        '{attr['type']}',
        {attr['num_shells']}) 
    """
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


def populate_columns(db_instance, table, data):
    assert isinstance(data, dict)
    for symb, attr in data.items():
        db_instance.insert_value(table, symb, attr)


def transform_pubchem_data(json_filepath):

    elems_map = {}

    with open(json_filepath, 'r') as js:
        json_obj = json.load(js)
        cols = json_obj['Table']['Columns']['Column']
        rows = json_obj['Table']['Row']

        for row in rows:
            elems_map[row['"Cell'][1]] = row['Cell']

    elems_map_transformed = {}
    for symb, attr in elems_map.items():
        attr_map = {}
        for i, att in enumerate(attr):
            attr_map[cols[i]] = att
        elems_map_transformed[symb] = attr_map

    return elems_map_transformed
