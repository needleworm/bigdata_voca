"""
Author : Byunghyun Ban
Email : bhban@kakao.com
"""

from pdfminer.high_level import extract_text
import os


def extract_texts(directory):
    txt = ""

    new_dir = directory + "_extracted"
    if new_dir not in os.listdir():
        os.mkdir(new_dir)

    for el in os.listdir(directory):
        if el.endswith(".pdf"):
            extracted_text = extract_text(directory + "/" + el)
            tmp = open(new_dir + "/" + el.split(".")[0] + ".txt", "w", encoding="utf8")
            tmp.write(extracted_text)
            tmp.close()
            txt += extracted_text
            print("> " + el + " has processed...")
