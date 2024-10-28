import os 
import pandas as pd

# Read the CSV file
main_directory=r"data\archive\OSAIL_KL_Dataset\Labeled"

metadata = pd.DataFrame(columns=["Name","Path","KL"])

print()

for grade in range(5):
    folder_path = os.path.join(main_directory,f"{grade}")

    for image_name in os.listdir(folder_path):
        image_path= os.path.join(folder_path, image_name)

        metadata = metadata.append(
            {
                "Name" : image_name,
                "Path" : image_path,
                "KL" : grade
            }, ignore_idex= True)
        
    print()
            