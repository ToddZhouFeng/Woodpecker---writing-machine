import cv2
import numpy as np

image = 1-cv2.imread("test/final.png", cv2.IMREAD_GRAYSCALE)/255
image = image.astype(np.uint8)
print(image.shape, image[0,0])