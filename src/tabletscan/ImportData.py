import os
import shutil
from pathlib import Path
import random
from datafed.CommandLib import API
import zipfile

# Download data files from DataFed
df_api = API()
datapath = os.getcwd() #directory where Globus Endpoint has access

get_resp = df_api.dataGet(
    'd/525646261',
    datapath,  # directory where data should be downloaded  
    wait=True,  
)
print(get_resp)

# Unzip Folder
with zipfile.ZipFile(datapath + "/525646261.zip", "r") as zip_ref:
    print("Unzipping nCT Scans")
    zip_ref.extractall(datapath)

#Split Data into Test and Train Sets
base_dir = Path("data/") # Location where you want data to go
train_dir = base_dir / "train"
test_dir = base_dir / "test"
categories = ["70MPa", "200MPa"]
source_dir = Path(datapath) # Location where you downloaded data

# Create directory structure
for split in ["train", "test"]:
    for category in categories:
        os.makedirs(base_dir / split / category, exist_ok=True)

# Function to split and move images
def split_and_move_images(source_dir, train_dir, test_dir, categories, train_ratio=0.8, seed=42):
    random.seed(seed)
    
    for category in categories:
        category_dir = source_dir / category
        images = list(category_dir.glob("*.jpg"))
        if not images:
            print(f"[WARNING] No images found in {category_dir}")
            continue
        
        random.shuffle(images)
        
        train_count = int(len(images) * train_ratio)
        train_images = images[:train_count]
        test_images = images[train_count:]
        
        for img in train_images:
            dest_dir = train_dir / category / img.name
            if not dest_dir.parent.is_dir():
                dest_dir.parent.mkdir(parents=True, exist_ok=True)
            print(f"[INFO] Copying {img} to {dest_dir}...")
            shutil.copy2(img, dest_dir)
        
        for img in test_images:
            dest_dir = test_dir / category / img.name
            if not dest_dir.parent.is_dir():
                dest_dir.parent.mkdir(parents=True, exist_ok=True)
            print(f"[INFO] Copying {img} to {dest_dir}...")
            shutil.copy2(img, dest_dir)

# Split and move images
split_and_move_images(source_dir, train_dir, test_dir, categories)
