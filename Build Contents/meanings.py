"""
Author : Byunghyun Ban
Email : bhban@kakao.com
"""

import utils as U
import time
import pyexcel as px
import os
import random


def add_line_to_xlsx(filename, line):
    data_array = px.get_array(file_name=filename)
    data_array.append(line)
    px.save_as(array=data_array, dest_file_name=filename)


def build_contents(filename):
    out_filename = "out_" + filename
    data_array = px.get_array(file_name=filename)
    header = data_array[0]
    data_array = data_array[1:]
    random.shuffle(data_array)

    errored_filename = "ERROR_" + filename.split(".")[0] + '.txt'

    header += ["발음기호", "품사", "의미"]

    if out_filename not in os.listdir():
        data_array = [header]
        px.save_as(array=data_array, dest_file_name=out_filename)

    if errored_filename not in os.listdir():
        error_file = open(errored_filename, 'w', encoding="utf8")
        error_file.write("에러 발생한 단어")
        error_file.close()

    processed_file = px.get_array(file_name=out_filename)

    processed_words = []
    for line in processed_file:
        word = line[0]
        processed_words.append(word)

    for line in data_array:
        word = line[0]
        if word in processed_words:
            continue

        print("Processing " + word + "... ")

        try:
            _, _, pron, meaning = U.get_single_word(word)
        except:
            time.sleep(2)
            try:
                _, _, pron, meaning = U.get_single_word(word)
            except:
                print(" Error!")
                error_file = open(errored_filename, 'a')
                error_file.write("\n" + word)
                error_file.close()
                continue
        try:
            pron = pron[1][pron[1].index("[") + 1: pron[1].index("]")].strip()
            if ";" in pron:
                pron = pron[:pron.index(";")]
            pron = "[" + pron + "]"
        except:
            pron = "-1"

        if not meaning:
            error_file = open(errored_filename, 'a', encoding="utf8")
            error_file.write(word)
            error_file.close()

        for el in meaning:
            line_copy = line + [pron, el[0], el[1]]
            add_line_to_xlsx(out_filename, line_copy)
            print("\t\t" + str(line_copy))

        processed_words.append(word)
