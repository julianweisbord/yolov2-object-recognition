'''
Created on May 19th, 2018
author: Julian Weisbord
sources:
description: Rename files in a directory to avoid replacing files with the same name
                when creating the data set.
'''

import os
import sys
import glob
import numpy as np
import cv2

ANOTATED_IMGS = 'annotations'
VALIDATION_PATH = 'darkflow-master/validation_images'

def make_val_set(base_dir):
    base_paths = glob.glob(base_dir + '/*')
    for pos, path in enumerate(base_paths):

        print("path before: ", path)
        path = path[:path.find(".")]
        print("path: ", path)
        annots = [img for img in os.listdir('annotations')]

        for pos, annot_img in enumerate(annots):
            annots[pos] = annot_img[:annot_img.find(".")]
        img = path.split('/', 1)[-1]
        if img not in annots:

            jpg_path = path + ".jpg"
            print("jpg_path", jpg_path)
            save_img = cv2.imread(jpg_path)
            val_img_path = VALIDATION_PATH + "/val_{}.jpg".format(img)
            print("val_img_path", val_img_path)
            cv2.imwrite(val_img_path, save_img)

def main():
    base = sys.argv[1]
    make_val_set(base)
if __name__ == '__main__':
    main()
