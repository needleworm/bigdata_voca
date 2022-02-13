"""
Author : Byunghyun Ban
Email : bhban@kakao.com
"""

import os
import re
import googletrans
import pymacro as pc
import time


def find_sentences_with_word(wordFile, resource_dir):
    dct = sentence_extractor(resource_dir)
    print("sentence separation done")
    resources = dct.keys()
    txt = open(wordFile)
    banList = [
        "\n", "\t", ",", ".", "’", "'", '"', "-", "—", "$", "(", ")", "[",
        "]", "{", "}", "!", "?", "의", "이", "가", "는", "은", "에게", "→",
        "”", "~", "1", "2", "3", "4", "5", "6", "7", "8", "9", "0",
        "*", ":", "@", "/", "‘", "\\n"
    ]

    new_dir_name = resource_dir + "_sentence_Extracted_Translated"
    if new_dir_name not in os.listdir():
        os.mkdir(new_dir_name)

    translator = googletrans.Translator()

    for line in txt:
        word = line.strip().split(",")[0]
        sentences = []

        for key in resources:
            db = dct[key]
            for el in db:
                for bn in banList:
                    tmp_line = el.replace(bn, " ")
                words_in_sentence = tmp_line.split(" ")
                if word in words_in_sentence:
                    sentences.append((el, key))

        if len(sentences) != 0:
            new_filename = new_dir_name + "/" + word + ".txt"
            new_file = open(new_filename, "w", encoding="utf8")

            body = ""

            for el in sentences:
                sentence, source = el
                body += source + "\n"
                body += sentence + "\n"
                #transalted_sentence = translator.translate(text=sentence, dest="ko")
                #time.sleep(0.1)
                #body += transalted_sentence.text + "\n"
                body += "\n"

            new_file.write(body)
            new_file.close()

            #google_docs_write_content(word, body)

            print("Report Saved > " + word)


def google_docs_write_content(title, body):
    sleepInterval = 0.5
    pc.click((4880, 2294))
    time.sleep(sleepInterval)
    ctrl_B()
    time.sleep(sleepInterval)
    pc.type_in(title)
    ctrl_B()
    time.sleep(sleepInterval)
    pc.key_press_once("enter")
    time.sleep(sleepInterval)
    pc.type_in(body)
    time.sleep(sleepInterval)
    ctrl_enter()


def ctrl_enter():
    # Ctrl을 누릅니다.
    pc.key_on("control")
    # c도 누릅니다.
    pc.key_on("enter")
    # 두 키를 모두 뗍니다.
    pc.key_off("control")
    pc.key_off("enter")


def ctrl_B():
    # Ctrl을 누릅니다.
    pc.key_on("control")
    # c도 누릅니다.
    pc.key_on("b")
    # 두 키를 모두 뗍니다.
    pc.key_off("control")
    pc.key_off("b")


def sentence_extractor(resource_dir):
    resource = os.listdir(resource_dir)
    dct = {}
    for el in resource:
        filename = resource_dir + "/" + el
        print("reading  > " + filename)
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
        "→", "~", "*", "@", "#", "_",
        "①", "②", "③", "④", "⑤",
        "!", "?", ".", '"', '”', '“',
        "━", "", "■", "∙"
    ]

    for el in banList:
        txt = txt.replace(el, ".")

    splt = txt.split(".")

    ban_this_contents = [
        "§",
        "(a)", "(b)", "(c)", "(d)", "(e)",
        "(A)", "(B)", "(C)", "(D)", "(E)",
        "(1)", "(2)", "(3)", "(4)", "(5)",
        "(i)", "(ii)", "(iii)", "(iv)", "(v)",
        "gov/about/", "http", "reCAPTCHA", "--"

    ]

    stripList = [
        "B ", "s ", "C ", "A ", "D ", "E "
        "III ", "II", "IV ", "V ", "13 IV",
        ", ", "- "
        "(a)", "(b)", "(c)", "(d)", "(e)",
        "(A)", "(B)", "(C)", "(D)", "(E)",
        "(1)", "(2)", "(3)", "(4)", "(5)",
        "(i)", "(ii)", "(iii)", "(iv)", "(v)",
        "§",
        ")", "c)"
    ]

    temp = []
    for el in splt:
        el = el.strip()
        for strp in stripList:
            if el.startswith(strp):
                el = el[len(strp) -1:]

        for cnt in ban_this_contents:
            if cnt in el:
                el = ""
                break

        if len(el) < 7:
            continue
        elif len(el.split(" ")) < 5:
            continue
        elif len(el.split(" ")) > 21:
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


#dct = save_sentences("survived words.txt", "resource")

find_sentences_with_word("survived words.txt", "resource")
