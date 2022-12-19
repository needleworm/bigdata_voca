import json

f = open("contentFullPdf.txt")
a = f.read().split("\n")
f.close()

keyIdx = []


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


for i, line in enumerate(a):
    line = line.strip()
    if len(line) == 4 and line.isdigit():
        keyIdx.append(i)


json_dict = {}
for i in keyIdx:
    idx = int(a[i].strip())
    word = a[i+1].split(' ')[0].strip()

    meanings = []
    for j in range(1, 10):
        line = a[i + j].strip()
        if line.startswith('1.'):
            meaning = line.split("1.")[-1].strip()
            if "]" in meaning:
                meaning = meaning.split("]")[1].strip()
            meanings.append(meaning)
        elif line.startswith('2.'):
            meaning = line.split("2.")[-1].strip()
            if "]" in meaning:
                meaning = meaning.split("]")[1].strip()
            meanings.append(meaning)
            break

    meaning = ", ".join(meanings)

    for j in range(1, 10):
        line = a[i + j].strip()
        if "년 수능" in line or "월 평가원" in line:
            sntnce = a[i + j + 1].strip()
            next_idx = i + j + 2
            if not sntnce.endswith(".") and not sntnce.endswith("?") and not sntnce.endswith("!"):
                sntnce += " " + a[i + j + 2].strip()
                next_idx += 1

            translation = a[next_idx].strip()
            if not translation.endswith(".") and not translation.endswith("?") and not translation.endswith("!"):
                translation += " " + a[next_idx + 1].strip()

            hubos = data_dict[word]
            for wd in hubos:
                sntnc = sntnce.replace(".", " ")
                sntnc = sntnce.replace(",", " ")
                sntnc = sntnce.replace("'", " ")
                sntnc = sntnce.replace('"', " ")
                sntnc = sntnce.replace("`", " ")
                sntnc = sntnce.replace(":", " ")
                if " " + wd + " " in sntnce:
                    appearance = wd
                    sentence = sntnce.split(" " + wd + " ")
                    break

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



