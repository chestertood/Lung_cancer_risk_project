from ultralytics import YOLO
import cv2
import numpy as np
import torch
import pandas as pd
# print(torch.__version__)
# print(torch.cuda.is_available())

picture = cv2.imread(r"The IQ-OTHNCCD lung cancer dataset/The IQ-OTHNCCD lung cancer dataset/Malignant cases/Malignant case (2).jpg")
alpha = 1  # คอนทราสต์
beta = 100    # ความสว่าง
adjusted_img = cv2.convertScaleAbs(picture, alpha=alpha, beta=beta)

# (ปรับ exposure โดยรวม)
gamma = 0.2  # ค่ากำหนดการปรับแสง
lookUpTable = np.empty((1, 256), np.uint8)
for i in range(256):
    lookUpTable[0][i] = np.clip(((i / 255.0) ** (1.0 / gamma)) * 255.0, 0, 255)

gamma_corrected = cv2.LUT(adjusted_img, lookUpTable)
gamma_corrected = cv2.resize(gamma_corrected, (624, 624))

path = r"Picture4_exposure.jpg"

# แสดงผลภาพที่ปรับค่า exposure
cv2.imshow('Exposure Adjusted Image', gamma_corrected)
cv2.imwrite(path, gamma_corrected)
cv2.waitKey(0)


