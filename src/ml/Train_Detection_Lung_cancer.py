from ultralytics import YOLO
import cv2
import numpy as np
import torch
import pandas as pd
import tensorflow as tf
import tensorflow_hub as hub

# print(torch.__version__)
# print(torch.cuda.is_available())
# print(tf.__version__)
# print("The following GPU devices are available: %s" % tf.test.gpu_device_name())


#### YOLO x Pytorch ##### 
yolo_models = ["yolov6n.yaml","yolov8n.pt", "yolov9c.pt" , "yolov10n.pt" , "yolo11n.pt" ]
# yolo_models = ["yolov6n.yaml"] 

# for i in yolo_models:
#     print(f"Loading model: {i}")
#     model = YOLO(i)
#     model.train(data="cancer_lastest/data.yaml", epochs=100, imgsz=624 , batch=8 , workers=0 , augment=True, device='0' )
########## END ###########    

####### Tensorflow ##########


# Test
model_test = YOLO("runs/detect/train22/weights/best.pt")
result = model_test.val(data="verify_lungcancer_by_doctor/data.yaml" , workers=0 , device='0')
print(f"ความแม่นยำเฉลี่ย: {result.box.map50:.2%}")

# for i in range(1, 33):
#     results = model_test.predict(source = f"cancer_test_valid/Picture{i}.jpg"
#     , show=False, save=True, conf=0.2, iou=0.45, device='0',save_crop=True ,save_txt=True ,project='custom_project', name=f'my_results_{i}')
#     print(results)

# for i in range(1, 33):
#     path = f"custom_project/my_results_{i}/Picture{i}.jpg"
#     img = cv2.imread(path)

#     # เช็คก่อนว่าอ่านรูปเจอไหม (กันโปรแกรมเด้ง)
#     if img is not None:
#         # 2. สร้าง Path ปลายทาง
#         save_path = f"Detection_tumor/Picture{i}.jpg"
        
#         # 3. บันทึกรูปลงโฟลเดอร์ใหม่
#         cv2.imwrite(save_path, img)
        
#         print(f"บันทึกแล้ว: {save_path}")
        
#         # cv2.imshow(f"Result_{i}", img) # แนะนำให้ปิดบรรทัดนี้ ไม่งั้นหน้าต่างเด้งขึ้นมา 32 อันครับ
#         # cv2.waitKey(100) # ถ้าจะเปิดดูจริงๆ ให้ใส่ delay หน่อย
#     else:
#         print(f"หาไฟล์ไม่เจอ: {path}")

# print("เสร็จสิ้นการรวมรูปภาพครับ!")
