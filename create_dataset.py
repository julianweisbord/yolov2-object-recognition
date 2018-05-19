import os
import sys
import random
import glob
import cv2
import numpy as np

BACKGROUND_WIDTH = 600
BACKGROUND_HEIGHT = 600
PADDING = 25
OVERLAY_WIDTH = 150
OVERLAY_HEIGHT = 150

def create_dataset(background_images, overlay_images):
    if not os.path.isdir("./time_dataset"):
        os.mkdir("./time_dataset")
    # print("overlay_images: ", overlay_images)
    ovr_images = glob.glob(overlay_images + '/*')
    bkg_images = glob.glob(background_images + '/*')
    # ovr_images = [img for img in ovr_images]
    overlay_list = []
    dataset = []

    for pos, bkg_img in enumerate(bkg_images):
        print("bkg_images", bkg_images)
        print("ovr_images", ovr_images)
        print("bkg_img: ", bkg_img)
        bkg_image = cv2.imread(bkg_img)
        bkg_image = cv2.resize(bkg_image, (BACKGROUND_WIDTH, BACKGROUND_HEIGHT), 0, 0, cv2.INTER_LINEAR)
        bkg_image = bkg_image.astype(np.float32)
        bkg_image = np.multiply(bkg_image, 1.0 / 255.0)

        # save overlayed images
        cur_overlay = ovr_images[pos]
        cur_overlay = cv2.imread(cur_overlay)
        cur_overlay = cv2.resize(cur_overlay, (OVERLAY_WIDTH, OVERLAY_HEIGHT), 0,0, cv2.INTER_LINEAR)
        cur_overlay = cur_overlay.astype(np.float32)
        cur_overlay = np.multiply(cur_overlay, 1.0 / 255.0)
        rows, cols, channels = cur_overlay.shape
        # Randomly place the image
        randx = random.randint(0, BACKGROUND_WIDTH - PADDING - rows)
        randy = random.randint(0, BACKGROUND_HEIGHT - PADDING - rows)
        overlay = cv2.addWeighted(bkg_image[randx:randx + rows, randy:randy + cols], 0, cur_overlay, 1, 0)
        bkg_image[randx:randx + rows, randy:randy + cols] = overlay
        final_img = np.multiply(bkg_image, 255.0)
        cv2.imwrite("./time_dataset/overlay{}.jpg".format(pos), final_img)

def main():
    if len(sys.argv) != 3:
        print("Usage: python3 create_dataset.py <background image folder path> <overlay image folder path>")
        exit()
    background_images = sys.argv[1]
    overlay_images = sys.argv[2]
    create_dataset(background_images, overlay_images)

if __name__ == '__main__':
    main()
