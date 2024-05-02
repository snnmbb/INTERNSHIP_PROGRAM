import cv2
import numpy as np
import os
import re
from matplotlib import pyplot as plt
from PIL import Image


image_ref = r"C:\Users\Asus\Desktop\LAB_TEST\REF\REF.png"
pattern = re.compile(r'(\d+)\.png')

try :
    REF = cv2.imread(image_ref)
    
    wid = REF.shape[1] 
    hgt = REF.shape[0]
     
    print('image pixels size = ' , str(wid) + " x " + str(hgt))

    gray_ref = cv2.cvtColor(REF, cv2.COLOR_BGR2GRAY)
    
    ret, thresh1 = cv2.threshold(gray_ref, 100, 500, cv2.THRESH_BINARY)
    
    contours1, _ = cv2.findContours(thresh1, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    
    cnt1 = contours1[0]

    x,y,w,h = cv2.boundingRect(cnt1)
    
    print('w = ',w)
    print('h = ',h)
    print('x = ',x)
    print('y = ',y)

    
    if len(contours1) > 0 :
        REF_bound = cv2.rectangle(gray_ref, (x, y), (x+w, y+h), (255, 0, 0), 1)
        
        center_x = ((x+w)+x)/2
        center_y = ((y+h)+y)/2
        
        print('center of ref - x : ' + str(center_x) + ' , y : '+ str(center_y))
        
        REF_coordinateX = cv2.line(gray_ref, (int(center_x),0), (int(center_x),3520), (255,255,255), 1)
        REF_coordinateY = cv2.line(gray_ref, (0,int(center_y)), (4656,int(center_y)), (255,255,255), 1)
        
        # Normalized
        CX_nor = center_x/4656
        CY_nor = center_y/3520

        file_ref = open(r"C:\Users\Asus\Desktop\LAB_TEST\REF_coordinates.txt" , "w")
        file_ref.write('center of ref - x : ' + str(center_x) + ' , y : '+ str(center_y))
        file_ref.write('//Normalized : center of ref - x : ' + str(CX_nor) + ' , y : '+ str(CY_nor))
        file_ref.close() 
        
        plt.figure(figsize=(5,5))
        plt.imshow(REF_bound,cmap='gray')
        plt.show()
    else:
        print("No contours found.")
    
except Exception as e:
    print("ERROR:", e)