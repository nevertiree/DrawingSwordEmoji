# -*- coding: utf-8 -*-

""" Parse frame subtitle via baidu OCR AIP. """

import os
import json
import ConfigParser

from aip import AipOcr  # http://ai.baidu.com/docs#/OCR-Python-SDK/80d64770

CONFIG_FILE = "baidu_api.cfg"
config = ConfigParser.ConfigParser()
config.read(CONFIG_FILE)

APP_ID = config.get("BAIDU_OCR", "APP_ID") 
API_KEY = config.get("BAIDU_OCR", "API_KEY")
SECRET_KEY = config.get("BAIDU_OCR", "SECRET_KEY") 

client = AipOcr(APP_ID, API_KEY, SECRET_KEY)
"""
{
    "log_id": 2481452968412708000, 
    "direction": 0, 
    "words_result_num": 1, 
    "words_result": [
        {
            "words": "不挑场硬仗打你翻得过身来吗", 
            "probability": {
                "variance": 0.000064, 
                "average": 0.995399, 
                "min": 0.972358
            }
        }
    ], 
    "language": -1
}
"""


def get_file_content(file_path):
    """ 读取图片 """
    with open(file_path, 'rb') as fp:
        return fp.read()


def accurate_ocr(image):
    """ 调用通用文字识别（高精度版） """
    client.basicAccurate(image)

    """ 如果有可选参数 """
    options = {"detect_direction": "true", "probability": "false"}

    """ 带参数调用通用文字识别（高精度版） """
    print(client.basicAccurate(image, options))


def basic_ocr(image):
    """ 调用通用文字识别, 图片参数为本地图片 """
    # client.basicGeneral(image)

    """ 如果有可选参数 """
    options = {"language_type": "CHN_ENG",
               "detect_direction": "true",
               "detect_language": "true",
               "probability": "false"}

    """ 带参数调用通用文字识别, 图片参数为本地图片 """
    try:
        return client.basicGeneral(image, options)['words_result']
    except json.decoder.JSONDecodeError:
        return None


if __name__ == '__main__':

    image_dir = "../data/image"
    content_dir = "../data/content"

    for image_sub_dir in os.listdir(image_dir):  
        # Open image sub-dir, eg: 01/ 02/ 03/ ...
        print(image_sub_dir)

        # Write OCR result into a csv file.
        content_file = os.path.join(content_dir, image_sub_dir+".csv")

        # If the programm crash, let it restart.
        restart_point = None
        if os.path.exists(content_file):
            last_line = None
            with open(content_file, "r", encoding="utf-8") as csv_file:
                for line in csv_file:
                    last_line = line
            if last_line:  # Find the last parsed image.
                restart_point = last_line.split(",")[0]  

        """ Parse screenshot image via baidu OCR API """
        for image_name in os.listdir(os.path.join(image_dir, image_sub_dir)):

            # Skip current image, if it has been parsed.
            if restart_point:
                if restart_point >= image_name:
                    continue

            # Call baidu OCR API
            image = get_file_content(os.path.join(image_dir, image_sub_dir, image_name))
            ocr_result_list = basic_ocr(image)

            # If OCR result is not None.
            if ocr_result_list:
                try:
                    with open(content_file, 'a+', encoding="utf-8") as f:
                        line = [str(image_name)]
                        for result in ocr_result_list:
                            line.append(result['words'])
                        line = ",".join(line) + "\n"
                        print(line)
                        f.write(line)
                except UnicodeEncodeError:
                    pass