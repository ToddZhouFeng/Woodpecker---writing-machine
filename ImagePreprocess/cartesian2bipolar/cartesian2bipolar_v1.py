import cv2
import numpy as np
import math

#基本参数
#单位：mm
""" w=184.0 #电机宽度 0.0046*25*16*10*5*2
wp=150.0 #纸宽度
hp=200.0 #纸高度
x1=17.0
y1=10.0 """

w=162
wp=150
hp=200
x1=6
y1=60

wr=0.0046 #最小转动距离
wr_min=wr*25
wr_max=wr*100
input_image_path="ImagePreprocess\lineCloser&Normalizer\lineCloser.png" #"ImagePreprocess\grey_girl.png"
output_image_path="test.jpg"

#获取源图像
input_image=cv2.imread(input_image_path)
print("图片大小为（高, 宽, 通道）：", input_image.shape)
wi=input_image.shape[1]
hi=input_image.shape[0]


#计算线的取值范围
a_min=math.sqrt(x1**2+y1**2)
a_max=math.sqrt((x1+wp)**2+(y1+hp)**2)
b_min=math.sqrt((w-x1-wp)**2+y1**2)
b_max=math.sqrt((w-x1)**2+(y1+hp)**2)

#计算位图的分辨率
wb=int(a_max/wr_min)
hb=int(b_max/wr_min)
print("位图宽长为：",wb,hb)
wb_start=int(a_min/wr_min-1)
hb_start=int(b_min/wr_min-1)
print("有效宽长为：",wb-wb_start,hb-hb_start)

#计算网格长度
wg=min(wp/wi, hp/hi)

#映射，固定转动距离
output_image=np.ones((hb,wb,3))*255#*100
point=0
for k in range(wb_start,wb):
    for l in range(hb_start,hb):
        a=k*wr_min
        b=l*wr_min
        if (a+b-0.0001)<w or (w+a-0.0001)<b or (w+b-0.0001)<a:
            continue
        x=(a**2+w**2-b**2)/(2*w)
        y=math.sqrt((a*w)**2-((w**2+a**2-b**2)/2)**2)/w
        if x>=x1 and y>=y1:
            m=int((x-x1)/wg)
            n=int((y-y1)/wg)
            if m<wi and n<hi:
                output_image[l,k]=input_image[n,m]
                point+=1
print("有效像素点：",point)

#映射，动态转动距离
""" output_image=np.ones((hb,wb,3))*100
for k in range(0,wb):
    for l in range(0,hb):
        a=k*wr_min
        b=l*wr_min
        if (a+b-0.1)<w or (w+a-0.1)<b or (w+b-0.1)<a:
            continue
        else:
            y=math.sqrt((a*w)**2-((w**2+a**2-b**2)/2)**2)/w
            if y>(y1+hp):
                continue
            else:
                wr_dynamic=int((wr_min+(wr_max-wr_min)/math.log(hp+1)*math.log(y1+hp-y+1))/wr)
            a=k*wr_dynamic*wr
            b=k*wr_dynamic*wr

        if (a+b-0.1)<w or (w+a-0.1)<b or (w+b-0.1)<a:
            continue
        x=(a**2+w**2-b**2)/(2*w)
        y=math.sqrt((a*w)**2-((w**2+a**2-b**2)/2)**2)/w
        if x>=x1 and y>=y1:
            m=int((x-x1)/wg)
            n=int((y-y1)/wg)
            if m<wi and n<hi:
                output_image[l,k]=input_image[n,m] """

output_image=output_image.astype(np.uint8)
cv2.namedWindow("input image",0)
cv2.imshow('input image', input_image)
#cv2.waitKey(0)
cv2.namedWindow("output image",0)
cv2.imshow('output image', output_image)
cv2.waitKey(0)
cv2.imwrite("test.jpg", output_image)