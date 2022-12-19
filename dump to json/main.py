import json

txt = open("contents.txt")
splt = txt.read().split("\n\n\n")
txt.close()

words = open("proposed.txt")
word_list = words.read().split("\n")
words.close()

data_dict = {}

file = open('dict.csv', encoding="utf8")
for line in file:
    line = line.strip()
    if ", " not in line:
        continue
    var, origin = line.strip().split(", ")
    if origin not in word_list:
        continue
    if origin not in data_dict:
        data_dict[origin] = [var]
        if origin != var:
            data_dict[origin].append(origin)
    else:
        data_dict[origin].append(var)

file.close()


json_dict = {}
for el in splt:
    splt_line = el.split("\n")
    idx, word, _ = splt_line[0].split("\t")
    idx = int(idx)
    wds.append(word)

    meanings = []
    for line in splt_line:
        line = line.strip()
        if "1." in line or "2." in line:
            q = line.split(".")[-1].strip()
            meanings.append(q)

    meaning = ", ".join(meanings)

    for i in range(len(splt_line)):
        line = splt_line[i]
        if " 수능]" in line or " 평가원]" in line:
            sntnce = splt_line[i + 1].strip()
            hubos = data_dict[word]
            for wd in hubos:
                if wd in sntnce:
                    appearance = wd
                    sentence = sntnce.split(" " + wd + " ")
                    break

            translation = splt_line[i + 2].strip()
            break

    json_dict[idx] = {
        "word": word,
        "meaning": meaning,
        "sentence": sentence,
        "translation": translation,
        "appearance": appearance
    }

out_file = open("2022_voca.json", "w", encoding="utf8")
json.dump(json_dict, out_file, indent=4, ensure_ascii=False)
out_file.close()
