import tkinter as tk
from tkinter import ttk
from tkinter import *
from tkinter import font
import threading
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
    global time_prev, e_prev# Value of offset - when the error is equal zero
    # PID calculations
    e = setpoint - measurement
    P = Kp*e
    I = Ki*(e+e_prev)
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
                
        return disX_nor
    else:
         print("No contours found.")  
         
e_prev = 0
error = []
new_pos = []
i = 0
pos = 55.0 # ตำแหน่งเริ่มต้นที่มอเตอร์ขยับไปให้แสงตกในกล้อง
new_position = pos
reference = 0
kp = 0
ki = 0
kd = 0
pos = 0


def main() :
    
    status = False
    
    try :
        #window setup
        window = tk.Tk()
        window.geometry("600x400") 
        window.title("Translation stage control 2024 V.0.3")
        
        bg = PhotoImage(file = 'C://Users//Asus//Desktop//INTERNSHIP_PROGRAM//UI_v3.png')
        canvas1 = Canvas( window, width = 600, height = 400)  
        canvas1.pack(fill = "both", expand = True) 
        canvas1.create_image( 0, 0, image = bg,anchor = "nw") 

        # Input field
        entry_kp = ttk.Entry(master=window , background = "lightsteelblue4", foreground ="dodgerblue4" , justify= "center")
        entry_kp.insert(0,"32")
        entry_kp.place(x = 305 , y = 120, width= 120, height=30)      
        
        entry_ki = ttk.Entry(master=window, background = "lightsteelblue4", foreground ="dodgerblue4" , justify= "center" )
        entry_ki.insert(0,"0.5")
        entry_ki.place(x = 305 , y = 175, width= 120, height=30)
        
        entry_kd = ttk.Entry(master=window, background = "lightsteelblue4", foreground ="dodgerblue4" , justify= "center")
        entry_kd.insert(0,"0.5")
        entry_kd.place(x = 305 , y = 230 , width= 120, height=30)
        
        entry_pos = ttk.Entry(master=window, background = "lightsteelblue4", foreground ="dodgerblue4" , justify= "center" )
        entry_pos.insert(0,"60")
        entry_pos.place(x = 305 , y = 290 , width= 120, height=30)
        
        
        def stop() :
            global status
            status = True
            print("stop")
            
        def default() :
            global status 
            status = False
            while(status == False) :
                print("default")
                
        def default_app() :
            t = threading.Thread(target=default)
            t.start()          
                            
        def enter():
            global KP,KI,KD,POS,new_position
            Kp = entry_kp.get()
            Ki  = entry_ki.get()
            Kd = entry_kd.get()
            Pos = entry_pos.get()
            KP = float(Kp)
            KI = float(Ki)
            KD = float(Kd)
            POS = float(Pos)
            
            if POS > 70 or POS < 40 or KP > 35 or KP < 25 or KI > 1 or KI < 0 or KD > 0.5 or KD < 0  :
                top= Toplevel(window)
                top.geometry("400x150")
                top.title("Warning Window")
                Label(top, text= "Values out of range!", font=('CenturyGothic 20 bold')).place(x=60,y=60)
                KP = 0
                KI  = 0 
                KD = 0
                POS = 0
            else :
                KP = float(entry_kp.get())
                KI  = float(entry_ki.get())
                KD = float(entry_kd.get())
                POS = float(entry_pos.get())
                print("Kp : " + entry_kp.get())
                print("Ki : " + entry_ki.get())
                print("Kd : " + entry_kd.get())
                print("First Position : " + entry_pos.get()) 
        
        def  start() :
            global status 
            status = False
            new_position = POS
            while(status == False) :
                for path in Dir_Read('s', path=save_path):
                    if status:
                        break  # Exit if status is True
                    else :
                        time.sleep(0.1)
                        disX = Draw_Contour(path)
                            
                        PID_Out = PID(KP , KI, KD , reference , disX) # KP , KI , KD , จุดที่แสงอยู่จุดศูนย์กลาง (reference 0) , ระยะห่างจากจุดศูนย์กลางที่รับค่าจากกล้อง/เซนเซอร์
                        print("Error : " + str(PID_Out))
                    
                        if PID_Out <= 5.55  and PID_Out >= 0.5 :
                            print("New_position : " + str(new_position)    )
                            return
                        elif PID_Out < reference: 
                            new_position = pos+PID_Out
                            print("New_position : " + str(new_position)    )
                        elif  PID_Out > reference: 
                            new_position = pos-PID_Out
                            print("New_position : " + str(new_position)   )
                    time.sleep(0.1)
                    
                    error.append(PID_Out)
                    new_pos.append(new_position)
                    with open('C://Users/Asus/Desktop/LAB_TEST/result.csv', 'w', newline='') as csvfile:
                        fieldnames = ["PID Output", "New position"]
                        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                        writer.writeheader()

                        for err_value, new_position in zip(error, new_pos):
                            writer.writerow({"PID Output": err_value, "New position": new_position})

        def start_app() :
            t = threading.Thread(target=start)
            t.start()
               
            
        # Button
        
        button = tk.Button(master=window, text="DEFAULT", 
                        command=default_app,
                        activebackground="dodgerblue4", 
                        activeforeground="white",
                        anchor="center",
                        bd=3,
                        bg="slategray3",
                        cursor="hand2",
                        disabledforeground="lightsteelblue1",
                        fg="black",
                        font=("CenturyGothic", 12),
                        height=1,
                        highlightbackground="white",
                        highlightcolor="lightgray",
                        highlightthickness=2,
                        justify="center",
                        overrelief="raised",
                        padx=10,
                        pady=5,
                        width=10,
                        wraplength=100 )
        button.place(x = 460 , y = 120)
        
        button = tk.Button(master=window, text="ENTER", 
                        command=enter,
                        activebackground="dodgerblue4", 
                        activeforeground="white",
                        anchor="center",
                        bd=3,
                        bg="slategray3",
                        cursor="hand2",
                        disabledforeground="lightsteelblue1",
                        fg="black",
                        font=("CenturyGothic", 12),
                        height=1,
                        highlightbackground="white",
                        highlightcolor="lightgray",
                        highlightthickness=2,
                        justify="center",
                        overrelief="raised",
                        padx=10,
                        pady=5,
                        width=10,
                        wraplength=100 )
        button.place(x = 460 , y = 170)

        button = tk.Button(master=window, text="START", 
                        command=start_app,
                        activebackground="dodgerblue4", 
                        activeforeground="white",
                        anchor="center",
                        bd=3,
                        bg="slategray3",
                        cursor="hand2",
                        disabledforeground="lightsteelblue1",
                        fg="black",
                        font=("CenturyGothic", 12),
                        height=1,
                        highlightbackground="white",
                        highlightcolor="lightgray",
                        highlightthickness=2,
                        justify="center",
                        overrelief="raised",
                        padx=10,
                        pady=5,
                        width=10,
                        wraplength=100 )
        button.place(x = 460 , y = 220)

        button = tk.Button(master=window, text="STOP", 
                        command=stop,
                        activebackground="dodgerblue4", 
                        activeforeground="white",
                        anchor="center",
                        bd=3,
                        bg="slategray3",
                        cursor="hand2",
                        disabledforeground="lightsteelblue1",
                        fg="black",
                        font=("CenturyGothic", 12),
                        height=1,
                        highlightbackground="white",
                        highlightcolor="lightgray",
                        highlightthickness=2,
                        justify="center",
                        overrelief="raised",
                        padx=10,
                        pady=5,
                        width=10,
                        wraplength=100 )
        button.place(x = 460 , y = 270)
        
        # Run the application
        window.mainloop()
        
    except Exception as e:
        print("ERROR:", e)
        
if __name__ == "__main__":
    main()   