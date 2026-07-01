import sys, copy
from docx import Document
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
sys.stdout.reconfigure(encoding='utf-8')

FILE = 'M-ID267600_full paper to Reviewer.docx'

def _set_text(r_el, text):
    for t in r_el.findall(qn('w:t')):
        r_el.remove(t)
    t = OxmlElement('w:t')
    t.set(qn('xml:space'), 'preserve')
    t.text = text
    r_el.append(t)

def _make_red(r_el):
    rPr = r_el.find(qn('w:rPr'))
    if rPr is None:
        rPr = OxmlElement('w:rPr')
        r_el.insert(0, rPr)
    for c in rPr.findall(qn('w:color')):
        rPr.remove(c)
    color = OxmlElement('w:color')
    color.set(qn('w:val'), 'FF0000')
    rPr.append(color)

def replace_red(paragraph, old, new):
    """Replace `old` with `new` inside whichever run contains it; mark new red."""
    for run in paragraph.runs:
        if old in run.text:
            txt = run.text
            i = txt.find(old)
            before, after = txt[:i], txt[i+len(old):]
            r = run._r
            run.text = before
            mid = copy.deepcopy(r); _make_red(mid); _set_text(mid, new)
            aft = copy.deepcopy(r); _set_text(aft, after)
            r.addnext(aft); r.addnext(mid)
            return True
    return False

def set_para_red(paragraph, new_text):
    """Replace entire paragraph text with one red run, keeping para style."""
    runs = paragraph.runs
    if not runs:
        return False
    first = runs[0]
    # clear all but first
    for r in runs[1:]:
        r._r.getparent().remove(r._r)
    _make_red(first._r)
    _set_text(first._r, new_text)
    return True

if __name__ == '__main__':
    doc = Document(FILE)
    P = doc.paragraphs

    edits = [
        # (para_index, old, new)
        (2,  'trained on the LUNA16 dataset', 'trained on the IQ-OTH/NCCD dataset'),
        (42, 'public datasets, including LUNA 16, which',
             'the publicly available IQ-OTH/NCCD dataset, which'),
    ]

    for idx, old, new in edits:
        ok = replace_red(P[idx], old, new)
        print(('OK  ' if ok else 'FAIL') + f' para {idx}: {old[:40]}...')

    doc.save(FILE)
    print('\nSaved.')
