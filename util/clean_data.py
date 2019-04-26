# -*- coding: utf-8 -*-

import re
import os
import json

import difflib

zh_pattern = re.compile(u'[\u4e00-\u9fa5]+')  # Chinese char


def de_duplication(origin_file, output_file):

    previous_line_dict = None

    with open(origin_file, "r", encoding="utf-8") as origin_f:
        for line in origin_f:

            # First line
            if not previous_line_dict:
                previous_line_dict = json.loads(line)
                continue

            with open(output_file, "a+", encoding="utf-8") as out_file:

                # Check words_result_num
                current_line_dict = json.loads(line) 

                if current_line_dict["words_result_num"] == 0:
                    continue
                else:
                   # 文本数量大于1，先做清洗
                    word_list = current_line_dict["words_result"]
                    result_word_list = []

                    for word_item in word_list:
                        if contain_zh(word_item["words"]) and float(word_item["probability"]["average"]) > 0.8:
                            result_word_list.append(word_item)

                    if len(result_word_list) > 0:
                        current_line_dict["words_result_num"] = len(result_word_list)
                        current_line_dict["words_result"] = result_word_list
                    else:
                        continue

                if current_line_dict["words_result_num"] != previous_line_dict["words_result_num"] :  
                   # 文本数量不相同，比较难以识别，先存下来
                    print("Word num > 2")
                    out_file.write(json.dumps(previous_line_dict, ensure_ascii=False) + "\n")
                elif not contain_zh(current_line_dict["words_result"][0]['words']):
                    # 如果不含中文
                    print("Not contain cn.")
                    current_line_dict = previous_line_dict  # Drop current line
                elif float(current_line_dict["words_result"][0]["probability"]["average"]) < 0.8:
                    print("Word prob < 0.8")
                    current_line_dict = previous_line_dict  # Drop current line
                else:
                    # 计算相邻行的相似度
                    current_word = current_line_dict["words_result"][0]["words"]
                    previous_word = previous_line_dict["words_result"][0]["words"]

                    if str_similar(current_word, previous_word) > 0.6:  # Similiar
                        print("Find Similar")
                        # Merge log_id
                        if isinstance(previous_line_dict["log_id"], list):
                            previous_line_dict["log_id"].append(current_line_dict["log_id"])
                        else:
                            previous_line_dict["log_id"] = [previous_line_dict["log_id"], current_line_dict["log_id"]]
                        
                        previout_prob = previous_line_dict["words_result"][0]["probability"]["average"]
                        current_prob = current_line_dict["words_result"][0]["probability"]["average"]

                        if previout_prob < current_prob:
                            previous_line_dict["words_result"][0]["words"] = current_word

                        # 既然相识，就保持让previous继承current
                        current_line_dict = previous_line_dict  # Drop current line
                    else:
                        # 既然不相识，就写入previous。
                        out_file.write(json.dumps(previous_line_dict, ensure_ascii=False) + "\n")

                previous_line_dict = current_line_dict

    with open(output_file, "a+", encoding="utf-8") as out_file:
        out_file.write(json.dumps(previous_line_dict, ensure_ascii=False) + "\n")  # Last line


def str_similar(s1, s2):
    return difflib.SequenceMatcher(None, s1, s2).quick_ratio()


def contain_zh(word):
    """ 判断传入字符串是否包含中文 """
    global zh_pattern
    match = zh_pattern.search(word)
    return match

if __name__ == "__main__":
    de_duplication(r"C:\Users\mi\Documents\Workspace\DrawingSword\data\content\ocr_result.csv",
        r"C:\Users\mi\Documents\Workspace\DrawingSword\data\content\ocr_result_3.csv")