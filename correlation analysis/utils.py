"""
Author : Byunghyun Ban
Email : bhban@kakao.com
"""

import time
import re


def is_korean(text):
    hangul = re.compile('[\u3131-\u3163\uac00-\ud7a3]+')
    result = hangul.findall(text)
    return bool(len(result))


def only_eng(text):
    if not text.isalpha():
        return False
    hangul = re.compile('[\u3131-\u3163\uac00-\ud7a3]+')
    result = bool(len(hangul.findall(text)))
    return not result
