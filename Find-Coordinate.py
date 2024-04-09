import cv2
import matplotlib.pyplot as plt
from SolExDataCube import Dir_Read
import os

image_path = r"C:\Users\Asus\Desktop\Dot"
image= cv2.imread(r"C:\Users\Asus\Desktop\Dot")
os.chdir(image_path)
original_image= image

gray= cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)

edges= cv2.Canny(gray, 50,200)

contours, hierarchy= cv2.findContours(edges.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

sorted_contours= sorted(contours, key=cv2.contourArea, reverse= False)

for image_dot in Dir_Read('s', path=image_path):
    
    item = sorted_contours[image_dot]


    #largest item
    R= cv2.moments(item)


    coordinate_center= int(R['m10']/R['m00'])


    print("center coordinate ", str(coordinate_center))

    print("")


    plt.imshow(image)
    plt.show()
