from huggingface_hub import hf_hub_download
from ultralytics import YOLO

# Das Modell von Hugging Face laden
model_path = hf_hub_download(repo_id="arnabdhar/YOLOv8-Face-Detection", filename="model.pt")
print(f"Model downloaded to: {model_path}")
model = YOLO(model_path)