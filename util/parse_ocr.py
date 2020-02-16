# -*- coding: utf-8 -*-

""" Parse frame subtitle via baidu OCR AIP. """

import os
import json
import configparser

from aip import AipOcr  # http://ai.baidu.com/docs#/OCR-Python-SDK/80d64770

CONFIG_FILE = 'baidu_api.ini'
config = configparser.ConfigParser()
config.read(os.path.join(os.getcwd(), 'util', 'baidu_api.ini'))

APP_ID = config.get('BAIDU_OCR', 'APP_ID') 
API_KEY = config.get('BAIDU_OCR', 'API_KEY')
SECRET_KEY = config.get('BAIDU_OCR', 'SECRET_KEY') 

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


def read_screenshot(file_path):
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
               "detect_direction": "false",
               "detect_language": "false",
               "probability": "true"}

    """ 带参数调用通用文字识别, 图片参数为本地图片 """
    try:
        return client.basicGeneral(image, options)
    except json.decoder.JSONDecodeError:
        return None


def online_ocr(screenshot_save_path, caption_save_path):

    for screenshot_sub_dir in os.listdir(screenshot_save_path):
        # Open image sub-dir, eg: 01/ 02/ 03/ ...
        print(screenshot_sub_dir)

        # Write OCR result into a csv file.
        content_file = os.path.join(caption_save_path, screenshot_sub_dir+".csv")

        # 断点续传
        restart_point = None
        if os.path.exists(content_file):
            last_line = None
            with open(content_file, "r", encoding="utf-8") as csv_file:
                for line in csv_file:
                    last_line = line
            if last_line:  # Find the last parsed image.
                print(last_line)
                restart_point = json.loads(last_line)["log_id"]
        print(restart_point)

        """ Parse screenshot image via OCR API """
        for image_name in os.listdir(os.path.join(screenshot_save_path, screenshot_sub_dir)):

            # Skip current image, if it has been parsed.
            if restart_point:
                if restart_point >= "_".join(image_name.split(".")[:-1]):
                    continue

            # 读取图片
            screenshot_object = read_screenshot(os.path.join(screenshot_save_path, screenshot_sub_dir, image_name))
            # 调用百度API
            ocr_result = basic_ocr(screenshot_object)

            # If OCR result is not None.
            if ocr_result and ocr_result["words_result_num"] > 0:
                try:
                    with open(content_file, 'a+', encoding="utf-8") as f:
                        ocr_result["log_id"] = image_name.split(".")[0]
                        result_str = json.dumps(ocr_result, ensure_ascii=False)
                        print(result_str + "\n")
                        f.write(result_str + "\n")
                except UnicodeEncodeError:
                    pass
