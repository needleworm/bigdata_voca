"""
Author : Byunghyun Ban
Email : bhban@kakao.com
"""

import sys

a = sys.argv[1]
b = sys.argv[2]


def save_to_csv():
    dct = merge_result()
    key = list(dct.keys())
    key.sort()
    res = open("merged_result.csv", "w", encoding="utf-8")
    res.write("WORD, SUNUNG, PGW\n")
    for el in key:
        res.write(el + ", ")
        res.write(dct[el]["sunung"] + ", ")
        res.write(dct[el]["pgw"] + "\n")
    res.close()


def csv_to_dict(f):
    q = open(f)
    dct = {}
    q.readline()
    for line in q:
        splt = line.strip().split(",")
        dct[splt[0]] = splt[-1].strip()

    q.close()

    return dct


def merge_result():
    dct1 = csv_to_dict(a)
    dct2 = csv_to_dict(b)
    res = {}

    for el in dct1.keys():
        res[el] = {}
        res[el]["sunung"] = dct1[el]
        res[el]["pgw"] = "0"

    for el in dct2.keys():
        if el not in res:
            res[el] = {}
            res[el]["sunung"] = "0"
            res[el]["pgw"] = dct2[el]
        else:
            res[el]["pgw"] = dct2[el]

    return res

save_to_csv()

print("done!")