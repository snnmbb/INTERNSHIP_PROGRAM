import cv2
import numpy as np
import os
import re

image_path2 = r"C:\Users\Asus\Desktop\test_im2_1.png"
pattern = re.compile(r'(\d+)\.png')
image = cv2.imread(image_path2)
original = image.copy()

gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

ROI_number = 0
cnts = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cnts = cnts[0] if len(cnts) == 2 else cnts[1]
for c in cnts:
    x, y, w, h = cv2.boundingRect(c)
    cv2.rectangle(image, (x, y), (x + w, y + h), (0, 0, 255), 2)

cv2.imshow("image", image)
cv2.imshow("Thresh", thresh)
cv2.waitKey()