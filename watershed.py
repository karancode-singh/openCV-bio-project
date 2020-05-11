import cv2
import numpy as np
import math
from math import hypot,sqrt
import base64
from PIL import Image
import io
from matplotlib import pyplot as plt
import time
from os.path import join

# selectOnImage = cv2.cvtColor(img[0], cv2.COLOR_GRAY2BGR)
selectOnImage = cv2.imread("1549379333.619327.jpg", cv2.IMREAD_COLOR)
selectOnImage_copy = selectOnImage.copy()
marker_image = np.zeros(selectOnImage.shape[:2],dtype=np.int32)
segments = np.zeros(selectOnImage.shape,dtype=np.uint8)
from matplotlib import cm
def create_rgb(i):
    return tuple(np.array(cm.tab10(i)[:3])*255)
colors = []
for i in range(10):
    colors.append(create_rgb(i))
current_marker = 1
n_markers = 10
marks_updated = False
def mouse_callback(event,x,y,flags,params):
    global marks_updated
    if event == cv2.EVENT_LBUTTONDOWN:
        cv2.circle(marker_image,(x,y),1,(current_marker),-1)
        cv2.circle(selectOnImage_copy,(x,y),1,colors[current_marker],-1)
        marks_updated = True
cv2.namedWindow('Image')
cv2.setMouseCallback('Image', mouse_callback)
while True:
    cv2.imshow('Watershed Segments', segments)
    cv2.imshow('Image',selectOnImage_copy)
    k = cv2.waitKey(1)
    if k == 27:
        break
    elif k == ord('c'):
        selectOnImage_copy = selectOnImage.copy()
        marker_image = np.zeros(selectOnImage.shape[:2],dtype=np.int32)
        segments = np.zeros(selectOnImage.shape, dtype=np.uint8)
    elif k>0 and chr(k).isdigit():
        current_marker = int(chr(k))
    
    if marks_updated:
        marker_image_copy = marker_image.copy()
        cv2.watershed(selectOnImage,marker_image_copy)
        segments = np.zeros(selectOnImage.shape,dtype=np.uint8)
        for color_ind in range(n_markers):
            segments[marker_image_copy==(color_ind)] = colors[color_ind]
cv2.destroyAllWindows()
