from swift.llm import get_model_tokenizer, get_template, inference, ModelType
import torch

###################################################################
# TESTING THE MODEL ON A SINGLE IMAGE
###################################################################

# UPDATE THESE TWO PATHS
# Look in your output_accident_model folder for the latest run and checkpoint
adapter_dir = "./output_accident_model/v6-20260312-020502/checkpoint-372"

# The path to the image you want to test
test_image_path = "D:\\Projects\\SaxionPA\\TestImages\\test_crash1.jpg" 
# ==========================================

print("Loading the 7-Billion parameter brain and your custom adapter...")
print("(This takes a minute, grabbing a coffee is recommended)")

model_kwargs = {
    'device_map': 'auto',
    'quantization_config': {'load_in_4bit': True}
}

model, tokenizer = get_model_tokenizer(
    ModelType.qwen2_5_vl_7b_instruct, 
    torch.float16, 
    model_kwargs=model_kwargs,
    adapter_id=adapter_dir
)

template = get_template(model.template_type, tokenizer)

query = "<image>\nAnalyze this CCTV frame. Is there an accident happening?"

print(f"\nAnalyzing the footage: {test_image_path}...")

response, history = inference(model, template, query, images=[test_image_path])

print("\n" + "="*40)
print("🚨 AI SURVEILLANCE REPORT 🚨")
print("="*40)
print(response)
print("="*40 + "\n")