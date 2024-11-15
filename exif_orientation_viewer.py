from PIL import Image
from PIL.ExifTags import TAGS

# Load the image using Pillow
image = Image.open('01753!!!289 - DSC_0956.JPG')

# Get the EXIF data from the image
exif_data = image._getexif()

# Check if EXIF data exists
if exif_data is not None:
    # Iterate through all EXIF tags
    for tag, value in exif_data.items():
        tag_name = TAGS.get(tag, tag)
        if tag_name == 'Orientation':
            print(f"Orientation: {value}")
            break
else:
    print("No EXIF data found in the image.")