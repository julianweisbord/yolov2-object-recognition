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
        # print("annots: ", annots)
        img = path.split('/', 1)[-1]
        if img not in annots:
            print("not in anots!")
            # print("annotation base path", img[:img.find(".")])
            # Add img to validation set
            jpg_path = path + ".jpg"
            print("jpg_path", jpg_path)
            save_img = cv2.imread(jpg_path)
            # print("save_img: ", save_img)
            val_img_path = VALIDATION_PATH + "/val_{}.jpg".format(img)
            print("val_img_path", val_img_path)
            cv2.imwrite(val_img_path, save_img)

def main():
    base = sys.argv[1]
    # for n, path in enumerate(os.listdir(base)):
    #     print(path)
    #     os.rename(base + '/' + path, base + '/time' + str(n + 753))
    make_val_set(base)
if __name__ == '__main__':
    main()
