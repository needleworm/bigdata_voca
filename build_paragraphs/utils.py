"""
Author : Byunghyun Ban
Email : bhban@kakao.com
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import urllib.request
import requests
import json
import re
from googletrans import Translator as T


translator = T()

opt = webdriver.ChromeOptions()
opt.add_argument("headless")

driver = webdriver.Chrome("./chromedriver", chrome_options=opt)

baseurl = "https://en.dict.naver.com/#/search?range=word&query="


def get_single_word(word):
    search_word(word)
    entry_info = get_entry_infos()
    pronounciation = get_pronounciation()
    meaning = get_meaning()

    return word, entry_info, pronounciation, meaning


def search_word(word):
    driver.get(baseurl + word)
    time.sleep(3)
    row = driver.find_elements(By.CLASS_NAME, "row")[0]
    row.find_element(By.CLASS_NAME, "link").click()


def get_entry_infos():
    try:
        entry_info = driver.find_element(By.CLASS_NAME, "entry_infos").text
    except:
        time.sleep(3)
        try:
            entry_info = driver.find_element(By.CLASS_NAME, "entry_infos").text
        except:
            entry_info = ""
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
        if q.isdigit() and idx < len(splt) -1 :
            if line.startswith("1."):
                ret.append(splt[idx-1])
            if "상호참조" in splt[idx + 1]:
                continue
            else:
                w = line.split(".")
                if len(w) < 2:
                    continue
                w = w[1].strip()
                nextline = splt[idx+1].strip()
                if isKorean(nextline):
                    ret.append(nextline.split(".")[-1])
                elif isKorean(splt[idx].strip().split(".")[-1]):
                    ret.append(splt[idx].strip().split(".")[-1])

                """
                if w[0].encode().isalpha():
                    newLine = splt[idx+1].strip()
                else:
                    newLine = w
                """

    return ret



def translate(sentence):
    time.sleep(1)
    try:
        return kakao_translate(sentence)
    except:
        try:
            return google_translate(sentence)
        except:
            try:
                return papago_translate(sentence)
            except:
                return False



def google_translate(sentence):
    return translator.translate(sentence, src="en", dest="ko").text


def papago_translate(sentence):
    client_id = "YOUR CLIENT ID"
    client_ps = "YOUR CLIENT SECRET CODE"
    encText = urllib.parse.quote(sentence)
    data = "source=en&target=ko&text=" + encText
    url = "https://openapi.naver.com/v1/papago/n2mt"
    request = urllib.request.Request(url)
    request.add_header("X-Naver-Client-Id",client_id)
    request.add_header("X-Naver-Client-Secret",client_ps)
    request.add_header('User-agent', 'Mozilla/5.0')
    response = urllib.request.urlopen(request, data=data.encode("utf-8"))
    rescode = response.getcode()
    if(rescode==200):
        response_body = response.read()
        response = json.loads(response_body.decode('utf-8'))
        return str(response["message"]["result"]["translatedText"])

    else:
        print("Error Code:" + rescode)
        return ""

def kakao_translate(sentence):
    url = "https://translate.kakao.com/translator/translate.json"
    headers = {
        "Referer": "https://translate.kakao.com/",
        "User-Agent": "Mozilla/5.0"
    }
    data = {
        "queryLanguage": "en",
        "resultLanguage": "kr",
        "q": sentence
    }

    resp = requests.post(url, headers=headers, data=data)
    data = resp.json()
    output = data['result']['output'][0][0]
    return output



def isKorean(text):
    hangul = re.compile('[\u3131-\u3163\uac00-\ud7a3]+')
    result = hangul.findall(text)
    return len(result)
