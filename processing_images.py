import kagglehub
import os
import json

############################################
# PROCESSING IMAGES AND CREATING THE JSONL FILE
############################################

print("Downloading dataset...")
path = kagglehub.dataset_download("ckay16/accident-detection-from-cctv-footage")
print(f"Dataset downloaded to: {path}")

dataset = []
image_id_counter = 1

print("Scanning folders and building the VLM dataset...")
for root, dirs, files in os.walk(path):
    for file in files:
        if file.lower().endswith(('.png', '.jpg', '.jpeg')):
            img_path = os.path.join(root, file)
            path_lower = img_path.lower()
            
            if 'non accident' in path_lower or 'non_accident' in path_lower:
                description = "No accident detected. The traffic and scene appear normal."
            elif 'accident' in path_lower:
                description = "An accident is occurring in this CCTV frame. Vehicles have collided."
            else:
                continue 
                
            entry = {
                "id": f"cctv_frame_{image_id_counter}",
                "image": img_path.replace("\\", "/"), 
                "conversations": [
                    {
                        "from": "user",
                        "value": "<image>\nAnalyze this CCTV frame. Is there an accident happening?"
                    },
                    {
                        "from": "assistant",
                        "value": description
                    }
                ]
            }
            dataset.append(entry)
            image_id_counter += 1

with open('cctv_image_train.json', 'w') as f:
    json.dump(dataset, f, indent=2)

print(f"Success! Processed {len(dataset)} images and saved to cctv_image_train.json")