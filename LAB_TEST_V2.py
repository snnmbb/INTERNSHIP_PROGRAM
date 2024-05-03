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


save_path = r"C:\\Users\\Asus\\Desktop\LAB_TEST\\"
asi.init('C:\\Users\\Asus\\AppData\\Local\\Programs\\Python\\Python310\\Lib\\ASI SDK\\lib\\x64\ASICamera2.lib')

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
camera.set_control_value(asi.ASI_EXPOSURE, 1165) #microseconds #ปรับค่าการรับแสง
camera.set_control_value(asi.ASI_WB_B, 0)  #ปรับค่าblue component of white balance
camera.set_control_value(asi.ASI_WB_R, 0) #ปรับค่าred component of white balance
camera.set_control_value(asi.ASI_GAMMA, 0) #ปรับค่าการเปลี่ยนสีจากสีดำเป็นสีขาว gamma with range 1 to 100 (nomnally 50)
camera.set_control_value(asi.ASI_BRIGHTNESS, 10)
camera.set_control_value(asi.ASI_FLIP, 0) #ปรับการหมุนรูป

print('Enabling stills mode')

from Thorlabs.MotionControl.DeviceManagerCLI import *
from Thorlabs.MotionControl.GenericMotorCLI import *
#from Thorlabs.MotionControl.PositionReadoutEncoderCLI import *
from Thorlabs.MotionControl.KCube.BrushlessMotorCLI import *
from System import Decimal

def main() :
    
    DeviceManagerCLI.BuildDeviceList()
            
    serial_num = str("28251928")  
    kcube = KCubeBrushlessMotor.CreateKCubeBrushlessMotor(serial_num)
    kcube.Connect(serial_num)
        
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
    kcube.MaxVelocity = Decimal(30)
            
    print("Homing Device...")
    kcube.Home(60000)  # 60 second timeout
    print("Device Homed")

    try:
        # Force any single exposure to be halted
        camera.stop_video_capture()
        camera.stop_exposure()
    except (KeyboardInterrupt, SystemExit):
        raise

    try : 
        pos = Decimal(52.0)
        for i in range(10) :
            kcube.MoveTo(pos, 60000)
            print(f'{kcube.Position}') 
            capture()
            i +=1
            pos += Decimal(1.0)


    except Exception as e:
        print("ERROR:", e) 
        
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

if __name__=="__main__": 
    main() 