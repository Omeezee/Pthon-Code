import fitz                       # PyMuPDF
import camelot                   # table extraction
from reportlab.pdfgen.canvas import Canvas
from reportlab.platypus import Table, TableStyle
from reportlab.lib import colors
from googletrans import Translator
import arabic_reshaper
from bidi.algorithm import get_display

# ——— CONFIG ———
IN_PDF = r"C:\Users\geode\Downloads\trialtwopdftranslator.pdf"
OUT_PDF   = "output_arabic.pdf"
LANG_FROM = "en"
LANG_TO   = "ar"

# ——— SETUP ———
doc        = fitz.open(IN_PDF)
translator = Translator()
c_out      = Canvas(OUT_PDF, pagesize=(doc[0].rect.width, doc[0].rect.height))

for pageno in range(len(doc)):
    page = doc[pageno]
    w, h  = page.rect.width, page.rect.height

    # 1) EXTRACT TEXT BLOCKS & TABLE BBOXES
    blocks = []
    for b in page.get_text("dict")["blocks"]:
        if "lines" not in b: continue
        text = "".join(span["text"] for line in b["lines"] for span in line["spans"])
        blocks.append({
            "bbox": b["bbox"],
            "font": b["lines"][0]["spans"][0]["font"],
            "size": b["lines"][0]["spans"][0]["size"],
            "text": text.strip()
        })

    tables = camelot.read_pdf(IN_PDF, pages=str(pageno+1), flavor="lattice")

    # 2) REDACT (blank out) all original text & tables
    for blk in blocks:
        page.add_redact_annot(blk["bbox"], fill=(1,1,1))  # white box
    for tbl in tables:
        page.add_redact_annot(tbl._bbox,   fill=(1,1,1))
    page.apply_redactions()

    # 3) RENDER REDACTED PAGE TO IMAGE (keeps figures/backgrounds)
    pix = page.get_pixmap(dpi=200)
    bg  = f"tmp_page_{pageno}.png"
    pix.save(bg)

    # 4) TRANSLATE & SHAPE each text block
    for blk in blocks:
        if not blk["text"]: 
            blk["text_ar"] = ""
            continue
        tr = translator.translate(blk["text"], src=LANG_FROM, dest=LANG_TO).text
        # Arabic reshaping + bidi
        reshaped = arabic_reshaper.reshape(tr)
        bidi_text = get_display(reshaped)
        blk["text_ar"] = bidi_text

    # 5) TRANSLATE each table cell
    translated_tables = []
    for tbl in tables:
        df = tbl.df.copy()
        for i in range(df.shape[0]):
            for j in range(df.shape[1]):
                cell = df.iat[i,j].strip()
                if cell:
                    tr = translator.translate(cell, src=LANG_FROM, dest=LANG_TO).text
                    # shape + bidi
                    reshaped = arabic_reshaper.reshape(tr)
                    df.iat[i,j] = get_display(reshaped)
        translated_tables.append((tbl._bbox, df))

    # 6) DRAW A NEW PAGE
    c_out.setPageSize((w, h))
    c_out.drawImage(bg, 0, 0, width=w, height=h)

    #   6A) text blocks
    for blk in blocks:
        x0, y0, x1, y1 = blk["bbox"]
        rl_y = h - y1
        c_out.setFont(blk["font"], blk["size"])
        # right‑align for RTL: drawRightString at the right edge
        c_out.drawRightString(x1, rl_y, blk["text_ar"])

    #   6B) tables
    for bbox, df in translated_tables:
        x0, y0, x1, y1 = bbox
        rl_y = h - y1
        data = df.values.tolist()
        tbl = Table(
            data,
            colWidths=(x1-x0)/df.shape[1],
            rowHeights=(y1-y0)/df.shape[0]
        )
        tbl.setStyle(TableStyle([
            ("GRID",         (0,0), (-1,-1), 0.5, colors.black),
            ("FONT",         (0,0), (-1,-1), "Helvetica", 8),
            ("ALIGN",        (0,0), (-1,-1), "RIGHT"),   # RTL cells
        ]))
        tbl.wrapOn(c_out, x1-x0, y1-y0)
        tbl.drawOn(c_out, x0, rl_y)

    c_out.showPage()

c_out.save()
print(f"✅ Saved Arabic‑translated PDF as {OUT_PDF}")
