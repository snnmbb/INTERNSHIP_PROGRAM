from PIL import Image

image_ref = r"C:\Users\Asus\Desktop\REF_CAP.png"

# Open image using Pillow
imageObject = Image.open(image_ref)

# Horizontally flip the image
hori_flippedImage = imageObject.transpose(Image.FLIP_LEFT_RIGHT)

# Display the original and flipped images
imageObject.show()
hori_flippedImage.show()

# Save the flipped image
hori_flippedImage.save('test_im_flip.png')