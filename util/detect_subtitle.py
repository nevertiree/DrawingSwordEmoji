# -*- coding: utf-8 -*-

import os

import numpy as np
import cv2 as cv


def extract_edge(image_file, is_show=False):
    """ Finds edges in an image using the Canny algorithm.
        :param image_file: str
        :return:
    """

    if isinstance(image_file, str):
        img = cv.imread(image_file)
    else:
        img = image_file
    gray_img = cv.cvtColor(img, cv.COLOR_RGB2GRAY)
    img = cv.Canny(gray_img, 800, 1000)

    if is_show:
        cv.imshow("frame", img)
        cv.waitKey()
        cv.destroyAllWindows()

    return img


def has_subtitle(image_file):

    image_edge = extract_edge(image_file)
    mapped_image_edge = np.sum(image_edge, axis=1)

    quad_len = int(0.25 * len(mapped_image_edge))

    upper_part_value = sum(mapped_image_edge[:quad_len])
    lower_part_value = sum(mapped_image_edge[quad_len:])

    # print(upper_part_value)
    # print(lower_part_value)

    return lower_part_value > upper_part_value * 5


def batch_detect():
    image_dir = "../image"

    for image_name in os.listdir(image_dir):
        print(image_name, has_subtitle(os.path.join(image_dir, image_name)))

def frame_similiar(image_file_1, image_file_2):
    img_1 = cv.imread(image_file_1)
    img_2 = cv.imread(image_file_2)

    # print(img_1) 
    # print(img_2) 

    shape = img_1.shape
    print(np.product(shape))
    diff_count = np.sum(img_1 - img_2)
    print(diff_count)
    print(diff_count/shape)
    # return img_1 == img_2

if __name__ == '__main__':
    # batch_detect()
    print(frame_similiar(r"C:\Users\mi\Documents\Workspace\DrawingSword\data\image\01\01_04750.jpg", 
        # r"C:\Users\mi\Documents\Workspace\DrawingSword\data\image\01\01_04775.jpg",
        r"C:\Users\mi\Documents\Workspace\DrawingSword\data\image\03\03_03125.jpg"
        # r"C:\Users\mi\Documents\Workspace\DrawingSword\data\image\01\01_04775.jpg",
    ))
