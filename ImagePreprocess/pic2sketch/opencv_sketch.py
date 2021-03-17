#coding:utf-8
import cv2
import numpy as np

#读取原始图像
gray = cv2.imread('ImagePreprocess\colour_girl.png')

#图像灰度处理
gray = cv2.cvtColor(gray,cv2.COLOR_BGR2GRAY)

#高斯滤波降噪
gaussian = cv2.GaussianBlur(gray, (11,11), 0)
 
#Canny算子
canny = cv2.Canny(gaussian, 50, 150)

#阈值化处理
ret, result = cv2.threshold(canny, 0, 255, cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)

#显示图像
cv2.namedWindow("result",0)
#cv2.imshow('src', img)
cv2.imshow('result', result)
cv2.waitKey()
cv2.destroyAllWindows()