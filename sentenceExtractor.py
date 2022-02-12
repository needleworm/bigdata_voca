"""
Author : Byunghyun Ban
Email : bhban@kakao.com
"""

import os
import re


def save_sentences(wordFile, resource_dir):
    dct = find_sentences_with_word(wordFile, resource_dir)
    new_dir_name = resource_dir + "_sentence_Extracted"
    if new_dir_name not in os.listdir():
        os.mkdir(new_dir_name)

    words = dct.keys()
    for word in words:
        new_filename = new_dir_name + "/" + word + ".txt"
        new_file = open(new_filename, "w", encoding="utf8")

        sentences = dct[word]

        for el in sentences:
            sentence, source = el
            new_file.write(sentence + ", " + source + "\n")

        new_file.close()

    print("done")


def find_sentences_with_word(wordFile, resource_dir):
    dct = sentence_extractor(resource_dir)
    print("sentence separation done")
    resources = dct.keys()
    txt = open(wordFile)
    count = 0
    retDct = {}
    for line in txt:
        if count == 100:
            return retDct
        word = line.strip().split(",")[0]
        sentences = []

        for key in resources:
            db = dct[key]
            for el in db:
                if word in el:
                    sentences.append((el, key))

        if len(sentences) != 0:
            retDct[word] = sentences
            count += 1

    print(retDct)
    print("Processing Done. Ready to write result file")
    return retDct


def sentence_extractor(resource_dir):
    resource = os.listdir(resource_dir)
    dct = {}
    for el in resource:
        filename = resource_dir + "/" + el
        file = open(filename, encoding="utf8")

        text = file.read()
        file.close()

        sentences = process(text)

        dct[el.split(".")[0]] = sentences

    return dct


def process(txt):
    concatenate = [
        "\n", "\t", "\\n", "  "
    ]

    for el in concatenate:
        while el in txt:
            txt = txt.replace(el, " ")

    banList = [
        "→", "~", "*", "@", "#",
        "①", "②", "③", "④", "⑤",
        "!", "?", ".", "'", '"', '”', "'", '“', "━"
    ]

    for el in banList:
        txt = txt.replace(el, ".")

    splt = txt.split(".")

    temp = []
    for el in splt:
        el = el.strip()
        if len(el) < 7:
            continue
        elif len(el.split(" ")) < 5:
            continue
        elif isKorean(el) != 0:
            continue
        else:
            temp.append(el)

    return temp


def isKorean(text):
    hangul = re.compile('[\u3131-\u3163\uac00-\ud7a3]+')
    result = hangul.findall(text)
    return len(result)


dct = save_sentences("merged_result.csv", "resource")
