import cv2
import numpy as np
import math

#基本参数
#单位：mm
w=184.0 #电机宽度 0.0046*25*16*10*5*2
wp=150.0 #纸宽度
hp=200.0 #纸高度
x1=17.0
y1=10.0
wr=0.0046*25 #最小转动距离
sec_beta=1.2
input_image_path="ImagePreprocess\lineCloser&Normalizer\lineNormalizer+otsu.png"
output_image_path="test.jpg"

#获取源图像
input_image=cv2.imread(input_image_path)
print("图片大小为（高, 宽, 通道）：", input_image.shape)
wi=input_image.shape[1]
hi=input_image.shape[0]


#计算线的取值范围
a_min=sec_beta*math.sqrt(x1**2+(y1/sec_beta)**2)
a_max=sec_beta*math.sqrt((x1+wp)**2+((y1+hp)/sec_beta)**2)
b_min=sec_beta*math.sqrt((w-x1-wp)**2+(y1/sec_beta)**2)
b_max=sec_beta*math.sqrt((w-x1)**2+((y1+hp)/sec_beta)**2)

#计算位图的分辨率
wb=int(a_max/wr)
hb=int(b_max/wr)
print("位图宽长为：",wb,hb)
wb_start=int(a_min/wr-1)
hb_start=int(b_min/wr-1)
print("有效宽长为：",wb-wb_start,hb-hb_start)

#计算像素网格长度
wg=min(wp/wi, hp/hi)

#映射，固定转动距离
output_image=np.ones((hb,wb,3))*255
point=0
for k in range(wb_start,wb):
    for l in range(hb_start,hb):
        a=k*wr
        b=l*wr
        if ((a+b)/sec_beta)<w or ((b-a)/sec_beta)>w or ((a-b)/sec_beta)>w:
            continue
        x=(a**2-b**2)/(2*w*(sec_beta**2))+w/2
        if a**2-(x**2)*(sec_beta**2)<0:
            continue
        y=math.sqrt(a**2-(x**2)*(sec_beta**2))
        if x>=x1 and y>=y1:
            m=int((x-x1)/wg)
            n=int((y-y1)/wg)
            if m<wi and n<hi:
                output_image[l,k]=input_image[n,m]
                point+=1
print("有效像素点：",point)

output_image=output_image.astype(np.uint8)
cv2.namedWindow("input image",0)
cv2.imshow('input image', input_image)
#cv2.waitKey(0)
cv2.namedWindow("output image",0)
cv2.imshow('output image', output_image)
cv2.waitKey(0)

#cv2.imwrite("output.png", output_image)