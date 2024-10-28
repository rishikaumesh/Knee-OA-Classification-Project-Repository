import os
from pydicom import dcmread

# Directory containing the DICOM files
dicom_dir = 'data/dicoms'

# Loop through all the DICOM files to inspect metadata
for dcm in os.listdir(dicom_dir):
    dcm_path = os.path.join(dicom_dir, dcm)
    dicom_data = dcmread(dcm_path)

    # Print the relevant metadata
    print(f"File: {dcm}")
    print(f"Patient ID: {dicom_data.PatientID}")
    
    # Check for 'ImageLaterality' (Left/Right indicator)
    if 'ImageLaterality' in dicom_data:
        print(f"Image Laterality: {dicom_data.ImageLaterality}")
    
    # Check for 'BodyPartExamined' (e.g., 'KNEE')
    if 'BodyPartExamined' in dicom_data:
        print(f"Body Part Examined: {dicom_data.BodyPartExamined}")
    
    # Print other useful metadata fields
    print(f"View Position: {dicom_data.ViewPosition if 'ViewPosition' in dicom_data else 'N/A'}")
    print(f"Modality: {dicom_data.Modality if 'Modality' in dicom_data else 'N/A'}")
    print("=" * 50)
