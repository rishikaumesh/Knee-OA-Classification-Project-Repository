# import os
# import numpy as np
# from pydicom import dcmread
# import matplotlib.pyplot as plt


# def coordinates(points_file):
#     line_count = 0
#     x = []
#     y = []
#     with open(points_file) as fp:
#         for line in fp:
#             if line_count >= 1:
#                 end_point = 151
#             if 3 <= line_count < end_point:
#                 x_temp = line.split(" ")[0]
#                 y_temp = line.split(" ")[1]
#                 y_temp = y_temp.replace("\n", "")
#                 x.append((float(x_temp)))
#                 y.append((float(y_temp)))
#             line_count += 1
#     return x, y

# dicom_dir= 'data/dicoms'
# landmarks_dir='data/landmarks'

# for dcm in os.listdir(dicom_dir): 
#     dcm_name=os.path.splitext(dcm)[0]

#     # Read the dicom file
#     dcm_path=os.path.join(dicom_dir,dcm)
#     dicom_data= dcmread(dcm_path)

#     landmarks_dir= os.path.join(landmarks_dir, f"{dcm_name}.pts")
#     Xs, Ys = coordinates(landmarks_dir)

#     ### Plot the dicom image and the landmarks ###
#     plt.imshow(dicom_data.pixel_array, cmap='gray')
#     plt.title(f"Patient ID: {dicom_data.PatientID}")
#     plt.show()

#     ### Pixel based cropping ###
#     cropped_image = 


#     print()

import os
import numpy as np
from pydicom import dcmread
import matplotlib.pyplot as plt
from PIL import Image

def coordinates(points_file):
    line_count = 0
    x = []
    y = []
    with open(points_file) as fp:
        for line in fp:
            if line_count >= 1:
                end_point = 151
            if 3 <= line_count < end_point:
                x_temp = line.split(" ")[0]
                y_temp = line.split(" ")[1]
                y_temp = y_temp.replace("\n", "")
                x.append((float(x_temp)))
                y.append((float(y_temp)))
            line_count += 1
    return x, y

dicom_dir = 'data/dicoms'
landmarks_dir = 'data/landmarks'

# Loop through all the DICOM files in the directory
for dcm in os.listdir(dicom_dir):
    dcm_name = os.path.splitext(dcm)[0]

    # Read the dicom file
    dcm_path = os.path.join(dicom_dir, dcm)
    dicom_data = dcmread(dcm_path)

    # Read corresponding landmarks
    points_file = os.path.join(landmarks_dir, f"{dcm_name}.pts")
    Xs, Ys = coordinates(points_file)

    ### Plot the dicom image and the landmarks ###
    plt.imshow(dicom_data.pixel_array, cmap='gray')
    plt.scatter(Xs, Ys, color='red')
    plt.title(f"Patient ID: {dicom_data.PatientID}")
    plt.show()

    ### Pixel based cropping around the landmarks ###

    # Get the pixel spacing (mm per pixel) from the DICOM metadata
    pixel_spacing = dicom_data.PixelSpacing  # [x_spacing, y_spacing] in mm

    # Convert 1 cm (10 mm) margin to pixels
    margin_mm = 10  # 1 cm = 10 mm
    margin_x_pixels = margin_mm / pixel_spacing[0]
    margin_y_pixels = margin_mm / pixel_spacing[1]

    # Get the bounding box around the landmarks
    min_x = max(0, int(min(Xs) - margin_x_pixels))
    max_x = min(dicom_data.pixel_array.shape[1], int(max(Xs) + margin_x_pixels))
    min_y = max(0, int(min(Ys) - margin_y_pixels))
    max_y = min(dicom_data.pixel_array.shape[0], int(max(Ys) + margin_y_pixels))

    # Crop the image based on the calculated bounding box
    cropped_image = dicom_data.pixel_array[min_y:max_y, min_x:max_x]

    # Convert the cropped array to an image and save as PNG
    cropped_image_pil = Image.fromarray(cropped_image)
    cropped_image_filename = f"{dcm_name}_cropped.png"
    cropped_image_pil.save(cropped_image_filename)

    print(f"Saved cropped image for {dcm_name} as {cropped_image_filename}")

