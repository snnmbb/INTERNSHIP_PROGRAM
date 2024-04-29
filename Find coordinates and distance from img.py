import cv2 as cv
import cv2
import numpy as np
import os
import re
from matplotlib import pyplot as plt

image_ref = r"C:\Users\Asus\Desktop\REF_CAP.png"
image_path = r"C:\Users\Asus\Desktop\test_im_flip.png"
pattern = re.compile(r'(\d+)\.png')

try:
    # Read file
    dot1 = cv2.imread(image_ref)
    dot2 = cv2.imread(image_path)
    
    # Convert color to grayscale
    gray_dot1 = cv2.cvtColor(dot1, cv2.COLOR_BGR2GRAY)
    gray_dot2 = cv2.cvtColor(dot2, cv2.COLOR_BGR2GRAY)
    
    # Find contour
    ret, thresh1 = cv2.threshold(gray_dot1, 100, 500, cv2.THRESH_BINARY)
    ret, thresh2 = cv2.threshold(gray_dot2, 100, 500, cv2.THRESH_BINARY)

    contours1, _ = cv2.findContours(thresh1, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours2, _ = cv2.findContours(thresh2, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    if len(contours1) > 0 and len(contours2) > 0:
        
        cnt1 = contours1[0]
        cnt2 = contours2[0]

        x_ref,y_ref,w_ref,h_ref = cv2.boundingRect(cnt1)
        x,y,w,h = cv2.boundingRect(cnt2)

        # Create a mask
        mask1 = cv2.drawContours(gray_dot1, [cnt1], -1, 255, thickness=-1)
        mask2 = cv2.drawContours(gray_dot2, [cnt2], -1, 255, thickness=-1)
        
        # Bitwise AND operation
        mask_and = cv2.bitwise_and(mask1, mask2)
        
        # Generate "exclusive" masks, i.e. masks without the intersection parts
        mask1_excl = cv2.bitwise_xor(mask1, mask_and)
        mask2_excl = cv2.bitwise_xor(mask2, mask_and)
        mask2_ex = cv2.rectangle(mask2_excl, (x, y), (x+w_ref, y+h_ref), (255, 255, 0), 1)

        #Find center coordinates and distance
        cx_ref = ((x_ref+w_ref)+x_ref)/2   
        cy_ref = ((y_ref+h_ref)+y_ref)/2      
        center_x = ((x+w_ref)+x)/2
        center_y = ((y+h_ref)+y)/2
        distance_x = cx_ref-center_x
        distance_y = cy_ref-center_y
        
        print('center of ref - x : ' + str(cx_ref) + ' , y : '+ str(cy_ref))
        print('center of object - x : ' + str(center_x) + ' , y : '+ str(center_y))
        print("Distance between objects x : " + str(distance_x) + " , y : " + str(distance_y))
        
        # Show images
        plt.figure(figsize=(10,6))
        plt.subplot(3, 3, 1), plt.imshow(dot1, cmap='gray'), plt.xlabel('dot1')
        plt.subplot(3, 3, 2), plt.imshow(dot2, cmap='gray'), plt.xlabel('dot2')
        plt.subplot(3, 3, 3), plt.imshow(dot1+dot2, cmap='gray'), plt.xlabel('dot1+dot2')
        plt.subplot(3, 3, 4), plt.imshow(mask1, cmap='gray'), plt.xlabel('mask1')
        plt.subplot(3, 3, 5), plt.imshow(mask2, cmap='gray'), plt.xlabel('mask2')
        plt.subplot(3, 3, 6), plt.imshow(mask_and, cmap='gray'), plt.xlabel('mask_and')
        plt.subplot(3, 3, 7), plt.imshow(mask1_excl, cmap='gray'), plt.xlabel('mask1_excl')
        plt.subplot(3, 3, 8), plt.imshow(mask2_ex, cmap='gray'), plt.xlabel('mask2_excl')
        plt.show()
  
        
    else:
        print("No contours found.")
except Exception as e:
    print("ERROR:", e)
