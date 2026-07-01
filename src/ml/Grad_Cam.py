from ultralytics import YOLO
model = YOLO("runs/detect/train23/weights/best.pt")
results = model("cancer_test_valid/Picture2.jpg")
# เรียก gradcam ได้เลย