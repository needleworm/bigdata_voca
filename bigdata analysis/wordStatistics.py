"""
Author : Byunghyun Ban
Email : bhban@kakao.com
"""

import os


def get_statistics(directory):
    dct, tests = get_statistics_txt(directory)
    tests.append("sum")
    keys = list(dct.keys())
    keys.sort()

    result = open(directory.split("_")[0] + "_statistics.csv", "w")

    header = ", ".join(tests)
    result.write("WORDS, " + header + "\n")

    for el in keys:
        lineList = [el]
        for tst in tests:
            lineList.append(str(dct[el][tst]))

        line = ", ".join(lineList)
        result.write(line + "\n")

    result.close()


def get_statistics_txt(directory):
    single_dicts = get_dictionaries(directory)
    keys = single_dicts.keys()

    merged_dict = {}

    for el in keys:
        dct = single_dicts[el]
        for word in dct.keys():
            if word not in merged_dict:
                merged_dict[word] = {}
                merged_dict[word]["sum"] = 0
            merged_dict[word][el.split(".")[0]] = dct[word]
            merged_dict[word]["sum"] += dct[word]

    tests = []
    for el in os.listdir(directory):
        if el.endswith(".txt"):
            tests.append(el.split(".")[0])

    for el in merged_dict.keys():
        for test in tests:
            if test not in merged_dict[el]:
                merged_dict[el][test] = 0
    tests.sort()
    return merged_dict, tests


def get_dictionaries(directory):
    single_dicts = {}
    for el in os.listdir(directory):
        if el.endswith(".txt"):
            f = open(directory + "/" + el, encoding="utf8")
            txt = f.read()
            f.close()
            splt = process(txt)
            dct = statistics(splt)
            single_dicts[el] = dct

    return single_dicts


def statistics(splt):
    dct = {}
    for el in splt:
        if el not in dct:
            dct[el] = 1
        else:
            dct[el] += 1

    return dct


def process(txt):
    banList = [
        "\n", "\t", ",", ".", "’", "'", '"', "-", "—", "$", "(", ")", "[",
        "]", "{", "}", "!", "?", "의", "이", "가", "는", "은", "에게", "→",
        "”", "~", "1", "2", "3", "4", "5", "6", "7", "8", "9", "0",
        "*", ":", "@", "/", "‘", "\\n"
    ]

    for el in banList:
        txt = txt.replace(el, " ")

    splt = txt.split(" ")

    temp = []
    for el in splt:
        if el.encode().isalpha():
            temp.append(el.lower())

    return temp

