import matplotlib.pyplot as plt
import numpy as np
import cv2
from SolExDataCube import Dir_Read
import os
import re

image_path= r"C:\Users\Asus\Desktop\Dot\Dot"
os.chdir(image_path)

pattern = re.compile(r'(\d+)\.png')

for image_dot in Dir_Read('s', path=image_path):

    image= cv2.imread(image_dot)

    original_image= image

    gray= cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)

    edges= cv2.Canny(gray, 40,200)
    
    contours, hierarchy= cv2.findContours(edges.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    sorted_contours= sorted(contours, key=cv2.contourArea, reverse= False)
    
    try:     

        dot1= sorted_contours[0]
        
        M = cv2.moments(dot1)

        (x,y),radius = cv2.minEnclosingCircle(dot1)
        
        center = (int(x),int(y))
        radius = int(radius)
        xcoordinate1 = x
        xcoordinate2 = x+radius
        
        # Creating a 2D histogram (hexbin plot)
        plt.hexbin(xcoordinate1, xcoordinate2, gridsize=30, cmap='Blues')
        
        # Adding labels and title
        plt.xlabel('X coordinate1')
        plt.ylabel('X coorsinate2')
        plt.title('2D Histogram (Hexbin Plot)')
        
        # Adding colorbar
        plt.colorbar()
        
        # Display the plot
        plt.show()
        
    except:
        print(image_dot)
        print("Index out of range for file:", image_dot)
        print("***************************************")
