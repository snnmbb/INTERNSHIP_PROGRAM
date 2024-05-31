import cv2 as cv
import cv2
import numpy as np
import os
import re
from matplotlib import pyplot as plt
import zwoasi as asi
import time
import sys
from SolExDataCube import Dir_Read
import clr
import sys
import tkinter as tk
from tkinter import ttk
from tkinter import *
from tkinter import font
import threading


#-----------------------------------------------SETUP CAMERA--------------------------------------------------------------------

window0 = tk.Tk()
window0.geometry("600x400") 
bg = PhotoImage(file = 'C://Users//Asus//Desktop//INTERNSHIP_PROGRAM//BG_UI.png')
canvas1 = Canvas( window0, width = 600, height = 400)  
canvas1.pack(fill = "both", expand = True) 
canvas1.create_image( 0, 0, image = bg,anchor = "nw") 
window0.title("Exposure time setup")

rectangle = canvas1.create_rectangle(50, 90, 350, 140, outline = "gray89", fill = "gray89") #(x1,y1,x2,y2)

title_label_kp = ttk.Label(master=window0, text='EXPOSURE', background ="gray89", font='CenturyGothic 10 bold' , foreground ="gray")
title_label_kp.place(x = 60 , y = 90)

entry_exp = ttk.Entry(master=window0 , background = "lightsteelblue4", foreground ="dodgerblue4" , justify= "center")
entry_exp.place(x = 60 , y = 105 , width= 280, height=30)

def EnterVal():
    global exposure
    exposure = entry_exp
    print("Exposue : " + entry_exp.get())

button = tk.Button(master=window0, text="ENTER", 
                        command=EnterVal,
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
button.place(x = 400 , y = 90)

window0.mainloop()
            
num_cameras = asi.get_num_cameras()
if num_cameras == 0:
    raise ValueError('No cameras found')

camera_id = 0  # use first camera from list
cameras_found = asi.list_cameras()
print(cameras_found)
camera = asi.Camera(camera_id)
camera_info = camera.get_camera_property()
print(camera_info)

# Get all of the camera controls
print('')
print('Camera controls:')
controls = camera.get_controls()
for cn in sorted(controls.keys()):
    print('    %s:' % cn)
    for k in sorted(controls[cn].keys()):
        print('        %s: %s' % (k, repr(controls[cn][k])))

# Use minimum USB bandwidth permitted
camera.set_control_value(asi.ASI_BANDWIDTHOVERLOAD, camera.get_controls()['BandWidth']['MinValue'])

# Set some sensible defaults. They will need adjusting depending upon
# the sensitivity, lens and lighting conditions used.
camera.disable_dark_subtract()

camera.set_control_value(asi.ASI_GAIN, 95) #ปรับค่าความละเอียด
camera.set_control_value(asi.ASI_EXPOSURE, 1000) #microseconds #ปรับค่าการรับแสง
camera.set_control_value(asi.ASI_WB_B, 0)  #ปรับค่าblue component of white balance
camera.set_control_value(asi.ASI_WB_R, 0) #ปรับค่าred component of white balance
camera.set_control_value(asi.ASI_GAMMA, 0) #ปรับค่าการเปลี่ยนสีจากสีดำเป็นสีขาว gamma with range 1 to 100 (nomnally 50)
camera.set_control_value(asi.ASI_BRIGHTNESS, 10)
camera.set_control_value(asi.ASI_FLIP, 0) #ปรับการหมุนรูป

#-----------------------------------------------SETUP LINEAR STAGE--------------------------------------------------------------------  
clr.AddReference("C:\\Program Files\\Thorlabs\\Kinesis\\Thorlabs.MotionControl.DeviceManagerCLI.dll.")
clr.AddReference("C:\\Program Files\\Thorlabs\\Kinesis\\Thorlabs.MotionControl.GenericMotorCLI.dll.")
clr.AddReference("C:\\Program Files\\Thorlabs\\Kinesis\\Thorlabs.MotionControl.KCube.BrushlessMotorCLI.dll.")
#clr.AddReference("C:\\Program Files\\Thorlabs\ \Kinesis\\ThorLabs.MotionControl.PositionReadoutEncoderCLI.dll")

from Thorlabs.MotionControl.DeviceManagerCLI import *
from Thorlabs.MotionControl.GenericMotorCLI import *
#from Thorlabs.MotionControl.PositionReadoutEncoderCLI import *
from Thorlabs.MotionControl.KCube.BrushlessMotorCLI import *
from System import Decimal


#-----------------------------------------------INITIALIZE--------------------------------------------------------------------
e_prev = Decimal(0)
error = []
new_pos = []
i = 0
pos = Decimal(55.0) # ตำแหน่งเริ่มต้นที่มอเตอร์ขยับไปให้แสงตกในกล้อง
new_position = pos
reference = Decimal(0)

image_ref = r"C:\Users\Asus\Desktop\LAB_TEST\REF\REF2.png"
save_path = r"C:\\Users\\Asus\\Desktop\LAB_TEST\DATA3\\"
asi.init('C:\\Users\\Asus\\AppData\\Local\\Programs\\Python\\Python310\\Lib\\ASI SDK\\lib\\x64\ASICamera2.lib')
pattern = re.compile(r'(\d+)\.png')
os.chdir(save_path)


#-----------------------------------------------PID FUNCTION--------------------------------------------------------------------
def PID(Kp , Ki , Kd , setpoint , measurement ): # measurement เป็นตำแหน่งที่จุด offset จากจุดศูนย์กลาง รับค่าจากกล้อง/เซนเซอร์....
    global time, e_prev# Value of offset - when the error is equal zero
    # PID calculations
    e = setpoint - measurement
    P = Kp*e
    I = Ki*(e+e_prev)
    D = Kd*(e-e_prev) 
    new_pos = P + I + D
    # update stored data for next iteration
    e_prev = e
    time_prev = time
    return new_pos

#-----------------------------------------------DRAW CONTOUR FUNCTION--------------------------------------------------------------------
def Draw_Contour(path) :
    dot1 = cv2.imread(image_ref)
    dot2 = cv2.imread(path)
    print('/n/nTest', path, 'Test/n/n')
    if dot2 is None:
        print(f"Error: Unable to load image at {path}")
        
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
            
            #print('sum', len(np.argwhere(mask_or == np.amax(mask_or))))
            
        print("-------------------------------------------------")
        print('center of ref - x : ' + str(cx_ref) + ' , y : '+ str(cy_ref))
        print('center of object - x : ' + str(center_x) + ' , y : '+ str(center_y))
        print("Distance between objects - x : " + str(distance_x) + " , y : " + str(distance_y))

        # Normalized
        CX_ref_nor = cx_ref/4656
        CY_ref_nor = cy_ref/3520
        center_x_nor = center_x/4656
        center_y_nor = center_y/3520
        disX_nor = distance_x/4656
        disY_nor = distance_y/3520
            
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
        
#-----------------------------------------------MAIN FUNCTION--------------------------------------------------------------------
def main():

    stop_event = threading.Event()
    
    try:
        
        #SETUP
        DeviceManagerCLI.BuildDeviceList()
        
        serial_num = str("28251928")  
        kcube = KCubeBrushlessMotor.CreateKCubeBrushlessMotor(serial_num)
        kcube.Connect(serial_num)

        #encoder =  ReadoutEncoder.CreatePositionReadoutEncoder(serial_num)
                
        time.sleep(0.25)
        kcube.StartPolling(250)
        time.sleep(0.25)  

        kcube.EnableDevice()
        time.sleep(0.25)  

       
        device_info = kcube.GetDeviceInfo()
        print(device_info.Description)

        
        if not kcube.IsSettingsInitialized():
            kcube.WaitForSettingsInitialized(10000)  
            assert kcube.IsSettingsInitialized() is True

        # Before homing or moving device, ensure the motors configuration is loaded
        m_config = kcube.LoadMotorConfiguration(serial_num,
                                                DeviceConfiguration.DeviceSettingsUseOptionType.UseDeviceSettings)

        time.sleep(1)
        kcube.MaxVelocity = Decimal(20)
        
        print("Homing Device...")
        kcube.Home(60000)  # 60 second timeout
        print("Device Homed")
        
        print('Enabling stills mode')
        
        try:
            # Force any single exposure to be halted
            camera.stop_video_capture()
            camera.stop_exposure()
        except (KeyboardInterrupt, SystemExit):
            raise
        
        
        #-------------------------------WINDOW VERSION----------------------------------------------
        # Window setting
        window = tk.Tk()
        window.geometry("600x400") 
        bg = PhotoImage(file = 'C://Users//Asus//Desktop//INTERNSHIP_PROGRAM//BG_UI.png')
        canvas1 = Canvas( window, width = 600, height = 400)  
        canvas1.pack(fill = "both", expand = True) 
        canvas1.create_image( 0, 0, image = bg,anchor = "nw") 
        window.title("Translation stage control 2024 V.0.2")

        rectangle = canvas1.create_rectangle(50, 90, 350, 140, outline = "gray89", fill = "gray89") #(x1,y1,x2,y2)
        rectangle = canvas1.create_rectangle(50, 150, 350, 200, outline = "gray89", fill = "gray89") #(x1,y1,x2,y2)
        rectangle = canvas1.create_rectangle(50, 210, 350, 260, outline = "gray89", fill = "gray89") #(x1,y1,x2,y2)
        rectangle = canvas1.create_rectangle(50, 270, 350, 320, outline = "gray89", fill = "gray89") #(x1,y1,x2,y2)

        # Title
        title_label_kp = ttk.Label(master=window, text='PROPORTIONAL', background ="gray89", font='CenturyGothic 10 bold' , foreground ="gray")
        title_label_kp.place(x = 60 , y = 90)
        title_label_ki = ttk.Label(master=window, text='INTEGRAL',background ="gray89", font='CenturyGothic 10 bold' , foreground ="gray")
        title_label_ki.place(x = 60 , y = 150)
        title_label_kd = ttk.Label(master=window, text='DERIVATIVE',background ="gray89", font='CenturyGothic 10 bold' , foreground ="gray")
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
        
        #Functions
        def Enter():
            global KP
            global KI
            global KD
            global POS
            KP = entry_kp.get()
            KI  = entry_ki.get()
            KD = entry_kd.get()
            POS = entry_pos.get()
            KP = float(KP)
            KI = float(KI)
            KD = float(KD)
            POS = float(POS)
            print("Kp : " + entry_kp.get())
            print("Ki : " + entry_ki.get())
            print("Kd : " + entry_kd.get())
            print("First Position : " + entry_pos.get())
            
        def Start() :
            
            i = 0
            stop_event.clear()
            while not stop_event.is_set():    
                
                

                pos = Decimal(POS)
                new_position = Decimal(POS)

                
                kcube.MoveTo(Decimal(POS), 7000)    
                  

                print("----------------------------------------------")
                print('Capturing image')
                if i < 10:
                    filename = '00'+ str(i)+'_image_lab.png'
                    camera.set_image_type(asi.ASI_IMG_RAW16)
                    camera.capture(filename=save_path+filename)
                    print('Saved to %s' % filename)
                    print("----------------------------------------------")
                else:
                    filename = '0'+ str(i)+'_image_lab.png'
                    camera.set_image_type(asi.ASI_IMG_RAW16)
                    camera.capture(filename=save_path+filename)
                    print('Saved to %s' % filename)
                    print("----------------------------------------------")
                   
                for path in Dir_Read('s', path=save_path):

                    time.sleep(0.5)
                    disX = Draw_Contour(path)
                        
                    PID_Out = PID(Decimal(KP) , Decimal(KI), Decimal(KD) , reference , Decimal(disX)) # KP , KI , KD , จุดที่แสงอยู่จุดศูนย์กลาง (reference 0) , ระยะห่างจากจุดศูนย์กลางที่รับค่าจากกล้อง/เซนเซอร์
                    print("Error : " + str(PID_Out))

                    if new_position <= Decimal(50.55 ) and new_position >= Decimal(50.5) :
                        print("New_position : " + str(new_position)    )
                        kcube.MoveTo(new_position, 7000)
                        return
                    elif PID_Out < reference: 
                        new_position = pos+PID_Out
                        print("New_position : " + str(new_position)    )
                        kcube.MoveTo(new_position, 7000)
                    elif  PID_Out > reference: 
                        new_position = pos-PID_Out
                        print("New_position : " + str(new_position)   )
                        kcube.MoveTo(new_position, 7000)
                    time.sleep(0.1)
                i+=1
                    
        def start_app() :
            t = threading.Thread(target=Start)
            t.start()
                        
        def Default() :
            
            i = 0
            stop_event.clear()
            while not stop_event.is_set():
                kcube.MoveTo(Decimal(60), 7000)

                
                new_position = Decimal(55)
                    
                
                    
                print("----------------------------------------------")
                print('Capturing image')
                if i < 10:
                    filename = '00'+ str(i)+'_image_lab.png'
                    camera.set_image_type(asi.ASI_IMG_RAW16)
                    camera.capture(filename=save_path+filename)
                    print('Saved to %s' % filename)
                    print("----------------------------------------------")
                else:
                    filename = '0'+ str(i)+'_image_lab.png'
                    camera.set_image_type(asi.ASI_IMG_RAW16)
                    camera.capture(filename=save_path+filename)
                    print('Saved to %s' % filename)
                    print("----------------------------------------------")
                    
                for path in Dir_Read('s', path=save_path):
                    if not stop_event.is_set() :
                        return
                    else:
                        
                        disX = Draw_Contour(path)
                            
                        PID_Out = PID(Decimal(32) , Decimal(0.5), Decimal(0.5) , reference , Decimal(disX)) # KP , KI , KD , จุดที่แสงอยู่จุดศูนย์กลาง (reference 0) , ระยะห่างจากจุดศูนย์กลางที่รับค่าจากกล้อง/เซนเซอร์
                        print("Error : " + str(PID_Out))

                        if new_position <= Decimal(50.55 ) and new_position >= Decimal(50.5) :
                            print("New_position : " + str(new_position)    )
                            kcube.MoveTo(new_position, 7000)
                            return
                        elif PID_Out < reference: 
                            new_position = pos+PID_Out
                            print("New_position : " + str(new_position)    )
                            kcube.MoveTo(new_position, 7000)
                        elif  PID_Out > reference: 
                            new_position = pos-PID_Out
                            print("New_position : " + str(new_position)   )
                            kcube.MoveTo(new_position, 7000)
                    time.sleep(0.1)
                i+=1
                    
        def default_app():
            r = threading.Thread(target=Default)
            r.start()
                    
        def home():
            stop_event.clear()
            while not stop_event.is_set():
                kcube.Home(6000)
                
        def home_app() :
            h = threading.Thread(target=home)
            h.start()
            
        def Stop():
            stop_event.set()
            print("Stop signal sent")
            
        # Button
        button = tk.Button(master=window, text="HOME", 
                        command=home_app,
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
        button.place(x = 400 , y = 90)
        
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
        button.place(x = 400 , y = 140)

        button = tk.Button(master=window, text="ENTER", 
                        command=Enter,
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
        button.place(x = 400 , y = 190)

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
        button.place(x = 400 , y = 240)
        
        button = tk.Button(master=window, text="STOP", 
                        command=Stop,
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
        button.place(x = 400 , y = 290)

        window.mainloop()
                    
    except Exception as e:
        print("ERROR:", e)    
        
#-----------------------------------------------------------------------------------------------------------------------------        
if __name__ == "__main__":
    main()