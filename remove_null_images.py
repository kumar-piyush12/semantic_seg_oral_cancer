import os

def remove_null_images(dataset_path):
    splits = ['train', 'valid', 'test']
    removed_images = 0
    
    for split in splits:
        img_dir = os.path.join(dataset_path, split, 'images')
        label_dir = os.path.join(dataset_path, split, 'labels')
        
        if not os.path.exists(img_dir) or not os.path.exists(label_dir):
            print(f"Warning: {split} directories not found.")
            continue
        
        img_files = [f for f in os.listdir(img_dir) if f.lower().endswith(('.jpg', '.png', '.jpeg'))]
        
        files_to_remove = []
        
        for img_file in img_files:
            label_file = os.path.splitext(img_file)[0] + '.txt'
            label_path = os.path.join(label_dir, label_file)
            
            if not os.path.exists(label_path):
                continue
            
            with open(label_path, 'r') as f:
                lines = f.readlines()
            
            # Remove image if ANY label is 'Null' (starts with 2)
            if any(line.strip().startswith('2 ') for line in lines):
                files_to_remove.append((img_file, label_file))
        
        # Remove files
        for img_file, label_file in files_to_remove:
            os.remove(os.path.join(img_dir, img_file))
            os.remove(os.path.join(label_dir, label_file))
            print(f"Removed: {img_file}")
            removed_images += 1
        
        print(f"{split} - Total images: {len(img_files)}, Removed images: {len(files_to_remove)}")
    
    # Update data.yaml
    yaml_path = os.path.join(dataset_path, 'data.yaml')
    with open(yaml_path, 'r') as f:
        yaml_content = f.read()
    
    yaml_content = yaml_content.replace("nc: 3\nnames: ['Abnormal', 'Normal', 'Null']", 
                                         "nc: 2\nnames: ['Abnormal', 'Normal']")
    
    with open(yaml_path, 'w') as f:
        f.write(yaml_content)
    
    print(f"\nTotal images removed: {removed_images}")

# Usage
dataset_path = r'C:\Users\91977\Desktop\Piyush\4th Year\4-2\MECH-LOP-Oral-Cancer\Dataset_2_YOLOv8'
remove_null_images(dataset_path)