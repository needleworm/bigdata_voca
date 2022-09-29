"""
Author : Byunghyun Ban
Email : bhban@kakao.com
"""

import os
import pyexcel as px
import utils as U
import numpy as np
import seaborn as sns
from matplotlib import pyplot as plt

directory = "sunung"
filename = "sunung.xlsx"
dict_file = "dict.csv"


def build_correlation_matrix(filename, dict_file):
    data_array = px.get_array(file_name=filename)
    word_list = data_array[0][1:]
    word_dict = read_word_dict_from_csv(dict_file, word_list)
    sunung_txts = read_sunung_txts(directory)

    context = []
    for el in sunung_txts:
        context += el[1]

    word_list.sort()
    matrix = np.zeros((len(word_list), len(word_list)), dtype=int)

    for i in range(len(word_list)):
        print("processing " + word_list[i])
        for j in range(len(word_list)):
            if i <= j:
                continue
            for line in context:
                words_a = word_dict[word_list[i]]
                words_b = word_dict[word_list[j]]
                for word_a in words_a:
                    for word_b in words_b:
                        if word_a in line and word_b in line:
                            if word_a not in word_b and word_b not in word_a:
                                matrix[i][j] += 1

    for i in range(len(word_list)):
        for j in range(len(word_list)):
            if i == j:
                continue
            if matrix[i][j] == 0 and matrix[j][i] != 0:
                matrix[i][j] = matrix[j][i]

    for i in range(len(word_list)):
        for line in context:
            words = word_dict[word_list[i]]
            for word in words:
                if word in line.split(" "):
                    matrix[i][i] += 1

    header = ["단어"] + word_list
    contents = [header]

    for i in range(len(word_list)):
        contents.append([word_list[i]] + list(matrix[i]))

    px.save_as(array=contents, dest_file_name="인접행렬_" + filename)

    content = []

    for i in range(1300):
        line = [word_list[i]]
        cntnt = []
        for j in range(1300):
            if i == j:
                continue
            cntnt.append([matrix[i][j], word_list[j]])
        cntnt.sort()
        cntnt.reverse()

        min = 99999
        max = 0
        qqq = []
        for el in cntnt:
            num, word = el
            if not num:
                break
            if num <= 2:
                break
            if num == min:
                break
            if num < min:
                min = num
            if num > max:
                max = num
            if num < max/10:
                break
            if line[0] in word or word in line[0]:
                continue
            qqq.append(word + " (" + str(num) + "회)")

        content.append(line + qqq)

    px.save_as(array=content, dest_file_name="top.xlsx")

    temp = list[matrix]
    lst = [list(el) for el in temp]
    lst.sort()

    corr = np.corrcoef(lst)
    mask = np.zeros_like(corr)
    mask[np.triu_indices_from(mask)] = True

    with sns.axes_style("white"):
        ax = sns.heatmap(corr, mask=mask, vmax=.6, square=True, cmap="YlGnBu")
        plt.savefig("heatmap.png")
        plt.close()

    return matrix


def read_word_dict_from_csv(filename, word_list):
    ret = {}
    file = open(filename, encoding="utf8")
    for line in file:
        line = line.strip()
        if ", " not in line:
            continue
        var, origin = line.strip().split(", ")
        if origin not in word_list:
            continue
        if origin not in ret:
            ret[origin] = [var]
            if origin != var:
                ret[origin].append(origin)
        else:
            ret[origin].append(var)

    file.close()
    return ret


def read_sunung_txts(directory):
    ret = []
    for el in os.listdir(directory):
        if el.endswith(".txt"):
            test_name = el.split(".")[0]
            txt = open(directory + "/" + el)
            body = txt.read()
            txt.close()

            body = body.replace(" \n. \n", " ")
            body = body.replace(" \n, \n", " ")
            body = body.replace("\n", " ")
            body = body.replace("\U000f0802", "")
            body = body.replace("\U000f003b", "")
            body = body.replace("\x0c", " ")
            body = body.replace("\xa0", " ")
            body = body.replace("/return", "")
            body = body.replace(". ,", ",")
            body = body.replace("-", "-")
            body = body.replace("’’", "’")
            body = body.replace("I m", "I'm")
            while "  " in body:
                body = body.replace("  ", " ")

            while "__" in body:
                body = body.replace("__", "_")

            while "--" in body:
                body = body.replace("--", "-")

            while " - - " in body:
                body = body.replace(" - - ", "")

            body = body.replace("!", "!\n")
            body = body.replace(".", ".\n")
            body = body.replace("?", ".\n")
            body = body.replace(". \n,", ",")
            body = body.replace(". \n,", ",")
            body = body.replace(".\n,", ",")
            body = body.replace(".\n ,", ",")
            body = body.replace(" a.\nm.", " a.m. ")
            body = body.replace(" p.\nm.", " p.m. ")
            body = body.replace("U.\nS.\n", "U.S.")
            body = body.replace("U.\nS", "U.S")
            body = body.replace("U.\nK.\n", "U.K.")
            body = body.replace("U.\nK", "U.K")
            body = body.replace(" etc.\n", " etc.")
            body = body.replace(".\n”", ".”\n")
            body = body.replace(".\n’", ".’\n")
            body = body.replace("!\n”", "!”\n")
            body = body.replace("!\n’", "!’\n")
            body = body.replace("?\n”", "?”\n")
            body = body.replace("?\n’", "?’\n")
            body = body.replace(" .\n", ".\n")
            body = body.replace("∙", "\n")
            body = body.replace(".\n)", ".)\n")
            body = body.replace("?\n)", "?)\n")
            body = body.replace("!\n)", "!)\n")
            body = body.replace(". \n)", ".)\n")
            body = body.replace("? \n)", "?)\n")
            body = body.replace("! \n)", "!)\n")
            body = body.replace(" )", ")")
            body = body.replace("( ", "(")
            body = body.replace(", “", "\n“")
            body = body.replace(".” ", ".”\n")
            body = body.replace("(e.\ng", "(e.g")
            body = body.replace("www.\n", "www.")
            body = body.replace("www. \n", "www.")
            body = body.replace(".\nuk", ".uk")
            body = body.replace(".\norg", ".org")
            body = body.replace("fffbg.\n", "fffbg.")
            body = body.replace("fremontart.\n", "fremontart.")
            body = body.replace(".\nco.uk", ".co.uk")
            body = body.replace(",\n", ", ")
            body = body.replace(", \n", ", ")
            body = body.replace("s\nc", "s c")
            body = body.replace("chs.\n", "chs.")
            body = body.replace("CVL.\n", "CVL.")
            body = body.replace("hyo.\n", "hyo.")
            body = body.replace("naturefoundation.\n", "naturefoundation.")
            body = body.replace(".\ncom", ".com")
            body = body.replace("’\n”", "’”\n")
            body = body.replace("”\n’", "”’\n")
            body = body.replace(
                "(A) － (C) － (B) ③ (B) － (C) － (A) ⑤ (C) － (B) － (A) ② (B) － (A) － (C) ④ (C) － (A) － (B)",
                "")
            body = body.replace(
                "(A) (C) ① based …… allows …… never ② based …… forbids …… mostly ③ lost …… allows …… mostly ④ lost …… "
                "allows …… never ⑤ lost …… forbids …… never ",
                "")
            body = body.replace(
                'excited → disappointed ② embarrassed → satisfied → relieved ③ lonely → pleased ⑤ delighted → jealous '
                '④ annoyed 20.',
                '')
            body = body.replace(
                'excited → disappointed ③ amazed → horrified ⑤ worried → confident ② indifferent → thrilled ④ '
                'surprised → relieved 20.',
                '')
            body = body.replace('$36 ② $40 ③ $45 ④ $47 ⑤ $50 4.', "")
            body = body.replace(
                '* hangar: (C) (D) (B) (B) (D) (C) (A) (B) (C) (D) (C) (D) (C) (D) (B) (B) Koppe Koppe Koppe (a) (e) '
                '(a) (b) (c) (d) (e)',
                '')
            body = body.replace(' and ________________________', '')
            body = body.replace("into that after (A) (C) (B) (A) (C) (B) (A) (C) (C) (B) (B) (A) (B) (C) (A) (B) (A) ",
                                "")
            body = body.replace("exciting and festive busy and frustrating mysterious and scary friendly and funny "
                                "peaceful and boring One of the toughest parts of isolation is a lack of an "
                                "expressive exit.",
                                "")
            body = body.replace("* sundae: , relieved irritated calm envious sympathetic terrified frightened "
                                "indifferent annoyed embarrassed",
                                "")
            body = body.replace("(a) ② (b) ③ (c) ④ (d) ⑤ (e) 45.", "")
            body = body.replace("－ (D) － (C) ③ (C) － (D) － (B) ⑤ (D) － (C) － (B) ② (C) － (B) － (D) ④ (D) － (B) － (C) ",
                                "")
            body = body.replace("(A) (B) (A) (B) ① justify …… time ③ cherish …… time ⑤ modify …… trouble (A) (B) ② "
                                "justify …… face ④ modify …… face 42.",
                                "")
            body = body.replace("① On the other hand …… however ② On the other hand …… for instance …… for instance ③ "
                                "As a result …… however ④ As a result ⑤ In other words …… therefore 38.", "")
            body = body.replace('$500 ② $600 ③ $700 ④ $1,000 ⑤ $1,200 Paul: 15.', "")
            body = body.replace('$36 ② $45 ③ $54 ④ $60 ⑤ $63 4.', "")
            body = body.replace('Blackhills Hiking Jackets Model A B C D E ① ② ③ ④ ⑤ Price $ 40 $ 55 $ 65 $ 70 $ 85 '
                                'Pockets Waterproof 3 4 5 6 6 ☓ ○ ○ ☓ ○ Color brown blue yellow gray black 13.', "")
            body = body.replace("－ (C) － (D) ③ (C) － (B) － (D) ⑤ (D) － (C) － (B) ② (B) － (D) － (C) ④ (D) － (B) － (C) "
                                "44.", "")

            body = body.replace('① For example …… As a result ② For example …… In contrast ③ Otherwise …… As a result '
                                '④ Meanwhile …… In contrast ⑤ Meanwhile …… Nevertheless 37.', "")

            body = body.replace('- (C) - (D) ③ (C) - (B) - (D) ⑤ (D) - (B) - (C) ② (B) - (D) - (C) ④ (C) - (D) - (B) '
                                '47.', "")
            body = body.replace('- (B) - (C) ③ (B) - (C) - (A) ⑤ (C) - (B) - (A) ② (B) - (A) - (C) ④ (C) - (A) - (B) '
                                '44.', "")

            body = body.replace('…… interference (A) ① foreign ② immediate …… sympathy …… sympathy ③ foreign ④ '
                                'imaginary …… alienation ⑤ immediate …… alienation 7 8.', "")

            body = body.replace('…… thinking …… occupied …… think …… think ① So …… to occupy ② So ③ So …… occupied ④ '
                                'Such …… thinking …… occupied ⑤ Such …… thinking …… to occupy 22.', "")

            body = body.replace('scared ④ annoyed ② delighted ⑤ sympathetic ③ encouraged 3.', "")

            body = body.replace('bored → amused ③ joyous → terrified ⑤ afraid → disappointed ② worried → pleased ④ '
                                'excited → sorrowful 31.', "")

            body = body.replace('- (B) - (C) ② (A) - (C) - (B) ③ (B) - (A) - (C) ④ (C) - (A) - (B) ⑤ (C) - (B) - (A) '
                                '50.', '')

            body = body.replace('a) ② (b) ③ (c) ④ (d) ⑤ (e', '')
            body = body.replace(' 47.', '.')
            body = body.replace("(A) , ", " ")
            body = body.replace("(B) , ", " ")
            body = body.replace("(C) , ", " ")
            body = body.replace("(D) , ", " ")
            body = body.replace("(E) , ", " ")
            body = body.replace(
                '- (B) - (C) ② (A) - (C) - (B) ③ (B) - (C) - (A) ④ (C) - (A) - (B) ⑤ (C) - (B) - (A) 30.',
                "")
            body = body.replace('try try try tried tried - - - - - opened opened to open to open opened - - - - - '
                                'sliding slide sliding slide sliding 21.', "")
            body = body.replace('referee - coach ② announcer - team owner ③ reporter - coach ④ team owner - player ⑤ '
                                'reporter - player 9.', "")
            body = body.replace('library ② publishing company ③ furniture store ④ bookstore ⑤ fire station 10.', "")
            body = body.replace('miniskirts ② training suits ③ dark green suits ④ navy blue suits ⑤ hats 13.', "")
            body = body.replace('to give her a ride ② to give her a recipe ③ to come to the party ④ to do the dishes '
                                '⑤ to go to the grocery store 11.', "")
            body = body.replace('to warn investors ② to attract investors ③ to entertain customers ④ to apologize to '
                                'customers ⑤ to criticize products 7.', "")
            body = body.replace('indifferent ② relaxed ③ confident ④ disappointed ⑤ amused 3.', "")
            body = body.replace('$850 ② $900 ③ $1,400 ④ $1,550 ⑤ $1,700 8.', "")
            body = body.replace(
                "- (B) - (C) ③ (B) - (C) - (A) ⑤ (C) - (B) - (A) ② (B) - (A) - (C) ④ (C) - (A) - (B) 50.", "")
            body = body.replace("define ② refine ③ define ④ refine ⑤ define", "")
            body = body.replace("is ① Removal of Moles ③ Origin of Fortunetelling ④ Moles : The Skin s Enemy ⑤ "
                                "Character and Superstition ② What a Mole Tells 43.", "")
            body = body.replace("compared ② forgotten ③ wished ④ repaired ⑤ remembered ", "")
            body = body.replace("① (A) - (B) - (C) ③ (B) - (C) - (A) ⑤ (C) - (B) - (A) ② (B) - (A) - (C) ④ (C) - (A) "
                                "- (B) ", "")
            body = body.replace("6.\n5", "6.5")
            body = body.replace('in spite of ② contrary to ③ owing to ④ regardless of ⑤ in addition to 27.', "")
            body = body.replace("-------- - (B) ", " ")
            body = body.replace('singer s.', 'singers.')
            body = body.replace('j oy', 'joy')
            body = body.replace('compared ② forgotten ③ wished ④ repaired ⑤ remembered-------- - (B) ignored '
                                'succeeded accomplished taken care of looked forward to 38.', '')

            body = body.replace(
                '- (D) - (C) ③ (C) - (D) - (B) ⑤ (D) - (C) - (B) ② (C) - (B) - (D) ④ (D) - (B) - (C).', '')

            sentences = []
            splt = body.split("\n")

            for line in splt:
                line = line.strip()
                if line.startswith("(A)"):
                    line = line[3:].strip()
                if line.startswith("(B)"):
                    line = line[3:].strip()
                if line.startswith("(C)"):
                    line = line[3:].strip()
                if line.startswith("(D)"):
                    line = line[3:].strip()
                if line.startswith("(E)"):
                    line = line[3:].strip()
                if line.startswith("(a)"):
                    line = line[3:].strip()
                if line.startswith("(b)"):
                    line = line[3:].strip()
                if line.startswith("(c)"):
                    line = line[3:].strip()
                if line.startswith("(d)"):
                    line = line[3:].strip()
                if line.startswith("(e)"):
                    line = line[3:].strip()
                if line.startswith("( ① )"):
                    line = line[5:].strip()
                if line.startswith("( ② )"):
                    line = line[5:].strip()
                if line.startswith("( ③ )"):
                    line = line[5:].strip()
                if line.startswith("( ④ )"):
                    line = line[5:].strip()
                if line.startswith("( ⑤ )"):
                    line = line[5:].strip()
                if line.startswith("①"):
                    line = line[1:].strip()
                if line.startswith("②"):
                    line = line[1:].strip()
                if line.startswith("③"):
                    line = line[1:].strip()
                if line.startswith("④"):
                    line = line[1:].strip()
                if line.startswith("⑤"):
                    line = line[1:].strip()
                if line.startswith("1)"):
                    line = line[2:].strip()
                if line.startswith("2)"):
                    line = line[2:].strip()
                if line.startswith("3)"):
                    line = line[2:].strip()
                if line.startswith("Man:"):
                    line = line[4:].strip()
                if line.startswith("Woman:"):
                    line = line[6:].strip()
                if line.startswith("Man :"):
                    line = line[5:].strip()
                if line.startswith("Woman :"):
                    line = line[7:].strip()
                if line.startswith("※"):
                    line = line[1:].strip()
                if line.startswith("◈"):
                    line = line[1:].strip()
                if line.startswith("－"):
                    line = line[1:].strip()
                if line.startswith("2 8 "):
                    line = line[3:].strip()
                if line.startswith("①"):
                    line = line[1:].strip()
                if line.startswith("( )"):
                    line = line[3:].strip()
                if line.startswith("()"):
                    line = line[2:].strip()
                if line.startswith("(B) (A)"):
                    line = line[7:].strip()
                if line.startswith("*"):
                    line = line[7:].strip()
                if line.startswith("(A)"):
                    line = line[3:].strip()
                if line.startswith("(B)"):
                    line = line[3:].strip()
                if line.startswith("(C)"):
                    line = line[3:].strip()
                if line.startswith("(D)"):
                    line = line[3:].strip()
                if line.startswith("(E)"):
                    line = line[3:].strip()
                if line.startswith("e:"):
                    line = line[2:].strip()
                if line.startswith(") "):
                    line = line[1:].strip()
                    line = line[3:].strip()
                if line.startswith("(①)"):
                    line = line[3:].strip()
                if line.startswith("(②)"):
                    line = line[3:].strip()
                if line.startswith("(③)"):
                    line = line[3:].strip()
                if line.startswith("(④)"):
                    line = line[3:].strip()
                if line.startswith("(⑤)"):
                    line = line[3:].strip()
                if line.startswith(": "):
                    line = line[1:].strip()
                if line.startswith("8 8"):
                    line = line[3:].strip()

                if len(line) < 10:
                    continue
                if len(line.split(" ")) < 4:
                    continue
                if U.is_korean(line):
                    continue
                if line.startswith("“") and not line.endswith("”"):
                    if "“" not in line[1:]:
                        line = line[1:].strip()
                elif not line.startswith("“") and line.endswith("”"):
                    if "“" not in line[:-2]:
                        line = line[:-1].strip()
                elif line.startswith("“") and line.endswith("”"):
                    line = line[1:-1].strip()

                if line.startswith("(") and line.endswith(")"):
                    line = line[1:-1].strip()
                elif line.startswith("(") and ")" not in line:
                    line = line[1:].strip()
                elif line.endswith(")") and "(" not in line:
                    line = line[1:].strip()

                sentences.append(line)

            ret.append((test_name, sentences))
    return ret

