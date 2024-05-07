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

image_ref = r"C:\Users\Asus\Desktop\LAB_TEST\REF\REF.png"
save_path = r"C:\\Users\\Asus\\Desktop\LAB_TEST\DATA2\\"
asi.init('C:\\Users\\Asus\\AppData\\Local\\Programs\\Python\\Python310\\Lib\\ASI SDK\\lib\\x64\ASICamera2.lib')
pattern = re.compile(r'(\d+)\.png')
os.chdir(save_path)


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
camera.set_control_value(asi.ASI_EXPOSURE, 293000) #microseconds #ปรับค่าการรับแสง
camera.set_control_value(asi.ASI_WB_B, 0)  #ปรับค่าblue component of white balance
camera.set_control_value(asi.ASI_WB_R, 0) #ปรับค่าred component of white balance
camera.set_control_value(asi.ASI_GAMMA, 0) #ปรับค่าการเปลี่ยนสีจากสีดำเป็นสีขาว gamma with range 1 to 100 (nomnally 50)
camera.set_control_value(asi.ASI_BRIGHTNESS, 10)
camera.set_control_value(asi.ASI_FLIP, 0) #ปรับการหมุนรูป

  
clr.AddReference("C:\\Program Files\\Thorlabs\\Kinesis\\Thorlabs.MotionControl.DeviceManagerCLI.dll.")
clr.AddReference("C:\\Program Files\\Thorlabs\\Kinesis\\Thorlabs.MotionControl.GenericMotorCLI.dll.")
clr.AddReference("C:\\Program Files\\Thorlabs\\Kinesis\\Thorlabs.MotionControl.KCube.BrushlessMotorCLI.dll.")
#clr.AddReference("C:\\Program Files\\Thorlabs\\Kinesis\\ThorLabs.MotionControl.PositionReadoutEncoderCLI.dll")

from Thorlabs.MotionControl.DeviceManagerCLI import *
from Thorlabs.MotionControl.GenericMotorCLI import *
#from Thorlabs.MotionControl.PositionReadoutEncoderCLI import *
from Thorlabs.MotionControl.KCube.BrushlessMotorCLI import *
from System import Decimal

e_prev = Decimal(0)

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

def main():

    try:
        
        #SETUP
        DeviceManagerCLI.BuildDeviceList()
        
        serial_num = str("28251928")  
        kcube = KCubeBrushlessMotor.CreateKCubeBrushlessMotor(serial_num)
        kcube.Connect(serial_num)
        pos = Decimal(50.0) # ตำแหน่งเริ่มต้นที่มอเตอร์ขยับไปให้แสงตกในกล้อง

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
        
        kcube.MoveTo(Decimal(52), 7000)

        for i in range(20) :
            print("----------------------------------------------")
            print('Capturing image')
            filename = str(i)+'_image_lab.png'
            camera.set_image_type(asi.ASI_IMG_RAW16)
            camera.capture(filename=save_path+filename)
            print('Saved to %s' % filename)
            print("----------------------------------------------")
            #capture()
            time.sleep(0.5)
            for path in Dir_Read('s', path=save_path):
                disX = Draw_Contour(path)
                reference = Decimal(52)
                print("Finished")
                
                new_position = PID(Decimal(0.07) , Decimal(0.08), Decimal(0.01) , reference , Decimal(disX)) # KP , KI , KD , จุดที่แสงอยู่จุดศูนย์กลาง (reference 0) , ระยะห่างจากจุดศูนย์กลางที่รับค่าจากกล้อง/เซนเซอร์
                print(new_position)
                if new_position >= pos :
                    print(new_position)    
                    kcube.MoveTo(new_position , 7000)
                    print(f'{kcube.Position}')
                else :
                    new_pos = pos+new_position  
                    print(new_pos)    
                    kcube.MoveTo(new_position , 7000)
                    print(f'{kcube.Position}')
            time.sleep(0.5)
            i=+1
                
        kcube.Home(60000)
        print("Finished")

        # Stop polling and close device
        kcube.StopPolling()
        kcube.Disconnect(True)
        
        
                 
    except Exception as e:
        print("ERROR:", e)   
'''       
def capture() :
    for j in range(10):
        print("----------------------------------------------")
        print('Capturing image')
        filename = str(j)+'_image_lab.png'
        camera.set_image_type(asi.ASI_IMG_RAW16)
        camera.capture(filename=save_path+filename)
        print('Saved to %s' % filename)
        print("----------------------------------------------")
        j=+1
'''
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
            
            #print('sum', len(np.argwhere(mask_or == np.amax(mask_or))))
            
        print("-------------------------------------------------")
        print(save_path)
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
        
if __name__ == "__main__":
    main()