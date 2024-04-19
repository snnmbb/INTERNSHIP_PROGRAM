import cv2 as cv
import cv2
import numpy as np
import os
import re
from matplotlib import pyplot as plt

image_path1 = r"C:\Users\Asus\Desktop\test_im2_1.png"
image_path2 = r"C:\Users\Asus\Desktop\test_im2_ref.png"
pattern = re.compile(r'(\d+)\.png')

try :
    font = cv2.FONT_HERSHEY_COMPLEX 
    #Read file
    dot1 = cv2.imread(image_path1)
    dot2 = cv2.imread(image_path2)
    
    #Convert color to grayscale
    gray_dot1 = cv2.cvtColor(dot1, cv2.COLOR_BGR2GRAY)
    gray_dot2 = cv2.cvtColor(dot2, cv2.COLOR_BGR2GRAY)
    
    #Find contour
    contours1, _ = cv2.findContours(gray_dot1, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    contours2, _ = cv2.findContours(gray_dot2, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    
    if len(contours1) > 0:
        # Create a mask
        mask1 = cv2.drawContours(np.zeros_like(gray_dot1), [contours1[0]], -1, 255, cv2.FILLED)
        mask2 = cv2.drawContours(np.zeros_like(gray_dot2), [contours2[0]], -1, 255, cv2.FILLED)
        
        # Bitwise AND operation
        mask_combined = cv2.bitwise_and(mask1, mask2)
        
        # Generate "exclusive" masks, i.e. masks without the intersection parts
        mask1_excl = cv2.bitwise_xor(mask1, mask_combined)
        mask2_excl = cv2.bitwise_xor(mask2, mask_combined)

        # Show images
        plt.figure()
        plt.subplot(3, 3, 1), plt.imshow(dot1), plt.xlabel('img1')
        plt.subplot(3, 3, 2), plt.imshow(dot2), plt.xlabel('Reference')
        plt.subplot(3, 3, 3), plt.imshow(dot1 + dot2), plt.xlabel('img1 + reference')
        plt.subplot(3, 3, 4), plt.imshow(mask1, cmap='gray'), plt.xlabel('mask1')
        plt.subplot(3, 3, 5), plt.imshow(mask2, cmap='gray'), plt.xlabel('mask2')
        plt.subplot(3, 3, 6), plt.imshow(mask_combined, cmap='gray'), plt.xlabel('mask_combined')
        plt.subplot(3, 3, 7), plt.imshow(mask1_excl, cmap='gray'), plt.xlabel('mask1_excl')
        plt.subplot(3, 3, 8), plt.imshow(mask2_excl, cmap='gray'), plt.xlabel('mask2_excl')
        plt.subplot(3, 3, 9), plt.imshow(mask_combined, cmap='gray'), plt.xlabel('mask_combined')
        plt.show()
        
    else:
        print("No contours found.")
except Exception as e:
    print("ERROR : ", e)