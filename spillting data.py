import os
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split

base_path = '/Users/rishikakalyanappa/Documents/AI MEDICAL IMAGING/archive (5)/OSAIL_KL_Dataset/Labeled' 

data = []

for kl_grade in range(5):
    folder_path = os.path.join(base_path, str(kl_grade))
    for image_name in os.listdir(folder_path):
        image_path = os.path.join(folder_path, image_name)
        data.append({'image_path': image_path, 'KL_Grade': kl_grade})

df = pd.DataFrame(data)

print("Sample data from the dataset:")
print(df.head(30))

# Visualize the KL Grade Distribution for the Entire Dataset
# Create a bar chart for the distribution of KL grades in the entire dataset
kl_counts = df['KL_Grade'].value_counts().sort_index()
plt.figure(figsize=(8, 5))
kl_counts.plot(kind='bar', color='skyblue', edgecolor='black')
plt.title('Distribution of KL Grades in Entire Dataset')
plt.xlabel('KL Grade')
plt.ylabel('Frequency')
plt.xticks(rotation=0)
plt.tight_layout()
plt.savefig('kl_distribution_entire_dataset.png')
plt.show()

# Split the Dataset into Training, Validation, and Test Sets
# Hold out 20% of the data as the test set
train_val_df, test_df = train_test_split(df, test_size=0.2, stratify=df['KL_Grade'], random_state=42)

# Split the remaining 80% into 80% training and 20% validation sets
train_df, val_df = train_test_split(train_val_df, test_size=0.2, stratify=train_val_df['KL_Grade'], random_state=42)

# Visualize the KL Grade Distribution for Each Split
# Function to plot distribution
def plot_kl_distribution(dataframe, title, filename):
    kl_counts = dataframe['KL_Grade'].value_counts().sort_index()
    plt.figure(figsize=(8, 5))
    kl_counts.plot(kind='bar', color='skyblue', edgecolor='black')
    plt.title(title)
    plt.xlabel('KL Grade')
    plt.ylabel('Frequency')
    plt.xticks(rotation=0)
    plt.tight_layout()
    plt.savefig(filename)
    plt.show()

# Plot distributions for training, validation, and test sets
plot_kl_distribution(train_df, 'Distribution of KL Grades in Training Set', 'kl_distribution_train.png')
plot_kl_distribution(val_df, 'Distribution of KL Grades in Validation Set', 'kl_distribution_val.png')
plot_kl_distribution(test_df, 'Distribution of KL Grades in Test Set', 'kl_distribution_test.png')
