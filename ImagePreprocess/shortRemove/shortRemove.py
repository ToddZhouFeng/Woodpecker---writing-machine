import cv2
import numpy as np

img=cv2.imread("output.png", 0)
img=255-img

#get all connected components in the image with their stats (including their size, in pixel)
nb_edges, output, stats, _ = cv2.connectedComponentsWithStats(img, connectivity=8) 
#output is an image where every component has a different value    
size=stats[1:,-1] #extracting the size from the statistics

min_size=30
#selecting bigger components
print("图中连通区域数：", nb_edges)
result=img
for e in range(0,nb_edges-1):
    #replace this line depending on your application, here I chose to keep
    #all components above the mean size of components in the image
    """ if size[e]>=np.mean(size):
        print(size[e])
        th_up = e + 2
        th_do = th_up

        #masking to keep only the components which meet the condition
        mask = cv2.inRange(output, th_do, th_up)
        result = cv2.bitwise_xor(img, mask) """
    if size[e] < min_size:
        result[output == e+1] = 0

result=255-result
cv2.namedWindow("result")
cv2.imshow('result', result)
cv2.waitKey()
cv2.imwrite("output.png", result)