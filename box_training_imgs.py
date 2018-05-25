import os
import matplotlib.pyplot as plt
import cv2
from matplotlib.widgets import RectangleSelector
from gen_xml import write_xml

# global constants
img = None
tl_list = []
br_list = []
object_list = []

# constants
IMAGE_FOLDER = 'darkflow-master/validation_images'
SAVEDIR = 'annotations'
SAVEDIR_VAL = 'annotations_val'
OBJECT = 'time_cover'


def line_select_callback(clk, rls):
    global tl_list
    global br_list
    global object_list
    tl_list.append((int(clk.xdata), int(clk.ydata)))
    br_list.append((int(rls.xdata), int(rls.ydata)))
    object_list.append(OBJECT)


def onkeypress(event):
    global object_list
    global tl_list
    global br_list
    global img
    if event.key == 'n':
        print(object_list)
        write_xml(IMAGE_FOLDER, img, object_list, tl_list, br_list, SAVEDIR_VAL)
        tl_list = []
        br_list = []
        object_list = []
        img = None
        plt.close()


def toggle_selector(event):
    toggle_selector.RS.set_active(True)


if __name__ == '__main__':

    for n, image_file in enumerate(os.scandir(IMAGE_FOLDER)):

        img = image_file
        fig, ax = plt.subplots(1)
        image = cv2.imread(image_file.path)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        ax.imshow(image)

        toggle_selector.RS = RectangleSelector(
            ax, line_select_callback,
            drawtype='box', useblit=True,
            button=[1], minspanx=5, minspany=5,
            spancoords='pixels', interactive=True
        )
        bbox = plt.connect('key_press_event', toggle_selector)
        key = plt.connect('key_press_event', onkeypress)
        plt.show()
