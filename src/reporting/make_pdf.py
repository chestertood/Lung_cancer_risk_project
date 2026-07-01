from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

pdfmetrics.registerFont(TTFont('ArialUni', 'C:/Windows/Fonts/ARIALUNI.ttf'))

FONT = 'ArialUni'
RED    = colors.HexColor('#C0392B')
ORANGE = colors.HexColor('#E67E22')
GREEN  = colors.HexColor('#27AE60')
BLUE   = colors.HexColor('#2980B9')
DARK   = colors.HexColor('#1A1A2E')
LIGHT_RED  = colors.HexColor('#FADBD8')
LIGHT_GRN  = colors.HexColor('#D5F5E3')
GRAY_BG    = colors.HexColor('#F2F3F4')
WHITE      = colors.white

doc = SimpleDocTemplate(
    'Reviewer_Feedback_Summary.pdf',
    pagesize=A4,
    rightMargin=2*cm, leftMargin=2*cm,
    topMargin=2*cm, bottomMargin=2*cm
)
W = A4[0] - 4*cm

def S(size, bold=False, color=DARK, leading=None):
    return ParagraphStyle('x', fontName=FONT, fontSize=size, textColor=color,
                          leading=leading or size*1.4, wordWrap='CJK')

def P(text, style): return Paragraph(text, style)

story = []

story.append(P('สรุป Reviewer Feedback — M-ID267600 (Updated)', S(18, bold=True, color=BLUE)))
story.append(Spacer(1, 4))
story.append(P('สถานะล่าสุด — สิ่งที่ยังต้องแก้', S(11, color=colors.HexColor('#555555'))))
story.append(HRFlowable(width=W, thickness=2, color=BLUE, spaceAfter=10))

# ── Priority table ────────────────────────────────────────────
def sec(text, bg, fg=WHITE):
    t = Table([[P(text, ParagraphStyle('h', fontName=FONT, fontSize=11,
                  textColor=fg, wordWrap='CJK', leading=15))]], colWidths=[W])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), bg),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('LEFTPADDING', (0,0), (-1,-1), 10),
    ]))
    return t

# ══════════════════════════════════════════════════════════════
# SECTION 1: ยังไม่แก้ (Critical)
# ══════════════════════════════════════════════════════════════
story.append(sec('ยังต้องแก้ — Critical', RED))
story.append(Spacer(1, 6))

remaining = [
    ('1', 'Citation Mismatch (ร้ายแรงสุด)',
     ['[22] → ควรเป็น reference สำหรับ 70:15:15 split ไม่ใช่ Goodfellow',
      '[26] → ควรเป็น Selvaraju et al. 2017 (Grad-CAM) ไม่ใช่ Bergstra & Bengio',
      '[28] → ควรเป็น reference สำหรับ YOLOv8n ไม่ใช่ pulmonary hamartoma',
      '[6] → ควรเป็น reference สำหรับ radiologist workload ไม่ใช่ LeCun et al.',
      'ต้องเช็ค reference ทั้งหมดและ renumber']),
]

for num, title, bullets in remaining:
    rows = [[P(f'{num}. {title}', ParagraphStyle('t', fontName=FONT, fontSize=10,
                textColor=RED, wordWrap='CJK', leading=14))]]
    for b in bullets:
        rows.append([P(f'• {b}', ParagraphStyle('b', fontName=FONT, fontSize=9,
                       textColor=DARK, wordWrap='CJK', leading=13))])
    t = Table(rows, colWidths=[W-1.2*cm])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), LIGHT_RED),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ('LEFTPADDING', (0,0), (-1,-1), 10),
        ('LINEBEFORE', (0,0), (0,-1), 3, RED),
        ('LINEAFTER',  (0,0), (0,-1), 3, RED),
        ('LINEABOVE',  (0,0), (-1,0), 1, RED),
        ('LINEBELOW',  (0,-1), (-1,-1), 1, RED),
    ]))
    story.append(t)
    story.append(Spacer(1, 6))

# ══════════════════════════════════════════════════════════════
# SECTION 2: ยังไม่แก้ (Moderate)
# ══════════════════════════════════════════════════════════════
story.append(Spacer(1, 6))
story.append(sec('ยังต้องแก้ — Moderate', ORANGE))
story.append(Spacer(1, 6))

moderate = [
    ('8', 'YOLO Recall ต่ำ — ต้องอธิบายใน Discussion',
     ['YOLOv8n recall ≈ 0.435 ต่ำมากสำหรับ cancer screening',
      'อธิบายสาเหตุ: dataset เล็ก, annotation โดยนักวิจัยไม่ใช่แพทย์',
      'เสนอแนวทางปรับปรุง: เพิ่ม data, expert annotation']),
    ('9', 'Discussion อ่อน — ต้องเพิ่ม',
     ['Compare กับ previous studies (อ้างงานอื่นที่ได้ mAP ใกล้เคียง)',
      'ระบุ limitations ชัดเจน (dataset size, image-level split, no external validation)',
      'ลด overclaim เรื่อง clinical deployment']),
]

for num, title, bullets in moderate:
    rows = [[P(f'{num}. {title}', ParagraphStyle('t', fontName=FONT, fontSize=10,
                textColor=ORANGE, wordWrap='CJK', leading=14))]]
    for b in bullets:
        rows.append([P(f'• {b}', ParagraphStyle('b', fontName=FONT, fontSize=9,
                       textColor=DARK, wordWrap='CJK', leading=13))])
    t = Table(rows, colWidths=[W-1.2*cm])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#FDEBD0')),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ('LEFTPADDING', (0,0), (-1,-1), 10),
        ('LINEBEFORE', (0,0), (0,-1), 3, ORANGE),
        ('LINEAFTER',  (0,0), (0,-1), 3, ORANGE),
        ('LINEABOVE',  (0,0), (-1,0), 1, ORANGE),
        ('LINEBELOW',  (0,-1), (-1,-1), 1, ORANGE),
    ]))
    story.append(t)
    story.append(Spacer(1, 6))

# ══════════════════════════════════════════════════════════════
# SECTION 3: แก้แล้ว
# ══════════════════════════════════════════════════════════════
story.append(Spacer(1, 6))
story.append(sec('แก้แล้ว ✓', GREEN))
story.append(Spacer(1, 6))

done_items = [
    '2. Feature Inconsistency ML Branch — text, Figure 6, features ตรงกับ survey dataset แล้ว',
    '3. ตัวเลข — Abstract, Table, Conclusion consistent หมดแล้ว (0.953, 0.929)',
    '4. "Hybrid" → "Dual-Pipeline" และ Grad-CAM claim ลบออกแล้ว',
    '5. Data Leakage — image-level (YOLO) และ patient-level (ML) + SMOTE in train only',
    '6. Abstract — dataset detail, validation procedure เพิ่มแล้ว',
    '7. Methodology — 2-phase annotation, IQ-OTH/NCCD source ระบุแล้ว',
    '8. Table 2 caption — เพิ่ม (Default parameter) แล้ว',
    '10. Lines 117-121 — ลบ "expected" แล้ว',
    '11. Figure 1 Flowchart — แก้ symbols แล้ว',
    '12. Lines 319-320 — 80:20 split justified แล้ว',
    '13. References — เช็คครบแล้ว',
]

for item in done_items:
    row = [[P(f'✓  {item}', ParagraphStyle('d', fontName=FONT, fontSize=9,
              textColor=colors.HexColor('#1E8449'), wordWrap='CJK', leading=13))]]
    t = Table(row, colWidths=[W-1.2*cm])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), LIGHT_GRN),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ('LEFTPADDING', (0,0), (-1,-1), 10),
        ('LINEBEFORE', (0,0), (0,-1), 3, GREEN),
    ]))
    story.append(t)
    story.append(Spacer(1, 3))

doc.build(story)
print('Done: Reviewer_Feedback_Summary.pdf')
