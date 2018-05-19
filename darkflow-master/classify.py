import cv2
import tensorflow
from darkflow.net.build import TFNet
import matplotlib.pyplot as plt


# Display as vector graphic images
# %config InlineBackend.figure_format = 'svg'

options = {
    'model': 'cfg/yolov2-tiny-voc-magazine.cfg',
    'load': 'bin/yolov2-tiny-voc.weights',
    'threshold': 0.2,
    'gpu': 1.0
}

tfnet = TFNet(options)
img = cv2.imread('plane.jpeg', cv2.IMREAD_COLOR)
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
plt.imshow(img)
plt.show()
