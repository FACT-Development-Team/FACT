# -*- coding: utf-8 -*-
"""
Created on Mon Jun 14 08:52:40 2021

"""

import re
import math
from anotator import Anotator
from anotator import basic_word_search
import numpy as np
from sympy.ntheory import isprime

def bounded_1(data_dict):
    if data_dict["value_list"] is not None:
        max_value = max(map(abs,data_dict["value_list"]))
        if max_value <= 1:
            return 1
        return 0
    return 4

def bounded_10(data_dict):
    if data_dict["value_list"] is not None:
        max_value = max(map(abs,data_dict["value_list"]))
        if max_value <= 10:
            return 1
        return 0
    return 4

def bounded_100(data_dict):
    if data_dict["value_list"] is not None:
        max_value = max(map(abs,data_dict["value_list"]))
        if max_value <= 100:
            return 1
        return 0
    return 4

def only_even(data_dict):
    if data_dict["value_list"] is not None:
        if np.count_nonzero(list(map(lambda x: (x%2), data_dict["value_list"]))) == 0:
            return 1
        return 0
    return 4

def only_odd(data_dict):
    if data_dict["value_list"] is not None:
        if np.count_nonzero(list(map(lambda x: (x%2)-1, data_dict["value_list"]))) == 0:
            return 1
        return 0
    return 4

def single_test_0_1_anotator(results):
    if results[0] == 1:
        return 4
    return 0


def increasing(data_dict):
    if data_dict["value_list"] is not None:
        prev = data_dict["value_list"][0]
        for num in data_dict["value_list"][1:]:
            if num < prev:
                return 0
            prev = num
        return 1
    return 4

def monotonically_increasing(data_dict):
    if data_dict["value_list"] is not None:
        prev = data_dict["value_list"][0]
        for num in data_dict["value_list"][1:]:
            if num <= prev:
                return 0
            prev = num
        return 1
    return 4

def decreasing(data_dict):
    if data_dict["value_list"] is not None:
        prev = data_dict["value_list"][0]
        for num in data_dict["value_list"][1:]:
            if num > prev:
                return 0
            prev = num
        return 1
    return 4

def monotonically_decreasing(data_dict):
    if data_dict["value_list"] is not None:
        prev = data_dict["value_list"][0]
        for num in data_dict["value_list"][1:]:
            if num >= prev:
                return 0
            prev = num
        return 1
    return 4

def unique_elements(data_dict):
    if data_dict["value_list"] is not None:
        if len(data_dict["value_list"]) == len(set(data_dict["value_list"])):
            return 1
        return 0
    return 4

def only_pos_composite(data_dict):
    if data_dict["value_list"] is not None:
        limit = math.pow(2,64)
        for num in data_dict["value_list"]:
            if num <= 0:
                return 3
            if num > limit:
                return 2
            if isprime(num) or num == 1:
                return 0
        return 1
    return 4

def only_pos_non_prime(data_dict):
    if data_dict["value_list"] is not None:
        limit = math.pow(2,64)
        for num in data_dict["value_list"]:
            if num <= 0:
                return 3
            if num > limit:
                return 2
            if isprime(num):
                return 0
        return 1
    return 4

def prime_and_composite_aggregator(results):
    if results[0] == 1:
        return 4
    if results[0] == 2:
        return 2
    return 0

def non_negative_elements(data_dict):
    if data_dict["value_list"] is not None:
        if np.count_nonzero(data_dict["value_list"] < 0) == 0:
            return 1
        return 0

    return 4

def non_negative_keyword(data_dict):
    if data_dict["keywords"] is not None:
        if "nonn" in data_dict["keywords"]:
            return 1
        return 0
    return 4

def positive_elements(data_dict):
    if data_dict["value_list"] is not None:
        if np.count_nonzero(data_dict["value_list"] <= 0) == 0:
            return 1
        return 0

    return 4

def non_negative_aggregator(results):
    if results[0] == 1 and results[1] == 1:
        return 4
    if results[0] + results[1] == 1:
        return 2
    return 0

def modulo(data_dict):
    return basic_word_search(data_dict, ["modulo", "mod ", "mod.", "mod,"], "name")

def modulo_regex(data_dict):
    if data_dict["name"] is not None:
        p = re.compile(r"(?:modulo|mod) (n|\d+)")
        m = p.search(data_dict["name"].lower())

        if m:
            if m.group(1) == "n":
                return 1
            return 2
        return 0
    return 4

def modulo_agreggator(results):
    if results[0] == 1:
        if results[1] == 1 or results[1] == 2:
            return 4
        return 3
    return 0

def modulo_n_agreggator(results):
    if results[0] == 1 and results[1] == 1:
            return 4
    if results[0] == 1:
        return 1
    return 0


def trigonometry_regex(data_dict):
    r0 = 0
    if data_dict["formulas"] is not None:
        p = re.compile(r"[^a-zA-Z]+(cos|sin|tan|cot|sec|csc)[^a-zA-Z]+")
        m = p.search(data_dict["formulas"].lower())

        if m:
            r0 = 1
    else:
        r0 = 4

    r1 = 0
    if data_dict["name"] is not None:
        p = re.compile(r"[^a-zA-Z]+(cos|sin|tan|cot|sec|csc|cosine|sine|tangent|cosecant|secant|cotangent)[^a-zA-Z]+")
        m = p.search(data_dict["name"].lower())

        if m:
            r1 = 1
    else:
        r1 = 4

    return [r0,r1]

def trigonometry_agreggator(result):
    if result[0][1] == 1:
        return 4
    if result[0][0] == 1:
        return 3
    return 0

def inverse_cyclotomic(data_dict):
    if data_dict["name"] is not None:
        p = re.compile(r"inverse of \d+(st|th|nd) cyclotomic polynomial")
        m = p.search(data_dict["name"].lower())

        if m:
            return 1
        return 0
    return 4

def cyclotomic_name(data_dict):
    return basic_word_search(data_dict, ["cyclotomic"], "name")

def cyclotomic_comments(data_dict):
    return basic_word_search(data_dict, ["cyclotomic"], "comments")

def cyclotomic_programs(data_dict):
    r0 = basic_word_search(data_dict, ["cyclotomic"], "maple_programs")
    r1 = basic_word_search(data_dict, ["cyclotomic"], "mathematica_programs")
    r2 = basic_word_search(data_dict, ["cyclotomic"], "other_programs")

    if 1 in [r0,r1,r2]:
        return 1
    return 0

def cyclotomic_agreggator(results):
    if results[0] == 1:
        return 4
    if results[1] == 1 and results[2] == 1:
        return 3
    if results[1] == 1 or results[2] == 1:
        return 2
    return 0


def main():
    b1_anotator = Anotator("bounded_by_1", bounded_1, single_test_0_1_anotator)
    b10_anotator = Anotator("bounded_by_10", bounded_10, single_test_0_1_anotator)
    b100_anotator = Anotator("bounded_by_100", bounded_100, single_test_0_1_anotator)

    even_anotator = Anotator("only_even_elements", only_even, single_test_0_1_anotator)
    odd_anotator = Anotator("only_odd_elements", only_odd, single_test_0_1_anotator)

    b1_anotator.run_and_save()
    b10_anotator.run_and_save()
    b100_anotator.run_and_save()

    even_anotator.run_and_save()
    odd_anotator.run_and_save()

def main2():
    inc_anotator = Anotator("increasing", increasing, single_test_0_1_anotator)
    mon_inc_anotator = Anotator("strict_monotonically_increasing", monotonically_increasing, single_test_0_1_anotator)
    dec_anotator = Anotator("decreasing", decreasing, single_test_0_1_anotator)
    mon_dec_anotator = Anotator("stric_monotonically_decreasing", monotonically_decreasing, single_test_0_1_anotator)

    unique_element_anotator = Anotator("contains_only_unique_elements",unique_elements , single_test_0_1_anotator)

    only_pos_composite_anotator = Anotator("contains_only_positive_composite_numers", only_pos_composite, prime_and_composite_aggregator)
    only_pos_non_prime_anotator = Anotator("contains_only_positive_non_prime_numers", only_pos_non_prime, prime_and_composite_aggregator)

    inc_anotator.run_and_save()
    mon_inc_anotator.run_and_save()
    dec_anotator.run_and_save()
    mon_dec_anotator.run_and_save()

    unique_element_anotator.run_and_save()

    only_pos_composite_anotator.run_and_save()
    only_pos_non_prime_anotator.run_and_save()

def main3():
    non_negative_anotator = Anotator("non_negative_numbers", [non_negative_elements, non_negative_keyword], non_negative_aggregator)
    positive_anotator = Anotator("non_negative_numbers", [positive_elements, non_negative_keyword], non_negative_aggregator)

    mod_anotator = Anotator("using_modulo", [modulo, modulo_regex], modulo_agreggator)
    mod_n_anotator = Anotator("modulo_n", [modulo, modulo_regex], modulo_n_agreggator)

    non_negative_anotator.run_and_save()
    positive_anotator.run_and_save()

    mod_anotator.run_and_save()
    mod_n_anotator.run_and_save()


def main4():
    trig_anotator = Anotator("using_trigonometric_functions", trigonometry_regex, trigonometry_agreggator)

    cyclotomic_anotator = Anotator("cyclotomic", [cyclotomic_name,cyclotomic_comments,cyclotomic_programs], cyclotomic_agreggator)
    inverse_cyclotomic_anotator = Anotator("inverse_-number-_cyclotomic_polynomial", inverse_cyclotomic, single_test_0_1_anotator)

    trig_anotator.run_and_save()

    cyclotomic_anotator.run_and_save()
    inverse_cyclotomic_anotator.run_and_save()


def main5():
    trig_anotator = Anotator("using_trigonometric_functions", trigonometry_regex, trigonometry_agreggator)
    inverse_cyclotomic_anotator = Anotator("inverse_-number-_cyclotomic_polynomial", inverse_cyclotomic, single_test_0_1_anotator)
    mod_anotator = Anotator("using_modulo", [modulo, modulo_regex], modulo_agreggator)
    mod_n_anotator = Anotator("modulo_n", [modulo, modulo_regex], modulo_n_agreggator)


    trig_anotator.run_and_save()
    inverse_cyclotomic_anotator.run_and_save()
    mod_anotator.run_and_save()
    mod_n_anotator.run_and_save()
