# -*- coding: utf-8 -*-

import os
import cv2 as cv

from util.detect_subtitle import has_subtitle


def save_video_frame(video_file, frame_dir):
    print(video_file)
    cap = cv.VideoCapture(video_file)

    if not os.path.exists(frame_dir):
        os.mkdir(frame_dir)

    frames_num = int(cap.get(7))  # CV_CAP_PROP_FRAME_COUNT
    print(frames_num)

    frame_frequency = 25

    for frame_id in range(len(frames_num)):
        ret, frame = cap.read()

        if frame_id % frame_frequency != 0:
            # capture every x frame
            continue
        else:

            try:
                # Detect whether current frame has a subtitle.
                if has_subtitle(frame):
                    # eg: 02_3325.jpg
                    cv.imwrite(os.path.join(frame_dir, video_file.split(".")[0]+"_"+str(frame_id)+".jpg"),
                               frame)

                # Display the resulting frame
                cv.imshow('frame', frame)
                if cv.waitKey(1) & 0xFF == ord('q'):
                    break
            except cv.error:
                break

    # when everything done , release the capture
    cap.release()
    cv.destroyAllWindows()


if __name__ == "__main__":

    video_dir = "../data/video"
    image_dir = "../data/image"
    for video_id in os.listdir(video_dir):
        save_video_frame(video_file=os.path.join(video_dir, video_id),
                         frame_dir=os.path.join(image_dir, video_id.split(".")[0]))
