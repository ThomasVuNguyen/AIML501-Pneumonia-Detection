from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_CELL_VERTICAL_ALIGNMENT
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

OUT = '/Users/thomasthemaker/School/AIML 501/AIML501 Day 2 Streamlit Deployment Report.docx'
CROPS = '/private/tmp/claude-501/-Users-thomasthemaker-School-AIML-501/aa383bd3-df1c-4e65-a51f-dca4a1b0eff2/scratchpad/crops/'
FONT = 'Google Sans'
BLACK = RGBColor(0, 0, 0)
GREY = RGBColor(0x55, 0x55, 0x55)
RED = RGBColor(0xB0, 0x1E, 0x1E)

doc = Document()
sec = doc.sections[0]
sec.page_width, sec.page_height = Inches(8.5), Inches(11)
sec.top_margin = sec.bottom_margin = Inches(.6)
sec.left_margin = sec.right_margin = Inches(.75)

normal = doc.styles['Normal']
normal.font.name = FONT
normal.font.size = Pt(10)
normal.font.color.rgb = BLACK
normal.paragraph_format.space_after = Pt(3)
normal.paragraph_format.line_spacing = 1.05

for name, size, before, after in [('Title', 15, 0, 1), ('Heading 1', 11, 6, 2)]:
    st = doc.styles[name]
    st.font.name = FONT
    st.font.size = Pt(size)
    st.font.bold = True
    st.font.color.rgb = BLACK
    st.paragraph_format.space_before = Pt(before)
    st.paragraph_format.space_after = Pt(after)
    st.paragraph_format.keep_with_next = True
# Title style ships with a bottom border; drop it
pPr = doc.styles['Title'].element.get_or_add_pPr()
for b in pPr.findall(qn('w:pBdr')):
    pPr.remove(b)


def run(p, text, bold=False, italic=False, size=None, color=None):
    r = p.add_run(text)
    r.bold, r.italic = bold, italic
    r.font.name = FONT
    if size:
        r.font.size = Pt(size)
    if color is not None:
        r.font.color.rgb = color
    return r


def para(text='', size=None, color=None, after=None, align=None):
    p = doc.add_paragraph()
    if text:
        run(p, text, size=size, color=color)
    if after is not None:
        p.paragraph_format.space_after = Pt(after)
    if align is not None:
        p.alignment = align
    return p


def bullet(label, text):
    p = doc.add_paragraph(style='List Bullet')
    p.paragraph_format.space_after = Pt(2)
    p.paragraph_format.left_indent = Inches(.18)
    p.paragraph_format.first_line_indent = Inches(-.14)
    run(p, label, bold=True)
    run(p, text)
    return p


def shade(cell, hex_fill):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement('w:shd')
    shd.set(qn('w:val'), 'clear')
    shd.set(qn('w:color'), 'auto')
    shd.set(qn('w:fill'), hex_fill)
    tcPr.append(shd)


def cell_margins(table, top=30, bottom=30, left=70, right=70):
    tblPr = table._tbl.tblPr
    mar = OxmlElement('w:tblCellMar')
    for side, val in [('top', top), ('bottom', bottom), ('left', left), ('right', right)]:
        el = OxmlElement(f'w:{side}')
        el.set(qn('w:w'), str(val))
        el.set(qn('w:type'), 'dxa')
        mar.append(el)
    tblPr.append(mar)


def no_borders(table):
    tblPr = table._tbl.tblPr
    borders = OxmlElement('w:tblBorders')
    for side in ['top', 'left', 'bottom', 'right', 'insideH', 'insideV']:
        el = OxmlElement(f'w:{side}')
        el.set(qn('w:val'), 'nil')
        borders.append(el)
    tblPr.append(borders)


# ---------- Header ----------
doc.add_paragraph('AIML-501 Pneumonia Classifier: Day 1 and Day 2', style='Title')
p = para(after=4)
run(p, 'Group: [Member 1], [Member 2], [Member 3], [Member 4]  ·  November 21, 2026  ·  Live app: ', size=9, color=GREY)
run(p, 'aiml501-pneumonia-detection.streamlit.app', size=9, bold=True)
run(p, '  ·  Code: ', size=9, color=GREY)
run(p, 'github.com/ThomasVuNguyen/AIML501-Pneumonia-Detection', size=9, bold=True)

p = para(after=3)
run(p, 'Day 1, model development. ', bold=True)
run(p, 'Kaggle Chest X-Ray Images (Pneumonia): 5,856 X-rays of children aged 1–5 from one hospital; 74% of training '
       'images show pneumonia. We re-split training 80/20 (4,172 / 1,044, no duplicates across splits) and kept the '
       '624-image test set untouched. ResNet18 and DenseNet121 (ImageNet weights, frozen backbone, new 2-class head) '
       'were trained for 16 epochs with class-weighted cross-entropy and Adam. Best validation accuracy was 98.4% / 97.6%, '
       'but test accuracy was 83.3% / 80.9%: recall 0.985 / 0.990, specificity only 0.581 / 0.509, ROC-AUC 0.958 / 0.959.')
p = para(after=2)
run(p, 'Day 2, deployment and evaluation. ', bold=True)
run(p, 'A Streamlit app applies the Day 1 preprocessing (224×224, grayscale to 3 channels, ImageNet normalization) and '
       'runs both models on any upload. Code and weights are on GitHub; the app runs on Streamlit Community Cloud.')

# ---------- Results table ----------
doc.add_heading('Prediction comparison (live app)', level=1)
rows = [
    ('Test image', 'Actual', 'ResNet18', 'Prob.', 'DenseNet121', 'Prob.'),
    ('A. Original NORMAL (NORMAL_test)', 'NORMAL', 'NORMAL', '80.6%', 'NORMAL', '62.9%'),
    ('A. Original PNEUMONIA (PNEUMONIA_test)', 'PNEUMONIA', 'PNEUMONIA', '97.6%', 'PNEUMONIA', '96.8%'),
    ('B. External NORMAL (adult PA film)', 'NORMAL', 'PNEUMONIA ✗', '73.2%', 'NORMAL', '63.3%'),
    ('B. External PNEUMONIA (adult lobar)', 'PNEUMONIA', 'PNEUMONIA', '97.4%', 'PNEUMONIA', '99.9%'),
    ('C. Unrelated: dog photo', 'Not an X-ray', 'PNEUMONIA ✗', '99.7%', 'PNEUMONIA ✗', '100.0%'),
    ('C. Unrelated: tree photo', 'Not an X-ray', 'PNEUMONIA ✗', '97.4%', 'PNEUMONIA ✗', '98.6%'),
    ('C. Unrelated: car photo', 'Not an X-ray', 'PNEUMONIA ✗', '95.4%', 'PNEUMONIA ✗', '96.5%'),
]
widths = [Inches(2.45), Inches(.95), Inches(1.1), Inches(.6), Inches(1.15), Inches(.75)]
t = doc.add_table(rows=len(rows), cols=6)
t.style = 'Table Grid'
t.autofit = False
for j, w in enumerate(widths):
    t.columns[j].width = w
t.alignment = WD_TABLE_ALIGNMENT.CENTER
cell_margins(t, 15, 15, 60, 60)
for i, r in enumerate(rows):
    for j, val in enumerate(r):
        c = t.cell(i, j)
        c.width = widths[j]
        c.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER
        cp = c.paragraphs[0]
        cp.paragraph_format.space_after = Pt(0)
        if j in (3, 5):
            cp.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        wrong = '✗' in val
        run(cp, val, bold=(i == 0), size=8.5, color=RED if wrong else None)
        if i == 0:
            shade(c, 'E8E8E8')
para('Prob. = output probability for the predicted class. ✗ = wrong label (for photos, neither label is valid).', size=8, color=GREY, after=0)

# ---------- Screenshots ----------
doc.add_heading('Screenshots from the deployed app', level=1)
shots = [
    ('1_original_normal.png', 'A. Original NORMAL test image'),
    ('2_original_pneumonia.png', 'A. Original PNEUMONIA test image'),
    ('3_external_normal.png', 'B. External NORMAL (Wikimedia, CC0)'),
    ('4_external_pneumonia.png', 'B. External PNEUMONIA (Wikimedia, CC0)'),
    ('5_unrelated_dog.png', 'C. Unrelated image (tree and car screenshots in the repo)'),
]
g = doc.add_table(rows=3, cols=2)
no_borders(g)
cell_margins(g, 10, 10, 40, 40)
IMG_W = Inches(3.1)
for k, (fname, cap) in enumerate(shots):
    c = g.cell(k // 2, k % 2)
    c.width = Inches(3.5)
    c.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.TOP
    ip = c.paragraphs[0]
    ip.paragraph_format.space_after = Pt(0)
    ip.add_run().add_picture(CROPS + fname, width=IMG_W)
    cp = c.add_paragraph()
    cp.paragraph_format.space_after = Pt(2)
    run(cp, cap, size=7.5, italic=True, color=GREY)

# Recommendations sit in the empty sixth cell, next to the dog screenshot
rc = g.cell(2, 1)
rc.width = Inches(3.5)
rp = rc.paragraphs[0]
rp.paragraph_format.space_after = Pt(2)
run(rp, 'Recommendations', bold=True, size=9.5)
for label, text in [
    ('Reject invalid inputs: ', 'an X-ray-vs-other check or an out-of-distribution score before classifying.'),
    ('Flag uncertainty: ', 'send low-confidence results and model disagreements to a person.'),
    ('Calibrate: ', 'temperature scaling, and a decision threshold that raises specificity.'),
    ('Retrain: ', 'fine-tune deeper layers on multi-site adult and pediatric X-rays.'),
]:
    bp = rc.add_paragraph(style='List Bullet')
    bp.paragraph_format.space_after = Pt(1)
    bp.paragraph_format.left_indent = Inches(.16)
    bp.paragraph_format.first_line_indent = Inches(-.12)
    run(bp, label, bold=True, size=8.5)
    run(bp, text, size=8.5)

# ---------- Findings ----------
doc.add_heading('What we found', level=1)
bullet('Original test images: ',
       'all 4 right, but less sure of NORMAL (80.6%, 62.9%) than PNEUMONIA (~97%), as in Day 1, where 98 and '
       '115 of 234 healthy test X-rays were false positives.')
bullet('External X-rays: ',
       'trained on children, tested on adults. ResNet18 called the healthy adult PNEUMONIA (73.2%); DenseNet121 was '
       'right at only 63.3%; both caught the pneumonia. The only disagreement in 7 images.')
bullet('Unrelated images: ',
       'a dog, a tree and a car were all PNEUMONIA at 95–100%. A two-class softmax always sums to 100% and has no '
       '"not an X-ray" option, so high output probability is not a reliable prediction.')
bullet('Limitations: ',
       'single-site pediatric data, class imbalance (low specificity), no input validation, uncalibrated probabilities.')

para('Educational demo only, not a medical device. Seven images show generalization problems but are not an '
     'external validation study. Images: Kaggle; Wikimedia Commons (M. Häggström CC0, Aciarium CC BY 4.0, '
     'B. Embleton CC BY-SA 2.0, D. Case CC BY-SA 3.0).',
     size=7.5, color=GREY, after=0)

doc.save(OUT)
print('Saved', OUT)
