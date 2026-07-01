# -*- coding: utf-8 -*-
"""Build a change-summary DOCX (old full-paper -> v2_RiskScore), then convert to PDF."""
import sys
sys.stdout.reconfigure(encoding='utf-8')
from docx import Document
from docx.shared import Pt, RGBColor, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH

RED   = RGBColor(0xC0, 0x00, 0x00)
GREEN = RGBColor(0x00, 0x70, 0x30)
BLUE  = RGBColor(0x1F, 0x3B, 0x73)
GREY  = RGBColor(0x55, 0x55, 0x55)

doc = Document()
# base font
st = doc.styles['Normal']
st.font.name = 'Calibri'
st.font.size = Pt(10.5)

# ---- title ----
h = doc.add_heading('', level=0)
r = h.add_run('Summary of Revisions')
r.font.size = Pt(20); r.font.color.rgb = BLUE; r.bold = True
sub = doc.add_paragraph()
rs = sub.add_run('M-ID267600 — changes from "full paper to Reviewer" → "v2_RiskScore"')
rs.font.size = Pt(11); rs.font.color.rgb = GREY; rs.italic = True
note = doc.add_paragraph()
rn = note.add_run('Legend:  ')
rn.bold = True; rn.font.size = Pt(9.5)
a = note.add_run('OLD (remove) '); a.font.color.rgb = RED; a.font.size = Pt(9.5); a.font.strike = True
b = note.add_run('   NEW (use this) '); b.font.color.rgb = GREEN; b.font.size = Pt(9.5)
c = note.add_run('   + = newly added text'); c.font.color.rgb = GREY; c.font.size = Pt(9.5)
doc.add_paragraph()

def section(num, title):
    p = doc.add_paragraph()
    r = p.add_run(f'{num}. {title}')
    r.bold = True; r.font.size = Pt(12); r.font.color.rgb = BLUE
    p.space_before = Pt(8)

def loc(text):
    p = doc.add_paragraph()
    r = p.add_run(text)
    r.italic = True; r.font.size = Pt(9); r.font.color.rgb = GREY

def old(text):
    p = doc.add_paragraph(); p.paragraph_format.left_indent = Inches(0.25)
    lbl = p.add_run('เดิม:  '); lbl.bold = True; lbl.font.size = Pt(9.5); lbl.font.color.rgb = RED
    r = p.add_run(text); r.font.color.rgb = RED; r.font.strike = True; r.font.size = Pt(10)

def new(text, added=False):
    p = doc.add_paragraph(); p.paragraph_format.left_indent = Inches(0.25)
    lbl = p.add_run('+ เพิ่มใหม่:  ' if added else 'แก้เป็น:  ')
    lbl.bold = True; lbl.font.size = Pt(9.5); lbl.font.color.rgb = GREEN
    r = p.add_run(text); r.font.color.rgb = GREEN; r.font.size = Pt(10)

# ========================= CHANGES =========================

section(1, 'Title (ชื่อเรื่อง)')
old('… through a Hybrid Deep Learning and Machine Learning …')
new('… through a Dual-Pipeline Deep Learning and Machine Learning Framework for Integrated Risk Assessment')

section(2, 'Abstract')
loc('แก้ dataset + ตัวเลขผล + ตัด Grad-CAM/RF')
old('trained on the LUNA16 dataset … mAP50 of 0.6875 … notes … features such as nodule diameter, spiculation, anatomical lobe location, smoking history, cancer history … Random Forest (RF) … accuracy 0.9256 … F1 0.9575 … Grad-CAM …')
new('trained on the IQ-OTH/NCCD dataset of 649 annotated CT images … mAP50 of 0.687 … utilizes a structured dataset of 309 records with symptom- and risk-based features, including smoking status, chronic disease, fatigue, wheezing, shortness of breath … accuracy 0.929 … F1 0.953  (ตัด RF และ Grad-CAM ออก)')

section(3, 'Introduction — แก้คำ')
loc('ย่อหน้าแรก intro')
old('egregious cancer mortality rates')
new('alarming cancer mortality rates')

section(4, 'Introduction — เพิ่มย่อหน้า Novelty')
new('To address these gaps, this study proposes a dual-pipeline framework that, to the authors’ knowledge, is among the first to integrate a convolutional object detection model on CT images with a gradient-boosting classifier on structured clinical/symptom data, combining their outputs into a single interpretable risk score. (อธิบายความใหม่ 3 ด้าน: complementary modalities / controlled DL comparison / interpretable risk score)', added=True)

section(5, 'Objectives (ย่อหน้า "This study aims")')
new('เพิ่มข้อ (4): propose an integrated risk-scoring framework that combines the imaging and clinical pipelines into a single interpretable measure of lung cancer risk.', added=True)

section(6, 'Probability of Lung Cancer (Mayo Clinic equation)')
old('This study’s Machine Learning framework integrates the following key radiological features in differentiating between benign and malignant tumors.')
new('In addition to the symptom-based clinical data used to train our machine learning models, the established Mayo Clinic malignancy prediction model [34] incorporates … for estimating the probability of malignancy.  (เปลี่ยนเป็นการอ้างอิงสมการ Mayo เป็น reference ไม่ใช่ feature ที่เทรนเอง)')

section(7, 'Multi-view section — typo')
old('this study will emphasizes a focus on Axiel View')
new('this study emphasises a focus on Axial View')

section(8, 'Dataset preparation')
old('CT scan images from public datasets, including LUNA 16, which contains annotated … personal … nodule size, medical history … in accordance with Lung-RADS [20].')
new('CT scan images from the publicly available IQ-OTH/NCCD dataset, which contains annotated … demographic and symptom-based clinical … smoking status, respiratory symptoms …  (ตัด Lung-RADS ออก)')

section(9, 'Object Detection branch — เพิ่มรายละเอียด dataset')
new('split at the image level … The detection dataset comprised 649 axial CT images (IQ-OTH/NCCD), annotated via Roboflow, partitioned into 456 train / 96 valid / 97 test, with 277 benign and 1,173 malignant nodules. Two-stage annotation: (1) researchers annotated bounding boxes by radiological criteria; (2) compared against a physician-verified set as reliable ground truth.', added=True)

section(10, 'Machine Learning branch — แก้ + เพิ่ม')
old('structured patients and nodule data … features are shown … nodule diameter, nodule density … family cancer history is split into … test sets at … ratio 80:20. … Table 1 … [24].')
new('structured patient data … features is shown … gender, anxiety, peer pressure, chronic disease, fatigue, allergy, wheezing, alcohol consumption, coughing, shortness of breath, swallowing difficulty, chest pain … evaluated using 10-fold stratified cross-validation, with SMOTE applied within each fold (no leakage); mean across folds. Dataset 309 records (270 positive / 39 negative), imbalance ~6.9:1 motivating SMOTE. … Table 3 … [24, 26].')

section(11, 'Model evaluation — ตัด Grad-CAM')
old('Model interpretability is further assessed using Grad-CAM to generate visual explanations for the predictions produced by the Object Detection branch [26].   (ลบทั้งประโยค)')

section(12, 'Integrated Risk Scoring — Section ใหม่ทั้งหมด')
new('หัวข้อใหม่ "Integrated Risk Scoring" + ย่อหน้าอธิบาย + สมการ (11) Risk Score = P(malignant)×50 + P(cancer)×50 + Table 2 ตัวอย่าง case.', added=True)

section(13, 'Results — ML comparison (เลข Table)')
old('Table 2 and Figure 8 present … / Table 2 Performance comparison of various machine learning models.')
new('Table 3 and Figure 8 present … / Table 3 Performance comparison of various machine learning models (Default parameter).')

section(14, 'CB Hyperparameter analysis (เลข Table + eta)')
old('Table 3-5 … a lower eta of 0.05 excels … / Table3 / Table4 / Table5 …')
new('Tables 4-6 … eta values of 0.05 and 0.20 yielded comparable results; 0.05 selected for stability … / Table 4 / Table 5 / Table 6 …')

section(15, 'Deep learning analysis (เลข Table + comma)')
old('Tables 6 and 7, offer … / Table 6 … / Table7 …')
new('Tables 7 and 8 offer … / Table 7 … / Table 8 …')

section(16, 'เพิ่ม: YOLO recall + Comparison/limitations')
new('ย่อหน้าใหม่อธิบาย low recall (0.435) ของ YOLOv8n (dataset เล็ก, single-annotator, mAP50 0.385→0.687 เมื่อ doctor-verified) + หัวข้อใหม่ "Comparison with previous studies and limitations" (เทียบงานก่อนหน้า + ข้อจำกัด 4 ข้อ).', added=True)

section(17, 'Conclusions — แก้คำ')
old('Through the usage of a two branch parallel pipeline …')
new('Through the use of a two-branch parallel pipeline …')

section(18, 'Performance of ML models (conclusion)')
old('… RF … accuracy 0.9256 … In another niche, the SVM model had a remarkable recall of 1.000 and was the most optimal model to prevent false negatives … F1 0.9575 … hence prove …')
new('… accuracy 0.929 … F1 0.953 … demonstrate …  (ตัดประโยค SVM recall 1.000 และ RF ออก)')

section(19, 'Performance of OD models (conclusion)')
old('classify benign and malignant tumor based on CT scan images …')
new('classify benign and malignant tumors based on CT scan images … + เพิ่มคำอธิบาย low recall 0.435 (dataset 110 cases/1,190 images, single-annotator; mAP50 0.385→0.687).')

section(20, 'Clinical significance — typo')
old('… dual-pipeline frameworks … shows great promise towards early dection …')
new('… show great promise towards early detection …')

section(21, 'References — เปลี่ยน/เพิ่ม')
new('• [7] LeCun … Deep learning  →  Hanna TN et al. Effect of Shift/Schedule/Volume on Interpretive Accuracy. Radiology 2018.\n'
    '• [20] Setio (LUNA16 challenge)  →  Al-Yasriy HF et al. Diagnosis of Lung Cancer Based on CT Scans Using CNN. 2020 (IQ-OTH/NCCD).\n'
    '• Goodfellow, Deep learning  →  Joseph VR. Optimal ratio for data splitting. 2022.\n'
    '• Granberg / Lundeen  →  CatBoost (Prokhorenkova 2018) + Ultralytics YOLOv8 (Jocher 2023).\n'
    '• เพิ่ม [34] Swensen (Mayo), [35] McWilliams (probability of cancer), [36] Huang (CT+clinical fusion).', added=True)

doc.add_paragraph()
tail = doc.add_paragraph()
rt = tail.add_run('หมายเหตุ: ในไฟล์ v2_RiskScore ข้อความที่แก้/เพิ่มทั้งหมด mark สีแดงไว้แล้ว — เปิดเทียบได้โดยตรง')
rt.italic = True; rt.font.size = Pt(9); rt.font.color.rgb = GREY

OUT = 'M-ID267600_Changes_Summary.docx'
doc.save(OUT)
print('Saved', OUT)
