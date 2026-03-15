import json
import csv
import os
import matplotlib.pyplot as plt

# ==========================================
# GRADING THE AI'S 4-HOUR EXAM, THIS IS ONLY IF IT CRASHED! WHICH IS ALMOST 100% OF THE TIME, SO THIS IS YOUR BACKUP PLAN TO GET A GRADE! 
# ==========================================
output_jsonl = "ai_results.jsonl"
csv_filename = "ai_test_results.csv"

print("="*50)
print("GRADING IN PROGRESS")
print("="*50)

correct = 0
wrong = 0
results_for_csv = []

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
        
        ai_text_lower = ai_text.strip().lower()

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

        if isinstance(img_data, str):
            filename = os.path.basename(img_data)
        elif isinstance(img_data, dict) and "image" in img_data:
            filename = os.path.basename(img_data["image"])
        else:
            filename = "Unknown_Image"

        results_for_csv.append([filename, true_label, ai_prediction, status, ai_text.strip()])

with open(csv_filename, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(["Filename", "True Category", "AI Prediction", "Result", "Raw AI Answer"])
    writer.writerows(results_for_csv)

print(f"Detailed report saved to Excel file: {csv_filename}")

total_images = correct + wrong
if total_images == 0:
    print("No images were graded. Something went wrong reading the file!")
    exit()

accuracy = (correct / total_images) * 100

print("="*50)
print(f"FINAL ACCURACY: {accuracy:.1f}% ({correct}/{total_images})")
print("="*50)

labels = [f'Correct ({correct})', f'Wrong ({wrong})']
sizes = [correct, wrong]
colors = ['#4CAF50', '#F44336']
explode = (0.1, 0)

plt.figure(figsize=(8, 6))
plt.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%', shadow=True, startangle=140)
plt.title(f'AI Accident Detection Accuracy\nTotal Images Tested: {total_images}')
plt.axis('equal')

print("Opening the graph! Close the graph window to finish.")
plt.show()