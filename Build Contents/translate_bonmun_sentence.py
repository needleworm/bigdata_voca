import utils as U
import pyexcel as px

pgw_sentences = "본문_평가원출신 문장.xlsx"


def get_translation(filename):
    array = px.get_array(file_name=filename)

    HEADER = array[0] + ["번역문"]
    array = array[1:]ㅠ

    for line in array:
        print(line[-1])
        translation = U.translate(line[-1])
        print(translation)
        line.append(translation)

    array = [HEADER] + array
    px.save_as(array=array, dest_file_name="[번역완료]" + filename + ".xlsx")


get_translation(pgw_sentences)
