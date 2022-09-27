"""
Author : Byunghyun Ban
Email : bhban@kakao.com
"""

import os
import pymacro as pc
import time
import sys

resource_dir = sys.argv[1].strip()
alpha = sys.argv[2].strip()


def write_wordfiles(alphabet, resource_dir):
    wordfiles = os.listdir(resource_dir)
    for el in wordfiles:
        if el.startswith(alphabet):
            word = el.split(".")[0]
            f = open(resource_dir + "/" + el, encoding="utf8")
            content = f.read()
            f.close()

            docs_write_content(word, content)


def docs_write_content(title, body):
    sleepInterval = 0.2
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

write_wordfiles(alpha, resource_dir)
