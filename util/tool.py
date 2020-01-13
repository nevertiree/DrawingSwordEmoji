# -*- coding: utf-8 -*-

import os

def rename():
    image_dir = os.path.join("data", "image")

    for image_sub_dir in os.listdir(image_dir):
        for image_name in os.listdir(os.path.join(image_dir, image_sub_dir)):
            a, b = image_name.split("_")
            new_name = a + "_" + b.zfill(9)
            if new_name != image_name: 
                print(new_name)
            os.rename(
                os.path.join(image_dir, image_sub_dir, image_name),
                os.path.join(image_dir, image_sub_dir, new_name)
            )

def merge():
    content_dir = os.path.join("..", "data", "content")

    for csv_file in os.listdir(content_dir):

        with open(os.path.join(content_dir, "full.csv"), "a+", encoding="utf8") as of:

            with open(os.path.join(content_dir, csv_file), "r", encoding="utf8") as f:

                for line in f:
                    of.write(line)

if __name__ == "__main__":
    merge()