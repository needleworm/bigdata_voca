"""
Author : Byunghyun Ban
Email : bhban@kakao.com
"""

import txtExtractor as TE
import wordStatistics as WS
import sys

directory = sys.argv[1]

TE.extract_texts(directory)

WS.get_statistics(directory + "_extracted")
