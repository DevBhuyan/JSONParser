#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
JSONParser
===========

Author: Devvjiit Bhuyan
Date: 2025-06-01

This script provides utilities to flatten and inflate JSON structures, as well as perform
keyword-based searches over flattened JSONs.

Functions:
- flatten_data: Flatten a nested JSON/dict.
- inflate_data: Inflate a flattened dict back into JSON.
- search_by_keyword: Search for keywords in keys and/or values of a flattened JSON.
"""

import json
from difflib import get_close_matches

SEPARATOR = '.'


def split_capitals(string: str) -> list[str]:
    """
    Split a string by capital letters.

    Example:
    >>> split_capitals("MyStringIsAwesome")
    ['My', 'String', 'Is', 'Awesome']
    >>>
    >>>

    Parameters
    ----------
    string : str
        The string to split.

    Returns
    -------
    list[str]
        list of strings, the splitted string.

    """
    # Make sure not to modify the original variable in place. 
    # That would change it globally everywhere.
    s = string
    splitted = []  # end result.
    part = ''  # the part of the string to append.
    for i in range(len(string) - 1):  # iterate.
        part += string[i]  # add the character.
        if string[i + 1].isupper():  # End of a word.
            splitted.append(part)  # append the part.
            part = ''  # Reset, new part coming!

    s = s.replace(''.join(splitted), '')  # to append the last part left.
    splitted.append(s)  # append the last part left.

    return splitted  # return the result.


def flatten_data(y: dict, separator: str = SEPARATOR):
    """Flatten a nested JSON structure into a flat dictionary.

    Args:
        y (dict): The nested JSON/dict.
        separator (str): The separator to use for concatenated keys.

    Returns:
        dict: A flat dictionary with compound keys.
    """
    out = {}

    def flatten(x, name=''):
        if type(x) is dict:
            for a in x:
                flatten(x[a], name + a + separator)
        elif type(x) is list:
            i = 0
            for a in x:
                flatten(a, name + str(i) + separator)
                i += 1
        else:
            out[name[:-1]] = x

    flatten(y)
    return out


def inflate_data(flat: dict, separator: str = SEPARATOR):
    """Inflate a flat dictionary back into a nested JSON structure.

    Args:
        flat (dict): The flattened dictionary.
        separator (str): The separator used in the flat dictionary's keys.

    Returns:
        dict: A nested dictionary/JSON.
    """
    def set_nested_value(d, keys, value):
        for i, key in enumerate(keys):
            if key.isdigit():
                key = int(key)
                if not isinstance(d, list):
                    d_temp = []
                    for _ in range(max(key + 1, len(d)) if isinstance(d, list) else key + 1):
                        d_temp.append({} if i < len(keys) - 1 else None)
                    if isinstance(d, dict):
                        for k, v in d.items():
                            try:
                                d_temp[int(k)] = v
                            except:
                                pass
                    d = d_temp
                while len(d) <= key:
                    d.append({} if i < len(keys) - 1 else None)
                if i == len(keys) - 1:
                    d[key] = value
                else:
                    if not isinstance(d[key], dict) and not isinstance(d[key], list):
                        d[key] = {}
                    d[key] = set_nested_value(d[key], keys[i + 1:], value)
                return d
            else:
                if i == len(keys) - 1:
                    d[key] = value
                else:
                    if key not in d:
                        d[key] = {} if not keys[i + 1].isdigit() else []
                    d[key] = set_nested_value(d[key], keys[i + 1:], value)
                return d

    result = {}
    for flat_key, value in flat.items():
        keys = flat_key.split(separator)
        result = set_nested_value(result, keys, value)

    return result


def search_by_keyword(src: dict,
                      keyword: str,
                      case_sensitive: bool = True,
                      close_matches: bool = False,
                      keys_only: bool = False,
                      values_only: bool = False):
    """Search a flattened dictionary for keys or values that match a given keyword.

    Args:
        src (dict): The dictionary to search in.
        keyword (str): The keyword to search for.
        case_sensitive (bool): Whether the search is case-sensitive.
        close_matches (bool): Whether to use fuzzy matching.
        keys_only (bool): Search only keys.
        values_only (bool): Search only values.

    Returns:
        dict: Dictionary with matches in 'by_key' and/or 'by_value'.
    """
    out = {
        "by_key": {},
        "by_value": {}
    }

    def exists_in(sups: str,
                  subs: str,
                  case_sensitive: bool,
                  close_matches: bool):

        if not isinstance(sups, str):
            sups = str(sups)
        if not isinstance(subs, str):
            subs = str(subs)

        if close_matches:
            if len(sups.split(SEPARATOR)) > 1:
                if get_close_matches(subs, sups.split(SEPARATOR)):
                    return True
            else:
                if get_close_matches(subs, sups.split()):
                    return True
        elif case_sensitive:
            return subs in sups
        else:
            return subs.lower() in sups.lower()

        return False

    for key, value in src.items():
        if exists_in(key,
                     keyword,
                     case_sensitive,
                     close_matches) and not values_only:
            out["by_key"][key] = value
        elif exists_in(value,
                       keyword,
                       case_sensitive,
                       close_matches) and not keys_only:
            out["by_value"][key] = value

    return out


if __name__ == "__main__":

    with open('./complex_json.json') as f:
        complex_json = json.load(f)

    flattened_json = flatten_data(complex_json)
    inflated_json = inflate_data(flattened_json)

    assert complex_json == inflated_json
