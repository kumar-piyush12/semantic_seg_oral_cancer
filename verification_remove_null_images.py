import os

def verify_null_images_removed(dataset_path):
    splits = ['train', 'valid', 'test']
    null_images_found = 0
    
    for split in splits:
        label_dir = os.path.join(dataset_path, split, 'labels')
        
        for label_file in os.listdir(label_dir):
            with open(os.path.join(label_dir, label_file), 'r') as f:
                lines = f.readlines()
                if any(line.strip().startswith('2 ') for line in lines):
                    print(f"Null label found in {split}/{label_file}")
                    null_images_found += 1
    
    if null_images_found == 0:
        print("✓ No Null images/labels remain in the dataset")
    else:
        print(f"⚠ {null_images_found} Null images/labels still present")

# Usage
dataset_path = r'C:\Users\91977\Desktop\Piyush\4th Year\4-2\MECH-LOP-Oral-Cancer\Dataset_2_YOLOv8'
verify_null_images_removed(dataset_path)