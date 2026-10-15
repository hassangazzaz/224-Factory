from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
                                Image, PageBreak, KeepTogether)
from reportlab.graphics.shapes import Drawing, Polygon, Line, String, Rect, Group
from reportlab.graphics import renderPDF
import sys

SHIRT_IMG, SHORTS_IMG, OUT = sys.argv[1], sys.argv[2], sys.argv[3]

BURG = colors.HexColor("#5A1F2B")
GOLD = colors.HexColor("#D9A441")
GREY = colors.HexColor("#F2EEEE")
LINE = colors.HexColor("#BBAAAA")

ss = getSampleStyleSheet()
H1 = ParagraphStyle("H1", parent=ss["Title"], fontSize=20, textColor=BURG, alignment=0, spaceAfter=4)
H2 = ParagraphStyle("H2", parent=ss["Heading2"], fontSize=13, textColor=BURG, spaceBefore=10, spaceAfter=4)
B = ParagraphStyle("B", parent=ss["BodyText"], fontSize=9, leading=12)
SM = ParagraphStyle("SM", parent=B, fontSize=8, leading=10, textColor=colors.HexColor("#555555"))
TC = ParagraphStyle("TC", parent=B, fontSize=8.5, leading=11)


def P(t, s=TC):
    return Paragraph(t, s)


def table(rows, widths, header=True):
    data = [[P(c) if isinstance(c, str) else c for c in r] for r in rows]
    t = Table(data, colWidths=widths, repeatRows=1 if header else 0)
    st = [("GRID", (0, 0), (-1, -1), 0.4, LINE),
          ("VALIGN", (0, 0), (-1, -1), "TOP"),
          ("LEFTPADDING", (0, 0), (-1, -1), 4), ("RIGHTPADDING", (0, 0), (-1, -1), 4)]
    if header:
        st += [("BACKGROUND", (0, 0), (-1, 0), BURG), ("TEXTCOLOR", (0, 0), (-1, 0), colors.white)]
        data[0] = [P(f"<font color='white'><b>{c.text if hasattr(c,'text') else c}</b></font>") for c in data[0]]
        t = Table(data, colWidths=widths, repeatRows=1)
    else:
        st += [("BACKGROUND", (0, 0), (0, -1), GREY)]
    t.setStyle(TableStyle(st))
    return t


def header_block(style_no, name):
    rows = [["Brand", "224 (Saudi Arabia)", "Style no.", style_no],
            ["Garment", name, "Season", "First collection 2026/27"],
            ["Fit", "Slim fit, men's", "Order qty", "50 pcs"],
            ["Contact", "Hassan Gazzaz, Founder<br/>hassangazzaz225@gmail.com<br/>WhatsApp +966 50 558 1955",
             "Version / date", "v1 / 15 Oct 2026"]]
    t = Table([[P(c) for c in r] for r in rows], colWidths=[2.6*cm, 6.4*cm, 2.8*cm, 5.2*cm])
    t.setStyle(TableStyle([("GRID", (0, 0), (-1, -1), 0.4, LINE),
                           ("BACKGROUND", (0, 0), (0, -1), GREY), ("BACKGROUND", (2, 0), (2, -1), GREY),
                           ("VALIGN", (0, 0), (-1, -1), "TOP")]))
    return t


def img(path, w):
    from PIL import Image as PI
    im = PI.open(path)
    h = w * im.height / im.width
    return Image(path, width=w, height=h)


# ---------- schematic back views ----------
def shirt_back():
    d = Drawing(7.5*cm, 8.5*cm)
    s = cm
    body = Polygon([1.6*s, 7.6*s, 2.9*s, 8.0*s, 4.6*s, 8.0*s, 5.9*s, 7.6*s, 7.2*s, 6.2*s, 6.5*s, 5.5*s,
                    5.9*s, 6.0*s, 5.9*s, 0.4*s, 1.6*s, 0.4*s, 1.6*s, 6.0*s, 1.0*s, 5.5*s, 0.3*s, 6.2*s],
                   fillColor=BURG, strokeColor=colors.black, strokeWidth=0.6)
    d.add(body)
    d.add(Rect(2.9*s, 7.75*s, 1.7*s, 0.35*s, fillColor=BURG, strokeColor=colors.black, strokeWidth=0.6))  # collar
    # gold piping on sleeve hems
    d.add(Line(0.3*s, 6.2*s, 1.0*s, 5.5*s, strokeColor=GOLD, strokeWidth=2))
    d.add(Line(7.2*s, 6.2*s, 6.5*s, 5.5*s, strokeColor=GOLD, strokeWidth=2))
    # stripes on wearer's left shoulder (seen on the left in back view)
    for off in (0, 0.18):
        d.add(Line((2.9-off)*s, (8.0-off*0.3)*s, (0.55-off)*s, (6.0-off)*s, strokeColor=GOLD, strokeWidth=1.6))
    # vertical embroidery
    g = Group(String(0, 0, "224 •", fontName="Helvetica-Bold", fontSize=13, fillColor=GOLD))
    g.rotate(-90)
    g.translate(-7.1*s, 3.55*s)
    d.add(g)
    d.add(String(0.1*s, 0.0*s, "BACK VIEW (schematic)", fontSize=7))
    d.add(Line(5.2*s, 7.75*s, 5.2*s, 7.1*s, strokeColor=colors.black, strokeWidth=0.4))
    d.add(String(5.3*s, 7.3*s, "8 cm", fontSize=7))
    return d


def shorts_back():
    d = Drawing(7.5*cm, 7.0*cm)
    s = cm
    d.add(Rect(1.0*s, 5.6*s, 5.5*s, 0.8*s, fillColor=BURG, strokeColor=colors.black, strokeWidth=0.6))
    body = Polygon([1.0*s, 5.6*s, 6.5*s, 5.6*s, 7.0*s, 1.0*s, 4.1*s, 1.0*s, 3.75*s, 3.2*s,
                    3.4*s, 1.0*s, 0.5*s, 1.0*s], fillColor=BURG, strokeColor=colors.black, strokeWidth=0.6)
    d.add(body)
    for x, ang in ((1.05, -94), (6.35, -86)):
        g = Group(String(0, 0, "224 •", fontName="Helvetica-Bold", fontSize=10, fillColor=GOLD))
        g.rotate(-90)
        g.translate(-5.1*s, x*s)
        d.add(g)
    d.add(String(0.1*s, 0.2*s, "BACK VIEW (schematic) - embroidery each side", fontSize=7))
    return d


def build():
    doc = SimpleDocTemplate(OUT, pagesize=A4, leftMargin=2*cm, rightMargin=2*cm,
                            topMargin=1.6*cm, bottomMargin=1.6*cm,
                            title="224 Tech Pack - Button-up Shirt & Shorts", author="224")
    W = A4[0] - 4*cm
    f = []

    # ---------- COVER / GENERAL ----------
    f += [Paragraph("224 &nbsp;|&nbsp; TECH PACK", H1),
          Paragraph("First production run: short-sleeve button-up shirt (224-SH01) and shorts (224-SO01)", B),
          Spacer(1, 8)]
    f.append(Paragraph("General requirements (both styles)", H2))
    f.append(table([
        ["Item", "Requirement"],
        ["Quantity", "50 pcs per style (shirt 50, shorts 50)"],
        ["Fabric rule", "<b>Cotton. No polyester.</b> Cotton/elastane (approx. 3-5% elastane) preferred for stretch if available. "
                        "Shirt and shorts may be different fabrics. Factory to propose stock options."],
        ["Main colour", "Burgundy - target Pantone 19-1617 TCX (Burgundy) or closest available stock colour. "
                        "Please send swatch/lab dip for approval."],
        ["Accent colour", "Gold - target Pantone 15-1142 TCX (Honey Gold) or closest. Used for stripes, piping, buttons, zips, embroidery."],
        ["Branding", "\"224 •\" embroidered in gold thread, vertical (reads top to bottom). Shirt: centre back. Shorts: both sides. "
                     "No other logos from factory (chest symbol and patches are applied in Saudi Arabia)."],
        ["Labels", "Brand neck/waist label: 224 woven label (artwork to follow - factory to quote). "
                   "Care/composition label in side seam (factory standard, English)."],
        ["Packing", "Each piece folded, individual clear bag (non-plastic/recyclable preferred), size sticker on bag. "
                    "Cartons mixed sizes OK, packing list per carton."],
        ["Shipping", "Destination Jeddah, Saudi Arabia. Please quote air freight (DAP if possible)."],
        ["Tolerance", "Measurements +/- 1 cm unless stated."],
    ], [3.2*cm, W-3.2*cm]))

    f.append(Paragraph("Size breakdown (proposed)", H2))
    f.append(table([["Style", "S", "M", "L", "XL", "Total"],
                    ["224-SH01 Shirt", "10", "18", "15", "7", "50"],
                    ["224-SO01 Shorts", "10", "18", "15", "7", "50"]],
                   [5*cm] + [2.2*cm]*5))
    f.append(Spacer(1, 6))
    f.append(Paragraph("Items marked <b>TBC</b> are open for the factory's advice and will be confirmed after the first sample.", SM))
    f.append(PageBreak())

    # ---------- SHIRT ----------
    f += [Paragraph("224-SH01 &nbsp;Short-sleeve button-up shirt", H1), header_block("224-SH01", "Short-sleeve button-up shirt"),
          Spacer(1, 8)]
    pics = Table([[img(SHIRT_IMG, 7.6*cm), shirt_back()]], colWidths=[W/2, W/2])
    pics.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "MIDDLE"), ("ALIGN", (0, 0), (-1, -1), "CENTER")]))
    f += [pics, Paragraph("Left: front design visual (reference). Right: back view showing embroidery placement.", SM)]

    f.append(Paragraph("Fabric &amp; trims", H2))
    f.append(table([
        ["Component", "Specification", "Notes"],
        ["Main fabric", "Cotton jersey or cotton piqué knit, approx. 180-200 GSM. Cotton/elastane preferred.", "No polyester. Factory to propose stock options. TBC"],
        ["Colour", "Burgundy (Pantone 19-1617 TCX or closest)", "Lab dip / swatch approval"],
        ["Shoulder stripes", "2 gold stripes, each 1.0 cm wide, 0.5 cm gap. Knit tape or contrast insert.", "Cotton tape preferred. TBC"],
        ["Sleeve hem piping", "Gold piping approx. 0.4 cm, on both sleeve hems", ""],
        ["Buttons", "Gold/tan, 4-hole, 15 mm (18L). 1 collar + 7 placket = 8 pcs + 1 spare", "Horn-look or metal-look; no plastic shine preferred"],
        ["Interlining", "Light fusible in collar and placket", ""],
        ["Sewing thread", "Burgundy, colour-matched", ""],
        ["Embroidery thread", "Gold (metallic or viscose)", "See embroidery spec"],
    ], [3.3*cm, 8.2*cm, W-11.5*cm]))

    f.append(Paragraph("Construction", H2))
    f.append(table([
        ["Area", "Detail"],
        ["Collar", "Classic point collar with collar stand. Collar point length approx. 7 cm. Top button on collar stand."],
        ["Front", "Full button-through placket, 3 cm wide, 7 buttons on placket + 1 on collar stand, evenly spaced. No chest pocket."],
        ["Shoulders", "Set-in sleeves. Two gold stripes run from the neck seam along the <b>wearer's left</b> shoulder and down the outer sleeve to the hem."],
        ["Sleeves", "Short sleeve with turned-back cuff / band, approx. 2.5 cm. Gold piping at hem edge on both sleeves."],
        ["Back", "Plain back, no yoke pleat. \"224 •\" embroidery centre back (see below)."],
        ["Hem", "Straight hem, 2 cm double-turned (or coverstitch if knit)."],
        ["Seams", "Side seams overlocked + topstitched; neat finish inside. Slim fit."],
    ], [3*cm, W-3*cm]))

    f.append(Paragraph("Embroidery - \"224 •\" centre back", H2))
    f.append(table([
        ["Spec", "Value"],
        ["Text", "224 • (characters 2-2-4, space, dot)"],
        ["Orientation", "Vertical, reading top to bottom, centred on centre back"],
        ["Position", "Starts 8 cm below back neck seam"],
        ["Size", "Letter height approx. 2.5 cm; total length approx. 10 cm"],
        ["Thread / type", "Gold thread, flat satin stitch"],
    ], [3.5*cm, W-3.5*cm]))
    f.append(PageBreak())

    f.append(Paragraph("224-SH01 &nbsp;Measurement chart (cm, garment laid flat)", H2))
    f.append(table([
        ["Code", "Point of measure", "S", "M", "L", "XL", "Tol."],
        ["A", "Chest width (2.5 cm below armhole)", "50", "53", "56", "59", "1"],
        ["B", "Body length (HPS to hem)", "70", "72", "74", "76", "1"],
        ["C", "Shoulder width (seam to seam)", "43", "45", "47", "49", "1"],
        ["D", "Sleeve length (shoulder point to hem)", "21", "22", "23", "24", "0.5"],
        ["E", "Sleeve opening width", "17", "18", "19", "20", "0.5"],
        ["F", "Armhole (straight)", "22", "23", "24", "25", "0.5"],
        ["G", "Hem width", "49", "52", "55", "58", "1"],
        ["H", "Collar length (button to buttonhole)", "39", "41", "43", "45", "0.5"],
        ["I", "Collar point length", "7", "7", "7", "7", "0.3"],
        ["J", "Placket width", "3", "3", "3", "3", "0.2"],
    ], [1.2*cm, 6.6*cm, 1.6*cm, 1.6*cm, 1.6*cm, 1.6*cm, W-14.2*cm]))
    f.append(Paragraph("Slim fit. Measurements are a starting point; please flag anything that conflicts with your block and adjust after the fit sample.", SM))
    f.append(PageBreak())

    # ---------- SHORTS ----------
    f += [Paragraph("224-SO01 &nbsp;Shorts", H1), header_block("224-SO01", "Shorts, elastic waist"), Spacer(1, 8)]
    pics = Table([[img(SHORTS_IMG, 8*cm), shorts_back()]], colWidths=[W/2, W/2])
    pics.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "MIDDLE"), ("ALIGN", (0, 0), (-1, -1), "CENTER")]))
    f += [pics, Paragraph("Left: front design visual (reference). Right: back view showing embroidery placement.", SM)]

    f.append(Paragraph("Fabric &amp; trims", H2))
    f.append(table([
        ["Component", "Specification", "Notes"],
        ["Main fabric", "Cotton or cotton/elastane, approx. 220-260 GSM (e.g. cotton stretch twill or cotton French terry)", "No polyester. May differ from shirt fabric. TBC"],
        ["Colour", "Burgundy (Pantone 19-1617 TCX or closest) - match shirt", "Lab dip / swatch approval"],
        ["Waistband elastic", "Fully elastic, 4 cm, enclosed in self-fabric waistband", "<b>No drawstring, no tie cord</b>"],
        ["Pocket zips", "2 x gold zips, approx. 15 cm, matching gold puller", "One per side pocket"],
        ["Pocket bags", "Cotton pocketing, burgundy or black", ""],
        ["Sewing thread", "Burgundy, colour-matched", ""],
        ["Embroidery thread", "Gold (metallic or viscose)", "See embroidery spec"],
    ], [3.3*cm, 8.2*cm, W-11.5*cm]))

    f.append(Paragraph("Construction", H2))
    f.append(table([
        ["Area", "Detail"],
        ["Waistband", "4 cm fully elastic waistband, encased, multi-needle stitched to keep elastic flat. No drawstring."],
        ["Pockets", "2 slanted front side pockets with gold zip closure (exposed gold zip tape as in visual)."],
        ["Back", "Plain back, no back pocket."],
        ["Leg", "Slim, above-knee length (approx. 13 cm / 5 in inseam). Hem 2.5 cm double-turned or coverstitch."],
        ["Seams", "Overlocked inside, topstitched side and inseams."],
        ["Embroidery", "\"224 •\" on both sides - see below."],
    ], [3*cm, W-3*cm]))

    f.append(KeepTogether([Paragraph("Embroidery - \"224 •\" both sides", H2), table([
        ["Spec", "Value"],
        ["Text", "224 •"],
        ["Orientation", "Vertical, reading top to bottom"],
        ["Position", "One on each outer leg, on the back panel just behind the side seam (approx. 2 cm), starting 5 cm below waistband - clear of the zip pockets"],
        ["Size", "Letter height approx. 2 cm; total length approx. 8 cm"],
        ["Thread / type", "Gold thread, flat satin stitch"],
    ], [3.5*cm, W-3.5*cm])]))

    f.append(Paragraph("224-SO01 &nbsp;Measurement chart (cm, garment laid flat)", H2))
    f.append(table([
        ["Code", "Point of measure", "S", "M", "L", "XL", "Tol."],
        ["A", "Waist width, relaxed", "36", "38.5", "41", "43.5", "1"],
        ["B", "Waist width, stretched", "50", "53", "56", "59", "1"],
        ["C", "Hip width (8 cm above crotch)", "50", "53", "56", "59", "1"],
        ["D", "Front rise (incl. waistband)", "26", "27", "28", "29", "0.5"],
        ["E", "Back rise (incl. waistband)", "36", "37", "38", "39", "0.5"],
        ["F", "Inseam", "13", "13", "13", "13", "0.5"],
        ["G", "Outseam (incl. waistband)", "42", "43", "44", "45", "1"],
        ["H", "Thigh width (2.5 cm below crotch)", "30", "31.5", "33", "34.5", "0.5"],
        ["I", "Leg opening width", "28", "29.5", "31", "32.5", "0.5"],
        ["J", "Waistband height", "4", "4", "4", "4", "0.2"],
        ["K", "Pocket zip length", "15", "15", "15", "15", "0.5"],
    ], [1.2*cm, 6.6*cm, 1.6*cm, 1.6*cm, 1.6*cm, 1.6*cm, W-14.2*cm]))
    f.append(Paragraph("Slim fit. Measurements are a starting point; please flag anything that conflicts with your block and adjust after the fit sample.", SM))

    f.append(Paragraph("Questions for the factory", H2))
    f.append(table([
        ["#", "Question"],
        ["1", "Which cotton / cotton-elastane fabrics do you have in stock in burgundy (composition, GSM)?"],
        ["2", "Price per piece at 50 pcs per style, including embroidery and labels"],
        ["3", "Sample cost and lead time (1 sample per style, size M)"],
        ["4", "Bulk lead time after sample approval"],
        ["5", "Air freight cost to Jeddah, Saudi Arabia"],
    ], [1*cm, W-1*cm]))

    def footer(c, d):
        c.saveState()
        c.setFont("Helvetica", 7.5)
        c.setFillColor(colors.grey)
        c.drawString(2*cm, 1*cm, "224 - Tech Pack v1 - Confidential")
        c.drawRightString(A4[0]-2*cm, 1*cm, f"Page {d.page}")
        c.restoreState()

    doc.build(f, onFirstPage=footer, onLaterPages=footer)


build()
