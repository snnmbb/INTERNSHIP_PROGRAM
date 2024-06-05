import os
import glob
from PIL import Image

# Define the directory containing the images
image_dir = r"C:\\Users\\Asus\\Desktop\\LAB_TEST\\DATA"

# Get all image files in the directory
# You can filter for specific image extensions like jpg, png, etc.
image_files = glob.glob(os.path.join(image_dir, '*.jpg')) + \
              glob.glob(os.path.join(image_dir, '*.png')) + \
              glob.glob(os.path.join(image_dir, '*.jpeg')) + \
              glob.glob(os.path.join(image_dir, '*.bmp')) + \
              glob.glob(os.path.join(image_dir, '*.gif'))

# Ensure there are image files in the directory
if not image_files:
    print("No image files found in the directory.")
else:
    # Find the most recent file based on modification time
    most_recent_file = max(image_files, key=os.path.getmtime)

    # Open and display the image using PIL
    try:
        image = Image.open(most_recent_file)
        image.show()
    except Exception as e:
        print(f"Error opening image: {e}")

    # Optionally, you can print the path of the most recent file
    print(f"The most recent image is: {most_recent_file}")