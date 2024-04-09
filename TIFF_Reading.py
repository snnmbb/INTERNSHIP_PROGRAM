from PIL import Image
import glob
import pathlib
import csv
from SolExDataCube import Dir_Read
import os

image_path = r"C:\Users\Asus\Desktop\ASI1600-PRO\img\mono16\\"
os.chdir(image_path)
# Create an empty list to store the image metadata
metadata_list = []

# Search for TIFF image files in the directory
for image_path_mono16 in Dir_Read('s', path=image_path):
    # Open the image file
    
    print(image_path_mono16)
    image = Image.open(image_path_mono16)

    # Extract basic metadata
    image_size = image.size
    image_height = image.height
    image_width = image.width
    image_format = image.format
    image_mode = image.mode
    image_is_animated = getattr(image, "is_animated", False)
    frames_in_image = getattr(image, "n_frames", 1)

    # Create a dictionary to store the metadata
    metadata = {
        "filename": pathlib.Path(image_path_mono16).name,
        "size": image_size,
        "height": image_height,
        "width": image_width,
        "format": image_format,
        "mode": image_mode,
        "is_animated": image_is_animated,
        "frames": frames_in_image,
    }

    # Add the metadata dictionary to the list
    metadata_list.append(metadata)

# Write the metadata list to a CSV file
if metadata_list:  # Ensure metadata_list is not empty before writing to CSV
    with open("metadata.csv", "w", newline="") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=metadata_list[0].keys())
        #print(metadata_list[0].keys())
        writer.writeheader()
        writer.writerows(metadata_list)
else:
    print("No TIFF image files found in the directory.")