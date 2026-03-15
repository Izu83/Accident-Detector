import json
import csv
import os
import matplotlib.pyplot as plt

# ==========================================
# GRADING WITH DUPLICATE FILTER
# ==========================================
output_jsonl = "ai_results.jsonl"
csv_filename = "ai_test_results.csv"

print("="*50)
print("FILTERING DUPLICATES & GRADING")
print("="*50)

unique_images = {}

if not os.path.exists(output_jsonl):
    print(f"ERROR: Could not find {output_jsonl}!")
    exit()

with open(output_jsonl, "r", encoding="utf-8") as f:
    for line in f:
        data = json.loads(line)
        
        img_data = data.get("images", [""])[0]
        img_path_str = str(img_data).lower()
        
        ai_text = ""
        if "response" in data:
            ai_text = data["response"]
        elif "messages" in data and len(data["messages"]) > 0:
            ai_text = data["messages"][-1].get("content", "")
        
        if isinstance(img_data, str):
            filename = os.path.basename(img_data)
        elif isinstance(img_data, dict) and "image" in img_data:
            filename = os.path.basename(img_data["image"])
        else:
            filename = img_path_str

        unique_images[filename] = {
            "path": img_path_str,
            "ai_text": ai_text.strip().lower(),
            "raw_text": ai_text.strip()
        }

correct = 0
wrong = 0
results_for_csv = []

for filename, info in unique_images.items():
    img_path_str = info["path"]
    ai_text_lower = info["ai_text"]

    if "non accident" in img_path_str:
        true_label = "Non Accident"
    elif "accident" in img_path_str:
        true_label = "Accident"
    else:
        continue

    if "no accident" in ai_text_lower:
        ai_prediction = "Non Accident"
    else:
        ai_prediction = "Accident"

    is_correct = (ai_prediction == true_label)
    if is_correct:
        correct += 1
        status = "CORRECT"
    else:
        wrong += 1
        status = "WRONG"

    results_for_csv.append([filename, true_label, ai_prediction, status, info["raw_text"]])

with open(csv_filename, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(["Filename", "True Category", "AI Prediction", "Result", "Raw AI Answer"])
    writer.writerows(results_for_csv)

total_images = correct + wrong
accuracy = (correct / total_images) * 100 if total_images > 0 else 0

print(f"Filtered down to {total_images} UNIQUE images.")
print("="*50)
print(f"REAL FINAL ACCURACY: {accuracy:.1f}% ({correct}/{total_images})")
print("="*50)

labels = [f'Correct ({correct})', f'Wrong ({wrong})']
sizes = [correct, wrong]
colors = ['#4CAF50', '#F44336'] 
explode = (0.1, 0) 

plt.figure(figsize=(8, 6))
plt.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%', shadow=True, startangle=140)
plt.title(f'AI Accident Detection Accuracy\nTotal Unique Images: {total_images}')
plt.axis('equal')

print("Opening the graph! Close the graph window to finish.")
plt.show()