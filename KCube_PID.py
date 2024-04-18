import os
import time
import sys
import clr
import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt

clr.AddReference("C:\\Program Files\\Thorlabs\\Kinesis\\Thorlabs.MotionControl.DeviceManagerCLI.dll.")
clr.AddReference("C:\\Program Files\\Thorlabs\\Kinesis\\Thorlabs.MotionControl.GenericMotorCLI.dll.")
clr.AddReference("C:\\Program Files\\Thorlabs\\Kinesis\\Thorlabs.MotionControl.KCube.BrushlessMotorCLI.dll.")


from Thorlabs.MotionControl.DeviceManagerCLI import *
from Thorlabs.MotionControl.GenericMotorCLI import *
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
        DeviceManagerCLI.BuildDeviceList()
        serial_num = str("28251928")  
        kcube = KCubeBrushlessMotor.CreateKCubeBrushlessMotor(serial_num)
        
        pos = Decimal(50.0) # ตำแหน่งเริ่มต้นที่มอเตอร์ขยับไปให้แสงตกในกล้อง
        
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
        reference = Decimal(0)
        print("Homing Device...")
        #kcube.Home(60000)  # 60 second timeout
        print("Device Homed")
        #kcube.MoveTo(pos,10000)
        while(True) :
            #val_str = input("Enter value of offset : ")
            #print("OK")
            #val = Decimal(val_str)
            #print("OK")
            new_position = PID(Decimal(0.07) , Decimal(0.08), Decimal(0.01) , reference , Decimal(0.02)) # KP , KI , KD , จุดที่แสงอยู่จุดศูนย์กลาง (reference 0) , ระยะห่างจากจุดศูนย์กลางที่รับค่าจากกล้อง/เซนเซอร์
            print(new_position)
            if new_position >= Decimal(0.01) :
                new_pos = pos-new_position
            else :
                new_pos = pos+new_position  
            print(new_pos)    
            kcube.MoveTo(new_pos , 5000)

            
        # Stop polling and close device
        #kcube.StopPolling()
        #kcube.Disconnect(True)
        
    except Exception as e:
        print(e)
        


if __name__ == "__main__":
    main()