#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json


## returns a unique json
def uniqueJson(input):
    unique = set()
    output = []

    for i in input:
        repr_i = repr(i)
        if repr_i in unique:
            continue
        unique.add(repr_i)
        output.append(i)
    return output


## Filter World Cities List
def citiesCountry(code, file):
    with open(file) as json_file:  ## open city dictionary
        input = json.load(json_file)
        json_file.close()
        # output = [city for city in input if city["country"] == country_code] #  Old line to use with cities_of_turkey.json file
        output = [city for city in input if city["code"] == code]
        return output
