import pandas as pd
import matplotlib.pyplot as plt

# โหลดข้อมูลจากไฟล์ results.csv ที่ YOLO สร้างให้
results = pd.read_csv('yolo_mpa50.csv')
results.columns = results.columns.str.strip() # ลบช่องว่างที่ชื่อคอลัมน์

# ตั้งค่าฟอนต์ให้ใหญ่ขึ้น
plt.rcParams.update({'font.size': 20})

fig, ax = plt.subplots(figsize=(10, 60), dpi=150)

# ตัวอย่างการ Plot mAP50
# ax.plot(results['epoch'], results['YOLOv6n'], label='YOLOv6n', linewidth=3)
ax.plot(results['epoch'], results['YOLOv8n'], label='YOLOv8n', linewidth=3)
ax.plot(results['epoch'], results['YOLOv9c'], label='YOLOv9c', linewidth=3)
# ax.plot(results['epoch'], results['YOLOv10n'], label='YOLOv10n', linewidth=3)
ax.plot(results['epoch'], results['YOLOv11n'], label='YOLOv11n', linewidth=3)

ax.set_xlabel('Epochs', fontsize=28)
ax.set_ylabel('mAP50', fontsize=28)
ax.set_title('Training Performance', fontsize=28)
ax.grid(True)
ax.legend()

plt.show()