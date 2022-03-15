"""
Author : Byunghyun Ban
Email : bhban@kakao.com
"""

import os


def build_word_list(source_dir):
    out_filename = source_dir + "_word_list.txt"

    target_files = []
    files = os.listdir(source_dir)

    for el in files:
        if el.endswith(".txt"):
            target_files.append(source_dir + "/" + el)


    target_files.sort()
    word_list = []

    for el in target_files:
        f = open(el, encoding="utf-8-sig")
        text = f.read()
        pages = text.split("________________")

        for page in pages:
            lines = page.split("\n")

            for line in lines:

                line = line.strip()
                if len(line) == 0:
                    continue
                
                words = line.split(" ")

                if len(words) == 1 and line.encode().isalpha():
                    word = line.lower()
                    if word not in word_list:
                        word_list.append(word)

    out_file = open(out_filename, "w")
    out_file.write("\n".join(word_list))
    out_file.close()

    return word_list