# -*- coding: utf-8 -*-

""" 去重 文本纠错 """
import re
import difflib
import ConfigParser

from aip import AipNlp

# pip install baidu-aip
# http://ai.baidu.com/docs#/NLP-Python-SDK/f524c757

CONFIG_FILE = "baidu_api.cfg"
config = ConfigParser.ConfigParser()
config.read(CONFIG_FILE)

APP_ID = config.get("BAIDU_NLP", "APP_ID") 
API_KEY = config.get("BAIDU_NLP", "API_KEY")
SECRET_KEY = config.get("BAIDU_NLP", "SECRET_KEY") 

client = AipNlp(APP_ID, API_KEY, SECRET_KEY)


def merge_str(input_file, output_file):
    with open(input_file, "r", encoding="utf-8") as origin_file:
        for line in origin_file:
            with open(output_file, "a+", encoding="utf-8") as out_file:
                head, *content = line.split(",")
                line = head + "," + "".join(content)
                out_file.write(line)


def de_duplication(ocr_file, output_file):

    previous_line = "image_id, image_content"

    with open(ocr_file, "r", encoding="utf-8") as origin_file:
        for line in origin_file:

            with open(output_file, "a+", encoding="utf-8") as out_file:
                if line.split(",")[1] == previous_line.split(",")[1]:  # Detect duplication
                    line = previous_line.split(",")[0] + "|" + line.split(",")[0] + "," + line.split(",")[1]
                elif string_similar(line.split(",")[1], previous_line.split(",")[1]) > 0.5:
                    if len(line) > len(previous_line):
                        line = previous_line.split(",")[0] + "|" + line.split(",")[0] + "," + line.split(",")[1]
                    else:
                        line = previous_line.split(",")[0] + "|" + line.split(",")[0] + "," + previous_line.split(",")[1]
                    pass
                else:
                    out_file.write(previous_line)
                previous_line = line


def correct_text(input_text: str):
    result = client.ecnet(input_text)
    return result['item']['correct_query']


def correct_csv_file(input_file, output_file):
    with open(input_file, "r", encoding="utf-8") as origin_file:
        for line in origin_file:
            with open(output_file, "a+", encoding="utf-8") as out_file:
                line = line.split(",")[0] + correct_text(line.split(",")[1]) + "\n"
                out_file.write(line)


def string_similar(s1, s2):
    return difflib.SequenceMatcher(None, s1, s2).quick_ratio()


zh_pattern = re.compile(u'[\u4e00-\u9fa5]+')


def contain_zh(word):
    """
    判断传入字符串是否包含中文
    :param word: 待判断字符串
    :return: True:包含中文  False:不包含中文
    """
    global zh_pattern
    match = zh_pattern.search(word)

    return match


def clear_no_chinese(input_file, output_file):
    with open(input_file, "r", encoding="utf-8") as origin_file:
        for line in origin_file:
            with open(output_file, "a+", encoding="utf-8") as out_file:
                if contain_zh(line):
                    out_file.write(line)


if __name__ == '__main__':
    clear_no_chinese(r"C:\Users\mi\Documents\Workspace\DrawingSword\content\ocr_v4.csv",
                     r"C:\Users\mi\Documents\Workspace\DrawingSword\content\ocr_v5.csv")
