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
import tkinter as tk
from tkinter import ttk
from tkinter import *
from tkinter import font
import threading

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

error=[]
kp = 0
ki = 0
kd = 0
pos = 0

def main() :
    
    stop_event = threading.Event()
    
    try :
        #window setup
        window = tk.Tk()
        window.geometry("600x400") 
        window.title("Translation stage control 2024 V.0.1")
        
        bg = PhotoImage(file = 'C://Users//Asus//Desktop//INTERNSHIP_PROGRAM//BG_UI.png')
        canvas1 = Canvas( window, width = 600, height = 400)  
        canvas1.pack(fill = "both", expand = True) 
        canvas1.create_image( 0, 0, image = bg,anchor = "nw") 

        rectangle = canvas1.create_rectangle(50, 90, 350, 140, outline = "gray89", fill = "gray89") #(x1,y1,x2,y2)
        rectangle = canvas1.create_rectangle(50, 150, 350, 200, outline = "gray89", fill = "gray89") #(x1,y1,x2,y2)
        rectangle = canvas1.create_rectangle(50, 210, 350, 260, outline = "gray89", fill = "gray89") #(x1,y1,x2,y2)
        rectangle = canvas1.create_rectangle(50, 270, 350, 320, outline = "gray89", fill = "gray89") #(x1,y1,x2,y2)

        # Title
        title_label_kp = ttk.Label(master=window, text='KP', background ="gray89", font='CenturyGothic 10 bold' , foreground ="gray")
        title_label_kp.place(x = 60 , y = 90)
        title_label_ki = ttk.Label(master=window, text='KI',background ="gray89", font='CenturyGothic 10 bold' , foreground ="gray")
        title_label_ki.place(x = 60 , y = 150)
        title_label_kd = ttk.Label(master=window, text='KD',background ="gray89", font='CenturyGothic 10 bold' , foreground ="gray")
        title_label_kd.place(x = 60 , y = 210)
        title_label_pos = ttk.Label(master=window, text='FIRST POSITION',background ="gray89", font='CenturyGothic 10 bold' , foreground ="gray")
        title_label_pos.place(x = 60 , y = 270)

        # Input field
        entry_kp = ttk.Entry(master=window , background = "lightsteelblue4", foreground ="dodgerblue4" , justify= "center")
        entry_kp.place(x = 60 , y = 105 , width= 280, height=30)
        entry_ki = ttk.Entry(master=window, background = "lightsteelblue4", foreground ="dodgerblue4" , justify= "center" )
        entry_ki.place(x = 60 , y = 165, width= 280, height=30)
        entry_kd = ttk.Entry(master=window, background = "lightsteelblue4", foreground ="dodgerblue4" , justify= "center")
        entry_kd.place(x = 60 , y = 225 , width= 280, height=30)
        entry_pos = ttk.Entry(master=window, background = "lightsteelblue4", foreground ="dodgerblue4" , justify= "center" )
        entry_pos.place(x = 60 , y = 285 , width= 280, height=30)
        
        
        def stop():
            stop_event.set()
            print("Stop signal sent")

        def default():
            stop_event.clear()
            while not stop_event.is_set():
                new_pos = []
                pos = 55
                
                for path in Dir_Read('s', path=save_path):
                    if stop_event.is_set():  # Check if stop signal has been sent
                        break
                    print("----------------------------------------------")
                    print('Capturing image')
                    print("----------------------------------------------")
                    time.sleep(0.5)
                    disX = Draw_Contour(path)
                    reference = 0  # จุดที่แสงอยู่จุดศูนย์กลาง
                    err = PID(35, 2.5, 0.12, reference, disX)  # KP , KI , KD , จุดที่แสงอยู่จุดศูนย์กลาง (reference 0) , ระยะห่างจากจุดศูนย์กลางที่รับค่าจากกล้อง/เซนเซอร์
                    print("Error : " + str(err))
                    if err > reference:
                        new_position = pos - err
                        print("New_position : " + str(new_position))
                    elif err < reference:
                        new_position = pos + err
                        print("New_position : " + str(new_position))
                    else:
                        break
                    time.sleep(0.5)
            print("Default thread stopped")

        def default_app():
            r = threading.Thread(target=default)
            r.start()

        def enter():
            global KP, KI, KD, POS
            KP = entry_kp.get()
            KI = entry_ki.get()
            KD = entry_kd.get()
            POS = entry_pos.get()
            print("Kp : " + entry_kp.get())
            print("Ki : " + entry_ki.get())
            print("Kd : " + entry_kd.get())
            print("First Position : " + entry_pos.get())

        def start():
            stop_event.clear()
            while not stop_event.is_set():
                kp = float(KP)
                ki = float(KI)
                kd = float(KD)
                pos = float(POS)
                
                for path in Dir_Read('s', path=save_path):
                    if stop_event.is_set():  # Check if stop signal has been sent
                        break
                    print("----------------------------------------------")
                    print('Capturing image')
                    print("----------------------------------------------")
                    time.sleep(0.5)
                    disX = Draw_Contour(path)
                    reference = 0  # จุดที่แสงอยู่จุดศูนย์กลาง
                    err = PID(kp, ki, kd, reference, disX)  # KP , KI , KD , จุดที่แสงอยู่จุดศูนย์กลาง (reference 0) , ระยะห่างจากจุดศูนย์กลางที่รับค่าจากกล้อง/เซนเซอร์
                    print("Error : " + str(err))
                    if err > reference:
                        new_position = pos - err
                        print("New_position : " + str(new_position))
                    elif err < reference:
                        new_position = pos + err
                        print("New_position : " + str(new_position))
                    else:
                        break
                    time.sleep(0.5)
            print("Start thread stopped")       
            
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
                        width=15,
                        wraplength=100 )
        button.place(x = 400 , y = 100)
        
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
                        width=15,
                        wraplength=100 )
        button.place(x = 400 , y = 150)

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
                        width=15,
                        wraplength=100 )
        button.place(x = 400 , y = 200)

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
                        width=15,
                        wraplength=100 )
        button.place(x = 400 , y = 250)
        
        # Run the application
        window.mainloop()
        
    except Exception as e:
        print("ERROR:", e)
        
if __name__ == "__main__":
    main()   