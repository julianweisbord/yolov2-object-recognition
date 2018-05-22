import os
import sys
import cv2
import tensorflow
from darkflow.net.build import TFNet
import matplotlib.pyplot as plt

def main():
    if len(sys.argv) !=2:
        print("Incorrect command line args")
        exit()

    val_data = sys.argv[1]

    options = {
        'model': 'cfg/tiny-yolo-voc-1c.cfg',
        'load': 1375,
        'threshold': 0.3,
        'gpu': 0.9
    }

    tfnet = TFNet(options)
    for img in os.listdir(val_data):
        print("path for image: ", img)
        img = "validation_images/" + img
        img = cv2.imread(img, cv2.IMREAD_COLOR)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        result = tfnet.return_predict(img)
        print(result)

        tl_corner = (result[0]['topleft']['x'], result[0]['topleft']['y'])
        br_corner = (result[0]['bottomright']['x'], result[0]['bottomright']['y'])
        print(tl_corner)
        label = result[0]['label']
        # Make a green bounding box around the image
        img = cv2.rectangle(img, tl_corner, br_corner, (0, 255, 0), 3)
        text_corner = (tl_corner[0] + 30, tl_corner[1] + 30)
        # Add text to box
        img = cv2.putText(img, label, text_corner, cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 0), 4)
        plt.rcParams["figure.figsize"] = (15, 15)

        plt.imshow(img)
        plt.show()
if __name__ == '__main__':
    main()
