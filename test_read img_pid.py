import cv2 as cv
import cv2
import numpy as np
import os
import re
from matplotlib import pyplot as plt
import time
import sys
from SolExDataCube import Dir_Read
import csv


image_ref = r"C:\Users\Asus\Desktop\LAB_TEST\REF\REF.png"
save_path = r"C:\\Users\\Asus\\Desktop\LAB_TEST\DATA2"
pattern = re.compile(r'(\d+)\.png')
os.chdir(save_path)

e_prev = 0

def PID(Kp , Ki , Kd , setpoint , measurement ): # measurement เป็นตำแหน่งที่จุด offset จากจุดศูนย์กลาง รับค่าจากกล้อง/เซนเซอร์....
    global time, e_prev# Value of offset - when the error is equal zero
    # PID calculations
    e = setpoint - measurement
    P = Kp*e
    I = Ki+e
    D = Kd*(e-e_prev) 
    pid = P + I + D
    # update stored data for next iteration
    e_prev = e
    time_prev = time
    return pid

def Draw_Contour(path) :
    dot1 = cv2.imread(image_ref)
    dot2 = cv2.imread(path)
        
    wid = dot1.shape[1] 
    hgt = dot1.shape[0] 
        
    print('image pixels size = ' , str(wid) + " x " + str(hgt))
    
    # Convert color to grayscale
    gray_dot1 = cv2.cvtColor(dot1, cv2.COLOR_BGR2GRAY)
    gray_dot2 = cv2.cvtColor(dot2, cv2.COLOR_BGR2GRAY)
    combine_dot = cv2.bitwise_or(gray_dot1, gray_dot2)
        
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
            
        print('w_ref = ',w_ref)
        print('h_ref = ',h_ref)
        print('x_ref = ',x_ref)
        print('y_ref = ',y_ref)

        print('w = ',w)
        print('h = ',h)
        print('x = ',x)
        print('y = ',y)

        # Create a mask
        mask1 = cv2.drawContours(gray_dot1, [cnt1], -1, 255, thickness=-1)
        mask2 = cv2.drawContours(gray_dot2, [cnt2], -1, 255, thickness=-1)
            
        # Bitwise AND operation
        mask_and = cv2.bitwise_and(mask1, mask2)
        mask_or = cv2.bitwise_or(mask1,mask2)
            
        # Generate "exclusive" masks, i.e. masks without the intersection parts
        mask1_excl = cv2.bitwise_xor(mask1, mask_and)
        mask2_excl = cv2.bitwise_xor(mask2, mask_and)
        mask2_ex = cv2.rectangle(mask2_excl, (x, y), (x+w, y+h), (255, 255, 0), 1)

        #Find center coordinates and distance
        cx_ref = ((x_ref+w_ref)+x_ref)/2   
        cy_ref = ((y_ref+h_ref)+y_ref)/2      
        center_x = ((x+w_ref)+x)/2
        center_y = ((y+h_ref)+y)/2
        distance_x = cx_ref-center_x
        distance_y = cy_ref-center_y
                        
        print("-------------------------------------------------")
        print('center of ref - x : ' + str(cx_ref) + ' , y : '+ str(cy_ref))
        print('center of object - x : ' + str(center_x) + ' , y : '+ str(center_y))
        print("Distance between objects - x : " + str(distance_x) + " , y : " + str(distance_y))

        # Normalized
        CX_ref_nor = cx_ref*0.00038
        CY_ref_nor = cy_ref*0.00038
        center_x_nor = center_x*0.00038
        center_y_nor = center_y*0.00038
        disX_nor = distance_x*0.00038
        disY_nor = distance_y*0.00038
            
        print("--------------------Normalize--------------------")
        print('CX_ref = ' , CX_ref_nor)
        print('CY_ref = ' , CY_ref_nor)
        print('center_x = ' , center_x_nor)
        print('center_Y = ' , center_y_nor)
        print('disX = ' , disX_nor)
        print('disY = ' , disY_nor)
        print("-------------------------------------------------")
                
        '''
        #comment when using linear stage
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
        '''
        return disX_nor
    else:
         print("No contours found.")  

error=[]


def main() :
    try :
        pos = 52 #ตำแหน่งที่ทำให้แสงอยู่ใกล้เคียงกับRefที่สุด
        new_position = pos
        new_pos = []
        
        for path in Dir_Read('s', path=save_path):
            print("----------------------------------------------")
            print('Capturing image')
            print("----------------------------------------------")
            time.sleep(0.5)
            disX = Draw_Contour(path)
            reference = 0 #จุดที่แสงอยู่จุดศูนย์กลาง               
            err = PID(0.5, 0.04, 0.8, reference , disX) # KP , KI , KD , จุดที่แสงอยู่จุดศูนย์กลาง (reference 0) , ระยะห่างจากจุดศูนย์กลางที่รับค่าจากกล้อง/เซนเซอร์
            print("Error : " + str(err))
            if err> reference :
                new_position = pos-err
                print("New_position : " + str(new_position)   ) 
            elif new_position < reference: 
                new_position = pos+err
                print("New_position : " + str(new_position)    )
            else :
                break
            time.sleep(0.5)
            error.append(err)
            new_pos.append(new_position)
            
            with open('C://Users/Asus/Desktop/LAB_TEST/result.csv', 'w', encoding='UTF8', newline='') as f:  
                writer = csv.writer(f)
                for err_value in error:
                    writer.writerow([err_value])
                '''
                for newpos_value in new_pos:
                    writer.writerow([newpos_value])
                '''
            
            '''
            plt.subplot(1, 2, 1)
            plt.plot(error)
            plt.xlabel('Index')
            plt.ylabel('ERR')
            
            plt.subplot(1, 2, 2)
            plt.plot(new_pos)
            plt.xlabel('Index')
            plt.ylabel('NEW_POSITION')
            
            plt.tight_layout()
            plt.gca().invert_yaxis()
            plt.show()
            '''
            
    except Exception as e:
        print("ERROR:", e)

if __name__ == "__main__":
    main()   