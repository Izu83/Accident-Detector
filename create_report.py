import json
import os
import pandas as pd

# ==========================================
# EXCEL (.XLSX) REPORT GENERATOR
# ==========================================
input_jsonl = "ai_results.jsonl"
output_excel = "ai_test_results.xlsx"

print("="*50)
print("GENERATING TRUE EXCEL REPORT (.XLSX)")
print("="*50)

if not os.path.exists(input_jsonl):
    print(f"ERROR: Could not find {input_jsonl}!")
    print("Make sure the AI has finished running its test first.")
    exit()

unique_images = {}

print("Reading AI results...")
with open(input_jsonl, "r", encoding="utf-8") as f:
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

results_for_excel = []
correct_count = 0
total_count = 0

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
        status = "CORRECT"
        correct_count += 1
    else:
        status = "WRONG"
        
    total_count += 1

    results_for_excel.append({
        "Filename": filename,
        "True Category": true_label,
        "AI Prediction": ai_prediction,
        "Result": status,
        "Raw AI Answer": info["raw_text"]
    })

print("Building true .xlsx file...")

df = pd.DataFrame(results_for_excel)

try:
    df.to_excel(output_excel, index=False, engine='openpyxl')
    
    print("="*50)
    print(f"SUCCESS! Native Excel report generated for {total_count} images.")
    print(f"You can now double-click and open '{output_excel}'.")
    print("="*50)
except Exception as e:
    print(f"ERROR saving Excel file: {e}")
    print("Make sure you don't have the old Excel file open right now!")