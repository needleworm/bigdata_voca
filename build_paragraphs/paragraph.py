"""
Author : Byunghyun Ban
Email : bhban@kakao.com
"""

import utils as U
import os
import time
import build_word_list as B


def build_paragraph(source_dir):
    word_list = B.build_word_list(source_dir)
    out_filename = source_dir + ".txt"
    out_dir = "out_" + source_dir 
    error_word = "errored_words.txt"

    if out_dir not in os.listdir():
        os.mkdir(out_dir)

    target_files = []
    files = os.listdir("./" + source_dir)

    for el in files:
        if el.endswith(".txt"):
            target_files.append(source_dir + "/" + el)

    target_files.sort()


    for el in target_files:
        f = open("./" + el, encoding="utf-8-sig")
        print("reading " + el)
        text = f.read()
        f.close()
        pages = text.split("________________")
        brk = False

        for page in pages:
            lines = page.split("\n")

            brk = False
            empty_page = True
            for line in lines:
                line = line.strip()
                if len(line) == 0:
                    continue
                else:
                    empty_page = False
                
                    words = line.split(" ")

                    if len(words) == 1 and line.encode().isalpha():
                        word = words[0].lower()
                        if word + ".txt" in os.listdir(out_dir):
                            brk = True
                            break
                        else:
                            print("processing " + word + ".....")
                            break
                
            if brk or empty_page:
                continue

            one_page = one_word_content(word, lines)
            if len(one_page) > 0:
                out_file_word = open(out_dir + "/" + word + ".txt", 'w', encoding="utf-8-sig")
                out_file_word.write(one_page)
                out_file_word.close()
            else:
                print("passing " + word)
                err_file = open(error_word, "a", encoding="utf-8-sig")
                err_file.write(page)
                err_file.write("________________\n")
                err_file.close()

    result = open(out_filename, "w", encoding="utf-8-sig")
    result.close()
    qqq = open("extracted_words.txt", "w", encoding="utf8")
    extracted_words = []

    for file in os.listdir(out_dir):
        if file.endswith(".txt"):
            word = file.split(".")[0]
            qqq.write(word + "\n")
            extracted_words.append(word)
            result = open(out_filename, "a", encoding="utf-8-sig")
            q = open(out_dir + "/" + file, encoding="utf-8-sig")
            result.write(q.read())
            q.close()
            result.close()
    qqq.close()

    www = open("sentence_sources_word_list.txt", encoding="utf-8").read().split("\n")

    eee = open("unextracted_words.txt", "w", encoding="utf-8")
    for el in www:
        if el not in extracted_words:
            eee.write(el + "\n")
    
    eee.close()



def one_word_content(word, lines):
    one_page = word + "\n\n"

    # word, entry_info, pronounciation, meaning
    try:
        _, entry_info, pronounciation, meaning = U.get_single_word(word)
    except:
        print("---- " + word + " crawling failed! retry!")
        time.sleep(3)
        try:
            _, entry_info, pronounciation, meaning = U.get_single_word(word)
        except:
            print("---- " + word + " crawling failed! Passing!")
            return ""
    
    if "Verb" in entry_info:
        entry_info = entry_info[entry_info.index("Verb"):]
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

    # sample sentence extraction
    sentence_text = ""

    for line in lines:
        qqq = line.strip().split(" ")
        if len(qqq[0]) == 0:
            continue
        if len(qqq) == 1:
            continue
        elif len(qqq) < 4:
            sentence_text += "\n" + line.strip() + "\n"

        elif U.isKorean(qqq[-2]):
            continue

        else:
            sentence_text += line.strip() + "\n"
            translation = U.translate(line.strip())
            if not translation:
                print("Translation Failed!! --- " + word)
                return ""
            sentence_text += translation + "\n"
    
    if len(sentence_text) > 4:
        one_page += sentence_text
        one_page += "\n\n-----\n\n"

        return one_page

    else:
        print("Sample Sentence Processing Failed!! --- " + word)
        return ""
