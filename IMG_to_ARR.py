from PIL import Image
from numpy import asarray
import os
import re

image_path_mono = r"C:\Users\Asus\Desktop\ASI1600-PRO\img\mono\0_image_mono.jpg"
image_path_mono16 = r"C:\Users\Asus\Desktop\ASI1600-PRO\img\mono16\0_image_mono16.tiff"
pattern = re.compile(r'(\d+)\.png')
img_mono = Image.open(image_path_mono)
img_mono16 = Image.open(image_path_mono16)

numpydata_mono = asarray(img_mono)
numpydata_mono16 = asarray(img_mono16)

print("MONO IMAGE")
print(numpydata_mono)
print(numpydata_mono.shape)
print("----------------------------------")
print("MONO16 IMAGE")
print(numpydata_mono16)
print(numpydata_mono16.shape)
