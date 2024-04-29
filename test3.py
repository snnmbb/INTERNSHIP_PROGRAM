from PIL import Image
import os
import re

image_ref = r"C:\Users\Asus\Desktop\REF_CAP.png"
pattern = re.compile(r'(\d+)\.png')
directory = r'C:\Users\Asus\Desktop'
os.chdir(directory) 

# Open image using Pillow
imageObject = Image.open(image_ref)

# Horizontally flip the image
hori_flippedImage = imageObject.transpose(Image.FLIP_LEFT_RIGHT)

# Display the original and flipped images
imageObject.show()
hori_flippedImage.show()

# Save the flipped image
hori_flippedImage.save('test_im_flip.png')