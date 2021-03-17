import numpy as np
import cv2
import time

def search(image, index_now):
    distance=0
    height=image.shape[0]
    width=image.shape[1]
    no_result=4
    while no_result != 0:
        distance+=1
        no_result=4
        k=0
        l=0
        if index_now[1]-distance>=0:
            #print(1, end='')
            for i in range(distance-1,-distance,-1):
                k=index_now[0]+i
                l=index_now[1]-distance
                if k>=0 and l>=0 and k<width and l < height and image[l, k]==1:
                    return [k, l]
            if index_now[0]-distance>=0:
                k-=1
                if k>=0 and l>=0 and k<width and l < height and image[l,k]==1:
                    return [l, k]
        else:
            no_result-=1
        if index_now[0]-distance>=0:
            #print(2, end='')
            for i in range(-distance+1,distance):
                k=index_now[0]-distance
                l=index_now[1]+i
                if k>=0 and l>=0 and k<width and l < height and image[l, k]==1:
                    return [k, l]
            if index_now[1]+distance<height:
                l+=1
                if k>=0 and l>=0 and k<width and l < height and image[l, k]==1:
                    return [k, l]
        else:
            no_result-=1
        if index_now[1]+distance<height:
            #print(3, end='')
            for i in range(-distance+1,distance):
                k=index_now[0]+i
                l=index_now[1]+distance
                if k>=0 and l>=0 and k<width and l < height and image[l, k]==1:
                    return [k, l]
            if index_now[0]+distance<width:
                k+=1
                if k>=0 and l>=0 and k<width and l < height and image[l, k]==1:
                    return [k, l]
        else:
            no_result-=1
        if index_now[0]+distance<width:
            #print(4)
            for i in range(distance-1,-distance,-1):
                k=index_now[0]+distance
                l=index_now[1]+i
                if k>=0 and l>=0 and k<width and l < height and image[l, k]==1:
                    return [k, l]
            if index_now[1]-distance>=0:
                l-=1
                if k>=0 and l>=0 and k<width and l < height and image[l, k]==1:
                    return [k, l]
        else:
            no_result-=1
    return None



if __name__ == "__main__":
    image = 1-cv2.imread("test/final.png", cv2.IMREAD_GRAYSCALE)/255
    image = image.astype(np.uint8)
    print(image.shape)
    index_now=[0,0]
    image_draw = np.zeros([image.shape[0],image.shape[1]], dtype=np.uint8)
    i=0
    while True:
        index_now = search(image,index_now)
        if index_now == None:
            break
        else:
            image_draw[index_now[1], index_now[0]] = 255
            image[index_now[1], index_now[0]] = 0
        i+=1
        cv2.namedWindow("image_draw",0)
        cv2.imshow("image_draw", image_draw)
        cv2.waitKey()
    cv2.imwrite("image_draw2.jpg", image_draw)