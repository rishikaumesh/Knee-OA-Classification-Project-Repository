import os
import numpy as np
from pydicom import dcmread
import matplotlib.pyplot as plt
from PIL import Image

# Function to normalize pixel values and convert to 8-bit (0-255) range for saving as PNG
def normalize_to_uint8(image_array):
    # Normalize the image array to 0-255 range
    image_array = image_array.astype(np.float32)
    image_array -= image_array.min()
    image_array /= image_array.max()
    image_array *= 255
    return image_array.astype(np.uint8)

# Function to read landmark points from the .pts file
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

# Directory paths for DICOM and landmark files
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

    ### Split the landmarks for left and right knee ###
    mid_x = dicom_data.pixel_array.shape[1] // 2  # Middle of the image
    left_knee_landmarks = [(x, y) for x, y in zip(Xs, Ys) if x < mid_x]
    right_knee_landmarks = [(x, y) for x, y in zip(Xs, Ys) if x >= mid_x]

    ### Crop the left knee ###
    left_Xs, left_Ys = zip(*left_knee_landmarks)
    min_x_left = max(0, int(min(left_Xs)))
    max_x_left = min(dicom_data.pixel_array.shape[1], int(max(left_Xs)))
    min_y_left = max(0, int(min(left_Ys)))
    max_y_left = min(dicom_data.pixel_array.shape[0], int(max(left_Ys)))

    left_cropped_image = dicom_data.pixel_array[min_y_left:max_y_left, min_x_left:max_x_left]

    # Normalize the left knee image to 8-bit range
    left_cropped_image_normalized = normalize_to_uint8(left_cropped_image)

    # Plot the cropped left knee image with landmarks
    plt.imshow(left_cropped_image_normalized, cmap='gray')
    plt.scatter([x - min_x_left for x in left_Xs], [y - min_y_left for y in left_Ys], color='red', s=10)
    plt.axis('off')  # Turn off axis for cleaner image
    
    # Save left knee image with landmarks
    left_image_filename = f"{dicom_data.PatientID}_L.png"
    plt.savefig(left_image_filename, bbox_inches='tight', pad_inches=0)
    plt.close()

    ### Crop the right knee ###
    right_Xs, right_Ys = zip(*right_knee_landmarks)
    min_x_right = max(0, int(min(right_Xs)))
    max_x_right = min(dicom_data.pixel_array.shape[1], int(max(right_Xs)))
    min_y_right = max(0, int(min(right_Ys)))
    max_y_right = min(dicom_data.pixel_array.shape[0], int(max(right_Ys)))

    right_cropped_image = dicom_data.pixel_array[min_y_right:max_y_right, min_x_right:max_x_right]

    # Normalize the right knee image to 8-bit range
    right_cropped_image_normalized = normalize_to_uint8(right_cropped_image)

    # Plot the cropped right knee image with landmarks
    plt.imshow(right_cropped_image_normalized, cmap='gray')
    plt.scatter([x - min_x_right for x in right_Xs], [y - min_y_right for y in right_Ys], color='red', s=10)
    plt.axis('off')  # Turn off axis for cleaner image
    
    # Save right knee image with landmarks
    right_image_filename = f"{dicom_data.PatientID}_R.png"
    plt.savefig(right_image_filename, bbox_inches='tight', pad_inches=0)
    plt.close()

    print(f"Saved cropped images with landmarks for {dcm_name} as {left_image_filename} and {right_image_filename}")
