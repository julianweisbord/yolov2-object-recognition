import os
import sys
import math
import xml.etree.ElementTree as ET
from shutil import copyfile
from matplotlib import pyplot as plt
import classify


BATCH_SIZE = 16
PREDICTED = "../mAP/predicted/"
GROUND_TRUTH = "../mAP/ground-truth/"
ANNOTATED_TRAIN = "../annotations"
ANNOTATED_VAL = "../annotations_val"
VALIDATION_IMAGES = "validation_images"
TRAIN_IMAGES = "../train_data"
PLOT = True


def create_txt_files(annotated_data, image_folder, prediction_results):
    '''
        for each annotated file, place info in txt file inside ground_truth folder as <class_name> <left> <top> <right> <bottom>
        run classify.py on all of val/ train data and output <class_name> <confidence> <left> <top> <right> <bottom> to txt file.

    '''
    # Create/overwrite txt files with predictions, ground truth, and images
    for name in prediction_results:
        skip = True
        print("file name: ", name)
        split_name = name.split('.', 1)[0]
        for file_name in os.listdir(annotated_data):
            if split_name == file_name.split('.', 1)[0]:
                skip = False
        if skip == True:
            print("coninuing")
            continue


        # copy file to images folder once
        copyfile(image_folder + '/' + name, "../mAP/images/" + name)
        txt_name = name.split('.', 1)[0] + ".txt"
        # <class_name> <confidence> <left> <top> <right> <bottom>
        f_pred = open("../mAP/predicted/{}".format(txt_name), "w+")
        print("prediction_results[name]: ", prediction_results[name])
        label = prediction_results[name][0]
        confidence = prediction_results[name][1]
        tl = prediction_results[name][2]
        br = prediction_results[name][3]
        write_pred = "{} {} {} {} {} {}".format(label, confidence, tl[0], tl[1], br[0], br[1])
        print("Write pred file: ", write_pred)
        # exit()
        f_pred.write(write_pred)

    annotations = os.listdir(annotated_data)
    for ann_file in annotations:

        skip = True
        print("file name: ", ann_file)
        split_ann_file = ann_file.split('.', 1)[0]
        for file_name in prediction_results:
            fl_name = file_name.split('.', 1)[0]
            if split_ann_file == fl_name:
                print("{} == {}".format(split_ann_file, fl_name))
                skip = False
        if skip == True:
            print("coninuing")
            continue

        tree = ET.parse(annotated_data + '/' + ann_file)
        root = tree.getroot()
        txt_name = ann_file.split('.', 1)[0] + ".txt"
        f_ground_truth = open("../mAP/ground-truth/{}".format(txt_name), "w+")
        # <class_name> <left> <top> <right> <bottom>
        name = root.find('filename').text
        print("filename for ground_truth: ", name)
        obj = root.find("object")
        if not obj:  # No Time cover in image
            continue

        label = obj.find('name').text
        bndbox = obj.find('bndbox')
        xmin = bndbox.find('xmin').text
        ymin = bndbox.find('ymin').text
        xmax = bndbox.find('xmax').text
        ymax = bndbox.find('ymax').text


        write_ground_truth = "{} {} {} {} {}".format(label, xmin, ymin, xmax, ymax)
        print("Write ground_truth file: ", write_ground_truth)
        f_ground_truth.write(write_ground_truth)

def get_predictions(imageset, annotated_data, step_num):

    epochs = []

    epoch = math.floor(step_num / BATCH_SIZE)
    if imageset == "train":
        image_folder = TRAIN_IMAGES
        prediction_results = classify.classify(TRAIN_IMAGES, step=step_num)
    else:
        image_folder = VALIDATION_IMAGES
        prediction_results = classify.classify(VALIDATION_IMAGES, step=step_num)
    print("epoch: ", epoch)
    create_txt_files(annotated_data, image_folder, prediction_results)


def plot(epochs, train_mAP, val_mAP):
    plt.plot(train_mAP, epochs)
    plt.plot(val_mAP, epochs)
    plt.xlabel("mAP %")
    plt.ylabel("Epoch number")
    plt.show()

def main():
    if len(sys.argv) != 4:
        print("Usage: python3 plot_map.py <train/val> <annotated_data> <step number> ")
        exit()
    imageset = sys.argv[1]
    annotated_data = sys.argv[2]
    step = int(sys.argv[3])
    print("imageset", imageset)

    epochs = [15, 23, 31, 39, 47, 55, 63, 71, 79, 87]
    train_mAP = [1.59, 65.27, 88.75, 92.08, 92.39, 93.83, 95.14, 95.63, 98.47, 97.6]
    val_mAP = [0.82, 63.88, 85.62, 87.71, 89.84, 88.1, 89.57, 89.05, 90.13, 90.64]
    if PLOT:
        plot(epochs, train_mAP, val_mAP)
    else:
        get_predictions(imageset, annotated_data, step)



if __name__ == '__main__':
    main()
