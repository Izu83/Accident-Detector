# 🚗 AI Accident Detection

---

## What is this?
For my project, I trained an AI to look at traffic camera pictures and figure out if there is a car crash happening or just normal traffic. 

I used a large AI model called **Qwen2.5-VL-7B** and fine-tuned it on my own custom dataset using my GPU. I also wrote Python scripts to automatically test the AI and create an Excel grade report.

---

## 📂 Folder Setup
To make the code work, your folders need to look like this:

```text
📁 Project Folder
 ├── 📁 test_dataset                 # Put your pictures in here to test them
 │    ├── 📁 Accident                # Pictures of crashes
 │    └── 📁 Non Accident            # Pictures of normal traffic
 ├── 📁 output_accident_model        # The folder where the trained AI brain is saved
 ├── evaluate_model.py               # The script to test the AI on the whole folder
 ├── create_report.py                # The script to make the Excel file
 ├── grading.py                      # The script to grade the performance
 ├── processing_image.py             # The script to process the images into json
 └── test_model.py                   # The script to test the Model on a SINGLE image
 
 
---

## ⚙️ How to Install
If you want to run this project on your own computer, follow these steps:

**1. Download the code** Open your terminal and clone this repository:
```bash
git clone [https://github.com/Izu83/accident-detector.git](https://github.com/Izu83/accident-detector.git)
cd accident-detector
```
*(Make sure to change the link to your actual GitHub link when you upload it!)*

**2. Install the required Python libraries** You need to install the tools that power the AI and make the graphs:
```bash
pip install matplotlib pandas openpyxl ms-swift transformers
```

---

## 🛠️ How to Run Everything

### 1. Training the AI
*This is the command I used to train the AI on my custom dataset so it could learn what an accident looks like.*

```bash
swift sft \
  --model_type qwen2_5_vl \
  --model Qwen/Qwen2.5-VL-7B-Instruct \
  --dataset your_training_data.jsonl \
  --sft_type lora \
  --quant_method bnb \
  --quant_bits 4 \
  --output_dir output_accident_model
```

### 2. Testing the AI
*When you drop new pictures into the `test_dataset` folders, run this script. The AI will look at every picture and write down its guess. (Warning: This takes time depending on how many pictures you test!)*

```bash
python evaluate_model.py
```

### 3. Getting the Results
*After the testing is done, run this script. It reads all the AI's answers, grades them to see if it was right or wrong, and creates a clean `ai_test_results.xlsx` Excel file and a Pie Chart showing the final score.*

```bash
python create_report.py
```


## P.S.
The output_accident_model and the test_dataset aren't uploaded because of the amount of weight of the files. You could just find some images in Keggle from datasets and the output_accident_model folders is gonna be made by itself when you run the scripts.
