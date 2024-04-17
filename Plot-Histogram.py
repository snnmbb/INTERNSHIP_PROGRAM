from PIL import Image
import matplotlib.pyplot as plt
import numpy as np
from SolExDataCube import Dir_Read
import os
import re

print("File path:", 'C:\\Users\\Asus\\Desktop\\Dot\\Dot_i\\Dot_13.png')
img = np.asarray(Image.open('C:\\Users\\Asus\\Desktop\\Dot\\Dot_i\\Dot_13.png'))

try : 
    print(img.shape)
    print(repr(img))
    fig = plt.figure(1)
    imgplot = plt.imshow(img)
    fig2 = plt.figure(2)
    if len(img.shape) == 2:
        lum_img = img[:, :]
    else:
        lum_img = img[:, :, 0]
    plt.hist(lum_img, bins='auto')
    plt.show()

except Exception as e:
    print("ERROR", e)
        