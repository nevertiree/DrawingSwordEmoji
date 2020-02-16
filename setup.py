# -*- coding: utf-8 -*-

import json
import os

from util.screenshot import screenshot
from util.parse_ocr import online_ocr

# VIDEO_PATH = "video"
VIDEO_PATH = r"C:\Users\wangl\Videos\YPM\是，大臣and是，首相"
SNAPSHOT_PATH = os.path.abspath("snapshot")  # 截图地址
CAPTION_PATH = os.path.abspath("caption")  # 字幕地址

VIDEO_PATH.replace(",", "_")
SNAPSHOT_PATH.replace(",", "_")


def format_detect(video_path=VIDEO_PATH) -> str:
    print(f"检查视频目录[{video_path}]...")
    assert os.path.exists(video_path)
    print(f"视频目录检测成功...")

    print(f"检查视频格式[{video_path}]...")
    video_name_list = os.listdir(video_path)
    postfix_list = [video_name.split(".")[-1] for video_name in video_name_list]  # 获得所有视频的后缀
    if len(set(postfix_list)) != 1:
        raise ValueError(f"所有视频的格式需要相同，目前检测出的视频格式有{set(postfix_list)}")
    video_format = postfix_list[0]  # 获得视频格式
    return video_format


def caption_snapshot(video_path=VIDEO_PATH, video_format="mp4"):
    """
        1. 间隔截屏
        2. 识别截屏中是否有字幕

        :param video_path:
        :param video_format:
        :return:
    """

    if not os.path.exists(SNAPSHOT_PATH):
        os.mkdir(SNAPSHOT_PATH)

    # 进行间隔截图
    for video_name in os.listdir(video_path):
        screenshot(video_path=os.path.join(video_path, video_name),
                   screenshot_save_dir=os.path.join(SNAPSHOT_PATH, "_".join(video_name.split(".")[:-1])))


def caption_ocr(snapshot_save_path=SNAPSHOT_PATH, caption_save_path=CAPTION_PATH):
    online_ocr(snapshot_save_path, caption_save_path)
    pass


if __name__ == '__main__':
    """
    1. 字幕识别与截图
        1.1 检查`video`目录
        1.2 读取视频并且识别字幕
    2. 文字识别
        2.1 把字幕截图发送到百度API中
    3. 字幕检索
        3.1 把经过百度检索的字幕进行进一步清洗
        3.2 把字幕存储到本地
    """
    # format_detect()  # 校验视频格式
    # caption_snapshot()  # 开始剪辑
    caption_ocr()
