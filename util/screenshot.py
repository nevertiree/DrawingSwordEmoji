# -*- coding: utf-8 -*-

import os
import cv2 as cv

from tqdm import tqdm

from util.detect_subtitle import has_subtitle


def screenshot(video_path, screenshot_save_dir):
    """ """
    print(f"开始截屏：{video_path}...")
    cap = cv.VideoCapture(video_path)

    # 创建截屏保存目录
    screenshot_save_dir = screenshot_save_dir.replace(",", "_")
    if not os.path.exists(screenshot_save_dir):
        os.mkdir(screenshot_save_dir)

    # 视频名字
    video_name = "_".join(os.path.basename(video_path).split(".")[:-1])
    video_name = video_name.replace(",", "_")
    print(f"视频名称：{video_name}...")

    # 获得帧数
    frames_num = int(cap.get(7))  # CV_CAP_PROP_FRAME_COUNT
    print(f"视频帧数：{frames_num}")

    frame_frequency = 25

    pre_frame_feature = 0
    first_frame = True

    for frame_id in tqdm(range(frames_num)):
        ret, frame = cap.read()

        if frame_id % frame_frequency != 0:
            # capture every x frame
            continue
        else:
            try:
                # 判断当前的视频里面是否有字幕
                is_caption, frame_feature = has_subtitle(frame)
                screenshot_path = os.path.join(screenshot_save_dir, video_name + "_" + str(frame_id) + ".jpg")

                if cv.waitKey(1) & 0xFF == ord('q'):
                    break

                if not is_caption:
                    continue
                elif first_frame:
                    first_frame = False
                    cv.imencode('.jpg', frame)[1].tofile(screenshot_path)
                    cv.imshow('frame', frame)
                    pre_frame_feature = frame_feature
                else:
                    if abs(frame_feature - pre_frame_feature) < 0.05 * frame_feature:
                        continue
                    else:
                        cv.imencode('.jpg', frame)[1].tofile(screenshot_path)
                        cv.imshow('frame', frame)
                        pre_frame_feature = frame_feature

            except cv.error:
                break

    # when everything done , release the capture
    cap.release()
    cv.destroyAllWindows()


if __name__ == "__main__":

    video_dir = "../data/video"
    image_dir = "../data/image"
    for video_id in os.listdir(video_dir):
        screenshot(video_path=os.path.join(video_dir, video_id),
                   screenshot_save_dir=os.path.join(image_dir, video_id.split(".")[0]))
