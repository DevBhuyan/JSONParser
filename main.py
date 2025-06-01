#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Sun Jun  1 21:54:04 2025

@author: dev
"""


from difflib import get_close_matches
import json


with open('./complex_json.json') as f:
    complex_json = json.load(f)

SEPARATOR = '.'


def flatten_data(y: dict,
                 separator: str = SEPARATOR):
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
    flattened_json = flatten_data(complex_json)
    inflated_json = inflate_data(flattened_json)

    assert complex_json == inflated_json
