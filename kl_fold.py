import os
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split, StratifiedKFold

# Loading the dataset
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

# Visualizing the KL Grade Distribution for the Entire Dataset
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

# Spliting the dataset into training + validation (80%) and test (20%)
train_val_df, test_df = train_test_split(df, test_size=0.2, stratify=df['KL_Grade'], random_state=42)

# Performing Stratified 5-Fold Cross Validation
skf = StratifiedKFold(n_splits=5)

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

# Apply the Stratified K-Fold Cross Validation
fold = 1
for train_index, val_index in skf.split(train_val_df, train_val_df['KL_Grade']):
    train_df = train_val_df.iloc[train_index]
    val_df = train_val_df.iloc[val_index]
    
    # Ploting the distribution of KL grades for the training set
    plot_kl_distribution(train_df, f'Distribution of KL Grades in Training Set - Fold {fold}', f'kl_distribution_train_fold_{fold}.png')
    
    # Ploting the distribution of KL grades for the validation set
    plot_kl_distribution(val_df, f'Distribution of KL Grades in Validation Set - Fold {fold}', f'kl_distribution_val_fold_{fold}.png')
    
    fold += 1

# Ploting the distribution of KL grades for the test set
plot_kl_distribution(test_df, 'Distribution of KL Grades in Test Set', 'kl_distribution_test.png')
