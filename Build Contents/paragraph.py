"""
Author : Byunghyun Ban
Email : bhban@kakao.com
"""

import utils as U
import os
import time


def build_paragraph(source_dir):
    out_filename = source_dir + ".txt"
    out_dir = "out_" + source_dir 

    if out_dir not in os.listdir():
        os.mkdir(out_dir)

    target_files = []
    files = os.listdir(source_dir)

    for el in files:
        if el.endswith(".txt"):
            target_files.append(source_dir + "/" + el)
            print(el + " detected")


    target_files.sort()

    for el in target_files:
        f = open(el, encoding="utf-8-sig")
        print("reading " + el)
        text = f.read()
        pages = text.split("________________")

        for page in pages:
            lines = page.split("\n")
            one_page = ""
            brk = False

            for line in lines:
                if brk:
                    break

                line = line.strip()
                if len(line) == 0:
                    continue
                
                words = line.split(" ")

                if len(words) == 1 and line.encode().isalpha():
                    word = line.lower()
                    if word + ".txt" in os.listdir(out_dir):
                        brk = True
                        continue
                    print("processing " + word + ".....")
                    one_page += word + "\n\n"

                    # word, entry_info, pronounciation, meaning
                    try:
                        _, entry_info, pronounciation, meaning = U.get_single_word(word)
                    except IndexError:
                        time.sleep(3)
                        try:
                            _, entry_info, pronounciation, meaning = U.get_single_word(word)
                        except:
                            brk = True
                            continue
                    
                    if entry_info[0]:
                        info = "동사 활용형\n"
                        ln = entry_info[1]
                        ln2 = ln.replace("3rd Person Singular Present Tense ", "")
                        ln3 = ln2.replace(" Past Tense ", ",")
                        ln4 = ln3.replace(" Present Participle ", ",")
                        ln5 = ln4.replace(" Past Participle ", ",")
                        splt_ln = ln5.split(",")
                        info += "3SP: " + splt_ln[0] + "\n"
                        info += "P: " + splt_ln[1] + "\n"
                        info += "PP: " + splt_ln[2] + "\n"
                        info += "ing: " + splt_ln[3] + "\n"
                        one_page += info + "\n"

                    one_page += pronounciation[0].strip() + "\n"
                    pronounciation = pronounciation[1:]
                    for pron in pronounciation:
                        sp_p = pron.replace("ˈ", "").split("[")
                        category = sp_p[0].strip()
                        ln_p = sp_p[1].strip()
                        ln_p = ln_p.replace(";", "")
                        sp_p2 = ln_p.split(" ")
                        prn = sp_p2[0]
                        if "Pronunciation " in category:
                            one_page += prn + "\n"
                            break
                        else:
                            one_page += category + ": " + prn + "\n"
                    one_page += "\n"

                    meaning_txt = ""
                    count = 1
                    for mean in meaning:
                        tst = mean.replace("(", "")
                        tst = tst.replace(")", "")
                        tst = tst.replace("[", "")
                        tst = tst.replace("]", "")
                        tst = tst.replace("/", "")
                        tst = tst.replace("'", "")
                        tst = tst.replace("'", "")
                        tst = tst.replace("  ", "")
                        tst = tst.replace(" ", "")
                        if tst.encode().isalpha():
                            meaning_txt += mean + "\n"
                            count = 1
                        else:
                            meaning_txt += str(count) + ". " + mean + "\n"
                            count += 1
                    one_page += meaning_txt + "\n"

                else:
                    qqq = line.split(" ")
                    if len(qqq) < 4:
                        one_page += "\n" + line.strip() + "\n"

                    elif U.isKorean(qqq[-2]):
                        continue

                    else:
                        one_page += line.strip() + "\n"
                        translation = U.translate(line.strip())
                        one_page += translation + "\n"

            one_page += "\n\n-----\n\n"
            
            out_file_word = open(out_dir + "/" + word + ".txt", 'w')
            out_file_word.write(one_page)
            out_file_word.close()

            if brk: 
                continue

    result = open(out_filename, "w")
    
    for file in os.listdir(out_dir):
        q = open(out_dir + "/" + file)
        result += q.read()
        q.close()
    result.close()
