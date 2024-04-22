import cv2 as cv
import cv2
import numpy as np
import os
import re
from matplotlib import pyplot as plt

image_path1 = r"C:\Users\Asus\Desktop\REF_CAP.png"
pattern = re.compile(r'(\d+)\.png')

image = cv2.imread(image_path1)

#cv2.imshow("image" , image)
#cv2.waitKey()

try :
    #Read file
    dot1 = cv2.imread(image_path1)
    
    #Convert color to grayscale
    gray_dot1 = cv2.cvtColor(dot1, cv2.COLOR_BGR2GRAY)
    
    #Find contour
    ret, thresh = cv2.threshold(gray_dot1, 127, 255, 0)
    contours1, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    cnt = contours1[0]
    
    if len(contours1) > 0:
        
        x,y,w,h = cv2.boundingRect(cnt)
        # Create a mask
        mask1 = cv2.drawContours(gray_dot1, [cnt], 0, 255, thickness=cv2.FILLED)
        mask1 = cv2.rectangle(dot1, (x, y), (x+w, y+h), (0, 255, 0), 2)
        
        # Bitwise AND operation
        mask_combined = cv2.bitwise_and(gray_dot1, gray_dot1)
        
        # Generate "exclusive" masks, i.e. masks without the intersection parts
        mask1_excl = cv2.bitwise_xor(gray_dot1, mask_combined)
        
        # Show images
        plt.figure(figsize=(10,6))
        plt.subplot(3, 3, 1), plt.imshow(gray_dot1, cmap='gray'), plt.xlabel('img1')
        plt.subplot(3, 3, 2), plt.imshow(mask1, cmap='gray'), plt.xlabel('mask1')
        plt.subplot(3, 3, 3), plt.imshow(mask1_excl, cmap='gray'), plt.xlabel('mask1_excl')
        plt.show()
        
    else:
        print("No contours found.")
except Exception as e:
    print("ERROR : ", e)
