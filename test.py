import cv2
import numpy as np
import os
import re


image_path = r"C:\Users\Asus\Desktop\REF_CAP.png"
image_path_new = r"C:\Users\Asus\Desktop\REF_CAP_W.png"
pattern = re.compile(r'(\d+)\.png')
directory = r'C:\Users\Asus\Desktop'
os.chdir(directory) 
image = cv2.imread(image_path)
image_new = cv2.imread(image_path_new)
original = image.copy()
src = cv2.imread(image_path, 1) 

#cv2.imshow("image",image)
#cv2.waitKey()

#save new image
hsv_img = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)  # rgb to hsv color space

s_ch = hsv_img[:, :, 1]  # Get the saturation channel

_,alpha = cv2.threshold(s_ch, 255, 0, cv2.THRESH_BINARY)  # Apply threshold - pixels above 5 are going to be 255, other are zeros.

b, g, r = cv2.split(src)

rgba = [b, g, r, alpha] 

dst = cv2.merge(rgba, 4) 

cv2.imwrite('REF_CAP_W.png', dst)  # Save the output image.


#draw boundingbox
gray = cv2.cvtColor(image_new, cv2.COLOR_BGR2GRAY)
thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY)[1]

ROI_number = 0
cnts = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
cnts = cnts[0] if len(cnts) == 2 else cnts[1]

for c in cnts:
    x, y, w, h = cv2.boundingRect(c)
    cv2.rectangle(image_new, (x, y), (x + w, y + h), (0, 0, 255), 1)

cv2.imshow("image", image)
cv2.imshow("Thresh", thresh)
cv2.waitKey()
