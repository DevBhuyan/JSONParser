#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
JSONParser
===========

Author: Devvjiit Bhuyan
Date: 2025-06-01

This script provides utilities to:
- Flatten nested JSON/dictionaries into key-value pairs with compound keys.
- Inflate such flattened dictionaries back into their original nested structure.
- Perform keyword-based or multi-word query-based searches on flattened dictionaries.
"""


import json
from helpers import (
    exists_in,
    SEPARATOR,
    get_close_matches,
    set_nested_value,
    validate_separator
)


def flatten_data(y: dict,
                 separator: str = SEPARATOR):
    """Flatten a nested JSON structure into a flat dictionary.

    Args:
        y (dict): The nested JSON/dict.
        separator (str): The separator to use for concatenated keys.

    Returns:
        dict: A flat dictionary with compound keys.
    """

    validate_separator(separator)

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


def inflate_data(flat: dict,
                 separator: str = SEPARATOR):
    """Inflate a flat dictionary back into a nested JSON structure.

    Args:
        flat (dict): The flattened dictionary.
        separator (str): The separator used in the flat dictionary's keys.

    Returns:
        dict: A nested dictionary/JSON.
    """

    validate_separator(separator)

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


def search_by_query(query: str,
                    src: dict,
                    close_matches: bool = True,
                    match_case: bool = False,
                    n_results: int = 25):
    """
    Search a flattened dictionary by checking for partial or fuzzy matches of each word in the query.

    Args:
        query (str): A sentence or group of words (e.g., "document sensitive policy").
        src (dict): Flattened JSON dictionary where search will be performed.
        close_matches (bool): Enable fuzzy matching using difflib.
        match_case (bool): Whether to enforce case-sensitive matches.
        n_results (int): Maximum number of results to return. Defaults to 25.

    Returns:
        dict: A dictionary of matching entries, sorted by relevance.
    """

    words = query.strip().split()
    results = {}

    def word_in_text(word, text):
        if not isinstance(text, str):
            text = str(text)

        if not match_case:
            word = word.lower()
            text = text.lower()

        if close_matches:
            tokens = []
            key, value = text.split()
            if SEPARATOR in key:
                tokens += key.split(SEPARATOR)
            else:
                tokens += key
            if ' ' in value:
                tokens += value.split()
            else:
                tokens += value
            return bool(get_close_matches(word, tokens))
        else:
            return word in text

    for key, value in src.items():
        combined_text = f"{key}:{value}"
        score = sum(word_in_text(word, combined_text) for word in words)

        if score > 0:
            results[key] = {"value": value, "score": score}

    sorted_results = dict(
        sorted(results.items(), key=lambda item: -item[1]["score"])[:n_results]
    )

    return {k: v["value"] for k, v in sorted_results.items()}


if __name__ == "__main__":

    with open('./complex_json.json') as f:
        complex_json = json.load(f)

    flattened_json = flatten_data(complex_json)
    inflated_json = inflate_data(flattened_json)

    assert complex_json == inflated_json
