import zwoasi as asi
import numpy
import os
import re


save_path = r"C:\Users\Asus\Desktop\LAB_TEST"
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
try:
    # Force any single exposure to be halted
    camera.stop_video_capture()
    camera.stop_exposure()
except (KeyboardInterrupt, SystemExit):
    raise

for i in range(10) :
    print('Capturing image')
    filename = str(i)+'_image_mono.png'
    camera.set_image_type(asi.ASI_IMG_RAW8)
    camera.capture(filename=save_path+filename)
    print('Saved to %s' % filename)
    i += 1
