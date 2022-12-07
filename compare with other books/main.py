"""
Author : Byunghyun Ban
Email : bhban@kakao.com
"""
import utils as U
import os
import pyexcel as px


ours = "ours.txt"
kss = "kss.txt"
wm = "wordmaster.txt"

dict_file = "dict.csv"

sn_dir = "sn"
pgw_dir = "pgw"

out_sn_dir = sn_dir + "_words"
out_pgw_dir = pgw_dir + "_words"


if out_sn_dir not in os.listdir():
    os.mkdir(out_sn_dir)

if out_pgw_dir not in os.listdir():
    os.mkdir(out_pgw_dir)


def read_word_dict_from_csv(filename, word_list):
    ret = {}
    file = open(filename, encoding="utf8")
    for line in file:
        line = line.strip()
        if ", " not in line:
            continue
        var, origin = line.strip().split(", ")
        if origin not in word_list and var not in word_list:
            continue
        if origin not in ret:
            ret[origin] = [var]
            if origin != var:
                ret[origin].append(origin)
        else:
            ret[origin].append(var)

    file.close()
    return ret


def read_sunung_txts(el):
    test_name = el.split(".")[0]
    txt = open(el, encoding="utf8")
    body = txt.read()
    body.lower()
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

        if len(line) < 1:
            continue
        if len(line.split(" ")) < 1:
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

    return (test_name, sentences)


def extract_word_list(out_dir, test_dir, test_filename):
    test_name, body = read_sunung_txts(test_dir + "/" + test_filename)
    word_list = set(" ".join(body).split(" "))
    word_dict = read_word_dict_from_csv(dict_file, list(word_list))

    wd_list = []
    for el in word_dict.keys():
        words = word_dict[el]
        for w in words:
            if w in word_list:
                wd_list.append(el)
                break

    ws = "\n".join(wd_list)
    out = open(out_dir + "/" + test_filename, "w")
    out.write(ws)
    out.close()


def txt_2_set(file):
    a = open(file)
    b = set(a.read().split("\n"))
    a.close()
    return b


def get_analysis(ours, kss, wm, comp_dir):
    word_ours = txt_2_set(ours)
    word_kss = txt_2_set(kss)
    word_wm = txt_2_set(wm)

    comp_files = os.listdir(comp_dir)
    comp_files.sort()

    HEADER = ["TestName", "# Words"]
    HEADER += ["[# Correct] " + ours, "[# Correct] " + kss, "[# Correct] " + wm]
    HEADER += ["[Accuracy] " + ours, "[Accuracy] " + kss, "[Accuracy] " + wm]
    array = [HEADER]

    for el in comp_files:
        if not el.endswith(".txt"):
            continue

        cnt = [el.split(".")[0]]
        word_test = txt_2_set(comp_dir + "/" + el)
        cnt.append(len(word_test))

        # 예측성공 개수
        ours = len(word_ours & word_test)
        kss = len(word_kss & word_test)
        wm = len(word_wm & word_test)

        cnt += [ours, kss, wm]

        # 적중률
        ours = (ours / len(word_ours)) // 0.001 / 10
        kss = (kss / len(word_kss)) // 0.001 / 10
        wm = (wm / len(word_wm)) // 0.001 / 10

        cnt += [ours, kss, wm]

        array.append(cnt)

    px.save_as(array=array, dest_file_name=comp_dir + ".xlsx")


for el in os.listdir(sn_dir):
    if el.endswith(".txt"):
        extract_word_list("sn_words", sn_dir, el)


for el in os.listdir(pgw_dir):
    if el.endswith(".txt"):
        extract_word_list("pgw_words", pgw_dir, el)


get_analysis(ours, kss, wm, out_pgw_dir)
get_analysis(ours, kss, wm, out_sn_dir)
