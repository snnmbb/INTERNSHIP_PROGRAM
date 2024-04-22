import cv2 as cv
import cv2
import numpy as np
import os
import re
from matplotlib import pyplot as plt

image_path1 = r"C:\Users\Asus\Desktop\test_im2_1.png"
image_path2 = r"C:\Users\Asus\Desktop\test_im2_ref.png"
pattern = re.compile(r'(\d+)\.png')

try:
    # Read file
    dot1 = cv2.imread(image_path1)
    dot2 = cv2.imread(image_path2)
    
    # Convert color to grayscale
    gray_dot1 = cv2.cvtColor(dot1, cv2.COLOR_BGR2GRAY)
    gray_dot2 = cv2.cvtColor(dot2, cv2.COLOR_BGR2GRAY)
    
    # Find contour
    ret, thresh1 = cv2.threshold(gray_dot1, 100, 255, cv2.THRESH_BINARY)
    ret, thresh2 = cv2.threshold(gray_dot2, 100, 255, cv2.THRESH_BINARY)

    contours1, _ = cv2.findContours(thresh1, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours2, _ = cv2.findContours(thresh2, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    if len(contours1) > 0 and len(contours2) > 0:
        
        cnt1 = contours1[0]
        cnt2 = contours2[0]

        x1,y1,w1,h1 = cv2.boundingRect(cnt1)
        x2,y2,w2,h2 = cv2.boundingRect(cnt2)

        # Create a mask
        mask1 = cv2.drawContours(gray_dot1, [cnt1], 0, 255, thickness=cv2.FILLED)
        mask2 = cv2.drawContours(gray_dot2, [cnt2], 0, 255, thickness=cv2.FILLED)
        
        # Bitwise AND operation
        mask_combined = cv2.bitwise_and(mask1, mask2)
        
        # Generate "exclusive" masks, i.e. masks without the intersection parts
        mask1_excl = cv2.bitwise_xor(mask1, mask_combined)
        mask2_excl = cv2.bitwise_xor(mask2, mask_combined)
        mask1_excl = cv2.rectangle(mask1_excl, (x1, y1), (x1+w1, y1+h1), (255, 0, 0), 2)

        # Show images
        plt.figure(figsize=(10,6))
        plt.subplot(3, 3, 1), plt.imshow(dot1, cmap='gray'), plt.xlabel('dot1')
        plt.subplot(3, 3, 2), plt.imshow(dot2, cmap='gray'), plt.xlabel('dot2')
        plt.subplot(3, 3, 3), plt.imshow(dot1+dot2, cmap='gray'), plt.xlabel('dot1+dot2')
        plt.subplot(3, 3, 4), plt.imshow(mask1, cmap='gray'), plt.xlabel('mask1')
        plt.subplot(3, 3, 5), plt.imshow(mask2, cmap='gray'), plt.xlabel('mask2')
        plt.subplot(3, 3, 6), plt.imshow(mask_combined, cmap='gray'), plt.xlabel('mask_combined')
        plt.subplot(3, 3, 7), plt.imshow(mask1_excl, cmap='gray'), plt.xlabel('mask1_excl')
        plt.subplot(3, 3, 8), plt.imshow(mask2_excl, cmap='gray'), plt.xlabel('mask2_excl')
        plt.show()
        
    else:
        print("No contours found.")
except Exception as e:
    print("ERROR:", e)
