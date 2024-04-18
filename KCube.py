import os
import time
import sys
import clr

clr.AddReference("C:\\Program Files\\Thorlabs\\Kinesis\\Thorlabs.MotionControl.DeviceManagerCLI.dll.")
clr.AddReference("C:\\Program Files\\Thorlabs\\Kinesis\\Thorlabs.MotionControl.GenericMotorCLI.dll.")
clr.AddReference("C:\\Program Files\\Thorlabs\\Kinesis\\Thorlabs.MotionControl.KCube.BrushlessMotorCLI.dll.")
#clr.AddReference("C:\\Program Files\\Thorlabs\\Kinesis\\ThorLabs.MotionControl.PositionReadoutEncoderCLI.dll")

from Thorlabs.MotionControl.DeviceManagerCLI import *
from Thorlabs.MotionControl.GenericMotorCLI import *
#from Thorlabs.MotionControl.PositionReadoutEncoderCLI import *
from Thorlabs.MotionControl.KCube.BrushlessMotorCLI import *
from System import Decimal

def main():

    try:
        
        DeviceManagerCLI.BuildDeviceList()
        
        serial_num = str("28251928")  
        kcube = KCubeBrushlessMotor.CreateKCubeBrushlessMotor(serial_num)
        #encoder =  ReadoutEncoder.CreatePositionReadoutEncoder(serial_num)
        measurement = kcube.Position 
        
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
                   
        for i in range (10) :
            kcube.MoveTo(Decimal(10.0), 60000)
            print(f'{kcube.Position}') 
            kcube.MoveTo(Decimal(20.0), 60000)
            print(f'{kcube.Position}') 
            kcube.MoveTo(Decimal(30.0), 60000)
            print(f'{kcube.Position}') 
            kcube.MoveTo(Decimal(40.0), 60000)
            print(f'{kcube.Position}') 
            kcube.MoveTo(Decimal(50.0), 60000)
            print(f'{kcube.Position}') 
            kcube.MoveTo(Decimal(60.0), 60000)
            print(f'{kcube.Position}') 
            kcube.MoveTo(Decimal(70.0), 60000)
            print(f'{kcube.Position}') 
            kcube.MoveTo(Decimal(80.0), 60000)
            print(f'{kcube.Position}') 
            kcube.MoveTo(Decimal(90.0), 60000)
            print(f'{kcube.Position}') 
            kcube.MoveTo(Decimal(0.0), 60000)
            print(f'{kcube.Position}') 
        kcube.Home(60000)
        print("Finished")

        # Stop polling and close device
        kcube.StopPolling()
        kcube.Disconnect(True)
        
    except Exception as e:
        print(e)
   

if __name__ == "__main__":
    main()