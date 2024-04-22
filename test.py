import cv2
import numpy as np
import os
import re


image_path = r"C:\Users\Asus\Desktop\test_im2_1.png"
image_path_new = r"C:\Users\Asus\Desktop\test_im2_w.png"
pattern = re.compile(r'(\d+)\.png')
directory = r'C:\Users\Asus\Desktop'
os.chdir(directory) 
image = cv2.imread(image_path)
image_new = cv2.imread(image_path_new)
original = image.copy()

#save new image
hsv_img = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)  # rgb to hsv color space

s_ch = hsv_img[:, :, 1]  # Get the saturation channel

thesh = cv2.threshold(s_ch, 5, 255, cv2.THRESH_BINARY)[1]  # Apply threshold - pixels above 5 are going to be 255, other are zeros.
thesh = cv2.morphologyEx(thesh, cv2.MORPH_OPEN, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (7, 7)))  # Apply opening morphological operation for removing artifacts.

cv2.floodFill(thesh, None, seedPoint=(0, 0), newVal=128, loDiff=1, upDiff=1)  # Fill the background in thesh with the value 128 (pixel in the foreground stays 0.

image[thesh == 128] = (255, 255, 255)  # Set all the pixels where thesh=128 to red.

cv2.imwrite('test_im2_w.png', image)  # Save the output image.

#draw boundingbox
gray = cv2.cvtColor(image_new, cv2.COLOR_BGR2GRAY)
thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

ROI_number = 0
cnts = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cnts = cnts[0] if len(cnts) == 2 else cnts[1]

for c in cnts:
    x, y, w, h = cv2.boundingRect(c)
    cv2.rectangle(image_new, (x, y), (x + w, y + h), (0, 0, 255), 2)

cv2.imshow("image", image_new)
cv2.imshow("Thresh", thresh)
cv2.waitKey()