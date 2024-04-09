import cv2
import matplotlib.pyplot as plt
from SolExDataCube import Dir_Read
import os
import re

image_path = r"C:\Users\Asus\Desktop\Dot"
os.chdir(image_path)

pattern = re.compile(r'(\d+)\.png')

for image_dot in Dir_Read('s', path=image_path):
    
    image= cv2.imread(image_dot)
    
    original_image= image

    gray= cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)

    edges= cv2.Canny(gray, 50,200)

    contours, hierarchy= cv2.findContours(edges.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    sorted_contours= sorted(contours, key=cv2.contourArea, reverse= False)
    
    try:
        item = sorted_contours[0]
        R = cv2.moments(item)
        coordinate_center = int(R['m10'] / R['m00'])
        
        print(image_dot)
        print("center coordinate : ", str(coordinate_center))
        print("*****************")
        
        sorted_contours = 0
        
        plt.imshow(image)
        plt.show()
        
    except:
        print(image_dot)
        print("Index out of range for file:", image_dot)
        print("*****************")