import cv2
import numpy as np
import os
import re

image_path= r"C:\Users\Asus\Desktop\test_im2_1.png"
pattern = re.compile(r'(\d+)\.png')
directory = r'C:\Users\Asus\Desktop'
os.chdir(directory) 

image = cv2.imread(image_path)

# Fill the black background with white color
#cv2.floodFill(image, None, seedPoint=(0, 0), newVal=(0, 0, 255), loDiff=(2, 2, 2), upDiff=(2, 2, 2))  # Not working!

