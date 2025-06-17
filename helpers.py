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
    Split a string by capital letters. And yes, it supports splitting numbers and acronyms like if:
        the string is 'abc123def' then it would split 'abc', '123'(the number) and 'def'
        and if the string is like:
        AbcACRONYMAndDef then it will be split like:
        'Abc', 'ACRONYM', 'And', 'Def'
        So as you can see, each word starts with capital letter, so if you add an acronym and then a word starts with capital letter, this function will easily split acronym and word right behind it, for example:
            It would take 'AbcdMYACRONYMIsAwesome'
            as 'Abcd', 'MYACRONYM', 'Is', 'Awesome'
            Instead of 'MYACRONYMIs' or 'MYACRONYMI'

    So your string should have:
        1. Each word starting with a capital letter.
        2. Acronyms as continuous BLOCK letters(Or it can be like normal words starting with capital letter but then it would be treated just like a normal word, so no problem with the function, but humans might have trouble recognising it as an acronym)
        3. Can have numbers too!!!
    And it can also take numbers seperated with dots, colons, hyphens, semi-colons, commas. For Example:

    >>> split_pascal_case('Values1.1dotsAnd2:2colons3;3Semicolons4-4-4HyphensAnd5,5,2commas.')
    ['Values',
     '1.1',
     'dots',
     'And',
     '2:2',
     'colons',
     '3;3',
     'Semicolons',
     '4-4-4',
     'Hyphens',
     'And',
     '5,5,2',
     'commas.']

    Some More Real Examples:
split_pascal_case("MyStringIsAwesome")
    ['My', 'String', 'Is', 'Awesome']
    >>> split_pascal_case('TheNASAIsFromUSAWhichIsUnitedStatesOfAmerica')
    ['The',
     'NASA',
     'Is',
     'From',
     'USA',
     'Which',
     'Is',
     'United',
     'States',
     'Of',
     'America']
    >>> split_pascal_case('Version5Has1047LinesOfCode')
    ['Version', '5', 'Has', '1047', 'Lines', 'Of', 'Code']

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
    for i in range(len(string) - 2):  # iterate.
        part += string[i]  # add the character.

        if string[i + 1].isalpha():  # Next char is Alphabet.
            # Handle numbers seperated with dots, colons, hyphens, semicolons, commas
            if string[i].isdigit() and (string[i + 1] == '.' or string[i + 1] == '-' or string[i + 1] == ':' or string[i + 1] == ';' or string[i + 1] == '-') and string[i + 2].isdigit():
                continue  # keep going untill the number ends.

            # Another word after an Acronym like NASA.
            if string[i].isupper() and string[i + 2].islower() and string[i + 1].isupper():
                splitted.append(part)  # add the part
                part = ''  # reset, new part starts!

            # A word is starting after a number so we end the number and start a new part, the next letters.
            elif string[i].isdigit():
                splitted.append(part)  # add part.
                part = ''  # reset.

            # An Acronym A.K.A continuous stream of BLOCK letters.
            elif string[i].isalpha() and string[i].isupper() and string[i + 1].isupper():
                continue  # Nothing to do...

            # A new word is starting.
            elif string[i].isalpha() and string[i].islower() and string[i + 1].isupper():
                splitted.append(part)
                part = ''

        # Next word is not alphabet.

        # A number is coming so we end the word.
        elif string[i].isalpha() and string[i + 1].isdigit():
            splitted.append(part)
            part = ''

        # It's a multi-digit number so we keep going untill the number ends.
        elif string[i + 1].isdigit() and string[i].isdigit():
            continue  # Nothing to do, just keep going next.

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
