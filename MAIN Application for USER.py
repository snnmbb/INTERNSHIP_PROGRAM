import cv2 as cv
import cv2
import numpy as np
import os
import re
from matplotlib import pyplot as plt
import zwoasi as asi
import time
import sys
import clr
import sys
import tkinter as tk
from tkinter import ttk
from tkinter import *
from tkinter import font
import threading
import csv

#-----------------------------------------------SETUP CAMERA--------------------------------------------------------------------
print ("---------------------------------SETTING CAMERA--------------------------------------")           
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
print ("---------------------------------FINISHED SETTING CAMERA--------------------------------------")           

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

pos = Decimal(55.0) # ตำแหน่งเริ่มต้นที่มอเตอร์ขยับไปให้แสงตกในกล้อง
new_position = pos
reference = Decimal(0)

global distance_X  
global error      
global new_pos 
global kp
global ki
global kd
global j
distance_X = []  
error = []      
new_pos = []
kp = []
ki = []
kd = []       
j = 0    

image_ref = r"C:\Users\Asus\Desktop\LAB_TEST\REF\REF1.png"
save_path = r"C:\\Users\\Asus\\Desktop\LAB_TEST\REAL_DATA\\"
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
    if new_pos > reference :
        new_pos = -new_pos
    elif new_pos < reference :
        new_pos = new_pos
    else :
        new_pos = reference
    return new_pos , P , I , D

#-----------------------------------------------DRAW CONTOUR FUNCTION--------------------------------------------------------------------
def Draw_Contour(image) :
    dot1 = cv2.imread(image_ref,1)
    dot2 = image
        
    wid = dot1.shape[1] 
    hgt = dot1.shape[0] 
    
    # Convert color to grayscale
    gray_dot1 = cv2.cvtColor(dot1, cv2.COLOR_BGR2GRAY)
    gray_dot2 = dot2

    
    combine_dot = cv2.bitwise_or(gray_dot1, gray_dot2)
        
    # Find contour
    ret, thresh1 = cv2.threshold(gray_dot1, 150, 200, cv2.THRESH_BINARY)
    ret, thresh2 = cv2.threshold(gray_dot2, 100, 500, cv2.THRESH_BINARY)
    
    contours1, _ = cv2.findContours(thresh1, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours2, _ = cv2.findContours(thresh2, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    if len(contours1) > 0 and len(contours2) > 0:   
        cnt1 = max(contours1, key=cv2.contourArea)
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
        center_x = ((x+w_ref)+x)/2
        distance_x = cx_ref-center_x
            
        print("-------------------------------------------------")
        print('center of ref - x : ' + str(cx_ref)  )
        print('center of object - x : ' + str(center_x))
        print("Distance between objects - x : " + str(distance_x))

        # Normalized
        CX_ref_nor = cx_ref/4656
        center_x_nor = center_x/4656
        disX_nor = distance_x/4656            
        print("--------------------Normalize--------------------")
        print('CX_ref = ' , CX_ref_nor)
        print('center_x = ' , center_x_nor)
        print('distance_X = ' , disX_nor)
        print("-------------------------------------------------")
                
        return disX_nor
    else:
         print("No contours found.")  
        
#-----------------------------------------------MAIN FUNCTION--------------------------------------------------------------------
def main():

    status = False
    
    try:
        print ("---------------------------------HOMING DEVIEC--------------------------------------")           

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
        kcube.Home(40000) 
        print("Device Homed")
        print ("---------------------------------FINISHED HOMING DEVIEC--------------------------------------")           
        
        try:
            # Force any single exposure to be halted
            camera.stop_video_capture()
            camera.stop_exposure()
        except (KeyboardInterrupt, SystemExit):
            raise
        
        #-------------------------------WINDOW VERSION----------------------------------------------
        # Window setting
        #window setup
        window = tk.Tk()
        window.geometry("600x400") 
        window.title("Translation stage control 2024 User Edition")
        
        bg = PhotoImage(file = 'C://Users//Asus//Desktop//INTERNSHIP_PROGRAM//UI_v3.png')
        canvas1 = Canvas( window, width = 600, height = 400)  
        canvas1.pack(fill = "both", expand = True) 
        canvas1.create_image( 0, 0, image = bg,anchor = "nw") 

        # Input field
        entry_kp = ttk.Entry(master=window , background = "lightsteelblue4", foreground ="dodgerblue4" , justify= "center")
        entry_kp.insert(0,"10")
        entry_kp.place(x = 305 , y = 120, width= 120, height=30)      
        
        entry_ki = ttk.Entry(master=window, background = "lightsteelblue4", foreground ="dodgerblue4" , justify= "center" )
        entry_ki.insert(0,"0.1")
        entry_ki.place(x = 305 , y = 175, width= 120, height=30)
        
        entry_kd = ttk.Entry(master=window, background = "lightsteelblue4", foreground ="dodgerblue4" , justify= "center")
        entry_kd.insert(0,"0.2")
        entry_kd.place(x = 305 , y = 230 , width= 120, height=30)
        
        entry_pos = ttk.Entry(master=window, background = "lightsteelblue4", foreground ="dodgerblue4" , justify= "center" )
        entry_pos.insert(0,"60")
        entry_pos.place(x = 305 , y = 290 , width= 120, height=30)
        
        #Functions
        def Enter():
            global KP,KI,KD,POS,new_position
            Kp = entry_kp.get()
            Ki  = entry_ki.get()
            Kd = entry_kd.get()
            Pos = entry_pos.get()
            KP = float(Kp)
            KI = float(Ki)
            KD = float(Kd)
            POS = float(Pos)
            
            if POS > 70 or POS < 40 or KP > 35 or KP < 0 or KI > 5 or KI < 0 or KD > 5 or KD < 0  :
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
            
        def Start() :
            
            print ("************************************* START POSITIONING ***************************************")           
            
            global status 
            status = False
            global distance_X  
            global error      
            global new_pos 
            global kp
            global ki
            global kd
            global j
            distance_X = []  
            error = []      
            new_pos = []
            kp = []
            ki = []
            kd = []    
            j = 0
            new_position = POS
            pos = Decimal(POS)
            new_position = Decimal(POS)
            kcube.MoveTo(Decimal(POS), 7000)

            while(status == False) :             
                
                time.sleep(0.5)
                print("----------------------------------------------")
                print('Capturing image')
                if j < 10:
                    filename = '00'+ str(j)+'_image_lab.png'
                else:
                    filename = '0'+ str(j)+'_image_lab.png'
                camera.set_image_type(asi.ASI_IMG_RAW8)
                img = camera.capture(filename=save_path+filename)
                print('Saved to %s' % filename)
                print("----------------------------------------------")
                j+=1
                                    
                if status:
                    break
                else:
                    disX = Draw_Contour(img)
                    
                    if disX is not None:  # Ensure disX has a value
                        if isinstance(distance_X, list):
                            distance_X.append(disX)  # Append to distanceX list
                    
                    
                        all_PID_Output = PID(Decimal(10), Decimal(0.1), Decimal(0.2), reference, Decimal(disX))
                        PID_Out = all_PID_Output[0]
                        p = all_PID_Output[1]
                        i = all_PID_Output[2]
                        d = all_PID_Output[3]
                        print("Error : " + str(PID_Out))
                        
                        new_position = PID_Out+kcube.Position #pos
                        print("New_position : " + str(new_position))
                        kcube.MoveTo(new_position, 7000)
                        
                        if PID_Out == Decimal(0) :
                            new_position = PID_Out+kcube.Position #pos
                            print("New_position : " + str(new_position))
                            kcube.MoveTo(new_position, 7000)
                        
                            if isinstance(error, list):
                                error.append(PID_Out) 

                            if isinstance(new_pos, list):
                                new_pos.append(new_position)
                                
                            if isinstance(kp, list):
                                kp.append(p)  

                            if isinstance(ki, list):
                                ki.append(i)  
                                
                            if isinstance(kd, list):
                                kd.append(d)   
                                                                                
                            with open('C://Users/Asus/Desktop/LAB_TEST/result.csv', 'w', newline='') as csvfile:
                                fieldnames = ["PID Output", "distanceX", "New position" , "KP" , "KI" , "KD"]
                                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                                writer.writeheader()

                                for err_value, distX, newPos,K_P,K_I,K_D in zip(error, distance_X, new_pos,kp,ki,kd):  # Corrected variable names
                                    writer.writerow({"PID Output": err_value, "distanceX": distX, "New position": newPos
                                    ,"KP":K_P ,"KI" :K_I ,"KD" : K_D})
                                    
                            print("*****************************FINISHED POSITIONG AT "+str(new_position)+"*********************************")   
                            return  
                        else :
                            if isinstance(error, list):
                                error.append(PID_Out) 

                            if isinstance(new_pos, list):
                                new_pos.append(new_position)
                                
                            if isinstance(kp, list):
                                kp.append(p)  

                            if isinstance(ki, list):
                                ki.append(i)  
                                
                            if isinstance(kd, list):
                                kd.append(d)   
                                                                                
                            with open('C://Users/Asus/Desktop/LAB_TEST/result.csv', 'w', newline='') as csvfile:
                                fieldnames = ["PID Output", "distanceX", "New position" , "KP" , "KI" , "KD"]
                                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                                writer.writeheader()

                                for err_value, distX, newPos,K_P,K_I,K_D in zip(error, distance_X, new_pos,kp,ki,kd):  # Corrected variable names
                                    writer.writerow({"PID Output": err_value, "distanceX": distX, "New position": newPos
                                    ,"KP":K_P ,"KI" :K_I ,"KD" : K_D}) 

                    
        def start_app() :
            t = threading.Thread(target=Start)
            t.start()
                        
        def Default() :
            print ("************************************* START POSITIONING ***************************************")
            global status 
            status = False
            
            global distance_X  
            global error      
            global new_pos 
            global kp
            global ki
            global kd
            global j
            distance_X = []  
            error = []      
            new_pos = []
            kp = []
            ki = []
            kd = []  
            j = 0  

            new_position = Decimal(50)
            kcube.MoveTo(Decimal(60), 7000) 
            
            while not status:
                print("----------------------------------------------")
                print('Capturing image')
                if j < 10:
                    filename = '00' + str(j) + '_image_lab.png'
                else:
                    filename = '0' + str(j) + '_image_lab.png'
                    
                camera.set_image_type(asi.ASI_IMG_RAW8)
                img = camera.capture(filename=save_path+filename)
                print('Saved to %s' % filename)
                print("----------------------------------------------")

                j+=1
                
                time.sleep(0.5)               
                if status:
                    break
                else:
                    disX = Draw_Contour(img)
                    
                    if disX is not None:  # Ensure disX has a value
                        if isinstance(distance_X, list):
                            distance_X.append(disX)  # Append to distanceX list
                    
                    
                        all_PID_Output = PID(Decimal(10), Decimal(0.1), Decimal(0.2), reference, Decimal(disX))
                        PID_Out = all_PID_Output[0]
                        p = all_PID_Output[1]
                        i = all_PID_Output[2]
                        d = all_PID_Output[3]
                        print("Error : " + str(PID_Out))
                        
                        new_position = PID_Out+kcube.Position #pos
                        print("New_position : " + str(new_position))
                        kcube.MoveTo(new_position, 7000)
                        
                        if PID_Out == Decimal(0) :
                            new_position = PID_Out+kcube.Position #pos
                            print("New_position : " + str(new_position))
                            kcube.MoveTo(new_position, 7000)
                        
                            if isinstance(error, list):
                                error.append(PID_Out) 

                            if isinstance(new_pos, list):
                                new_pos.append(new_position)
                                
                            if isinstance(kp, list):
                                kp.append(p)  

                            if isinstance(ki, list):
                                ki.append(i)  
                                
                            if isinstance(kd, list):
                                kd.append(d)   
                                                                                
                            with open('C://Users/Asus/Desktop/LAB_TEST/result.csv', 'w', newline='') as csvfile:
                                fieldnames = ["PID Output", "distanceX", "New position" , "KP" , "KI" , "KD"]
                                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                                writer.writeheader()

                                for err_value, distX, newPos,K_P,K_I,K_D in zip(error, distance_X, new_pos,kp,ki,kd):  # Corrected variable names
                                    writer.writerow({"PID Output": err_value, "distanceX": distX, "New position": newPos
                                    ,"KP":K_P ,"KI" :K_I ,"KD" : K_D})
                                    
                            print("*****************************FINISHED POSITIONG AT "+str(new_position)+"*********************************")   
                            return  
                        else :
                            if isinstance(error, list):
                                error.append(PID_Out) 

                            if isinstance(new_pos, list):
                                new_pos.append(new_position)
                                
                            if isinstance(kp, list):
                                kp.append(p)  

                            if isinstance(ki, list):
                                ki.append(i)  
                                
                            if isinstance(kd, list):
                                kd.append(d)   
                                                                                
                            with open('C://Users/Asus/Desktop/LAB_TEST/result.csv', 'w', newline='') as csvfile:
                                fieldnames = ["PID Output", "distanceX", "New position" , "KP" , "KI" , "KD"]
                                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                                writer.writeheader()

                                for err_value, distX, newPos,K_P,K_I,K_D in zip(error, distance_X, new_pos,kp,ki,kd):  # Corrected variable names
                                    writer.writerow({"PID Output": err_value, "distanceX": distX, "New position": newPos
                                    ,"KP":K_P ,"KI" :K_I ,"KD" : K_D}) 
                                    
        def default_app():
            r = threading.Thread(target=Default)
            r.start()
                    
        def home():
            global status 
            status = False            
            while not status:
                kcube.Home(6000)
                
        def home_app() :
            h = threading.Thread(target=home)
            h.start()
            
        def Stop():
            global status
            status = True
            print("***stop***")
            
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
                        width=10,
                        wraplength=100 )
        button.place(x = 460 , y = 90)
        
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
        button.place(x = 460 , y = 140)

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
                        width=10,
                        wraplength=100 )
        button.place(x = 460 , y = 190)

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
        button.place(x = 460 , y = 240)
        
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
                        width=10,
                        wraplength=100 )
        button.place(x = 460 , y = 290)

        window.mainloop()
                    
    except Exception as e:
        print("ERROR:", e)    
        
#-----------------------------------------------------------------------------------------------------------------------------        
if __name__ == "__main__":
    main()