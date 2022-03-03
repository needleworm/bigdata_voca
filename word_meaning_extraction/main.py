"""
Author : Byunghyun Ban
Email : bhban@kakao.com
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
import time


opt = webdriver.ChromeOptions()

driver = webdriver.Chrome("chromedriver", chrome_options=opt)

baseurl = "https://en.dict.naver.com/#/search?range=word&query="


def get_single_word(word):
    search_word(word)
    time.sleep(2)
    entry_info = get_entry_infos()
    pronounciation = get_pronounciation()
    meaning = get_meaning()

    return word, entry_info, pronounciation, meaning


def search_word(word):
    driver.get(baseurl + word)
    row = driver.find_elements(By.CLASS_NAME, "row")[0]
    row.find_element(By.CLASS_NAME, "link").click()


def get_entry_infos():
    entry_info = driver.find_element(By.CLASS_NAME, "entry_infos").text
    return entry_info.split("\n")


def get_pronounciation():
    entry_pronounce = driver.find_element(By.CLASS_NAME, "entry_pronounce").text
    splt = entry_pronounce.split("\n")
    ret = ["발음"]
    for line in splt:
        if "[" in line:
            ret.append(line.strip())
    return ret


def get_meaning():
    mean_tray = driver.find_element(By.CLASS_NAME, "mean_tray").text
    splt = mean_tray.split("\n")
    ret = []

    for idx, line in enumerate(splt):
        q = line.split(".")[0]
        if q.isdigit():
            if line.startswith("1."):
                ret.append(splt[idx-1])
            if "상호참조" in splt[idx+1]:
                continue
            else:
                w = line.split(".")
                if len(w) < 2:
                    continue
                w = w[1].strip()
                if w[0].encode().isalpha():
                    print(splt[idx+1])
                    newLine = splt[idx+1].strip()
                else:
                    print(w)
                    newLine = w
            
                ret.append(newLine)

    return ret


