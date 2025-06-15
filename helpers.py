#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 16 02:02:39 2025

@author: dev
"""


from difflib import get_close_matches


SEPARATOR = '.'
INVALID_SEPARATORS = [
    ':',
    '"',
    "'",
    ",",
    "\n"
]


def validate_separator(separator: str):

    if separator in INVALID_SEPARATORS:
        raise Exception(
            "Bad Separator. You cannot use the following separators: " + str(INVALID_SEPARATORS))


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


def split_pascal_case(string: str) -> list[str]:
    """
    Split a string by capital letters.

    Example:
    >>> split_pascal_case("MyStringIsAwesome")
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
        elif len(split_pascal_case(sups)) > 1:
            if get_close_matches(subs, split_pascal_case(sups)):
                return True
        else:
            if get_close_matches(subs, sups.split()):
                return True
    elif case_sensitive:
        return subs in sups
    else:
        return subs.lower() in sups.lower()

    return False
