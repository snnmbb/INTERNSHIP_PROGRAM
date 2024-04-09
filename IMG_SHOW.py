# importing Image module from PIL package 
from PIL import Image 
from matplotlib import pyplot as plt
from matplotlib import pyplot as mpimg
import numpy as np
import glob
import os
import pathlib
import csv
from SolExDataCube import Dir_Read

image_path = r"C:\Users\Asus\Desktop\ASI1600-PRO\img\mono16"
os.chdir(image_path)

for image_path_mono16 in Dir_Read('s', path=image_path):
    image = plt.imread(image_path_mono16)
    img = np.asarray(Image.open(image_path_mono16))
    im = Image.open(image_path_mono16).convert("L")  
    im1 = Image.Image.getdata(im) 
    print(image_path_mono16)
    print(im1) 
    print(repr(img))
    plt.imshow(image)
    plt.show(block=False)
    plt.pause(6)
    plt.close()   
    
    


