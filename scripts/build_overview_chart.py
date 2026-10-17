"""build_overview_chart.py - fill the NIAC 2027 overview chart template.

Usage:
  python build_overview_chart.py --brief BRIEF.md --template TEMPLATE.docx
         [--image IMG] --out OUT.docx

Brief format: lines `KEY: text`. Keys: TITLE, INNOVATION, IMPACT, MISSION,
APPROACH, GRAPHIC_CAPTION. Lines that start with `- ` belong to the last key
as bullets. A missing or empty key prints `MISSING KEY <name>` and exits 2.

Mapping of key to template text box (template: docs/2027_Overview_Chart_Template.docx).
Each box exists twice in document.xml (mc:Choice and its mc:Fallback copy);
both copies are filled. The box is found by the text of its first paragraph.

| Key             | Shape name    | Position on page            | First paragraph  | What is replaced                          |
|-----------------|---------------|-----------------------------|------------------|-------------------------------------------|
| TITLE           | Rectangle 5   | top banner of group         | "Project Title"  | title line; the "(do not include PI)" line is removed |
| INNOVATION      | Text Box 1    | top left (114300, 725029)   | "Innovation"     | paragraphs after the label become bullets |
| IMPACT          | Rectangle 8   | top right of group          | "Impact"         | paragraphs after the label become bullets |
| MISSION         | Rectangle 9   | bottom left of group        | "Mission"        | paragraphs after the label become bullets |
| APPROACH        | Text Box 13   | bottom right (5397500, 3395819) | "Approach"   | paragraphs after the label become bullets |
| GRAPHIC_CAPTION | Text Box 14   | center, over Rectangle 11   | "High resolution graphic" | its text (see below)          |

The label paragraph of the four content boxes stays as in the template.
Bullet paragraphs copy the first instruction paragraph of the box and add
the template's own bullet list (numId 1, level 0).

Image: the one picture is added as a floating drawing (one new run at the end
of the body paragraph, the same pattern as the CLOVER example chart). It is
scaled to fit inside Rectangle 11, the central graphic box, centered, aspect
ratio kept, and drawn above the box and above Text Box 14. With an image,
Text Box 14 text is emptied and GRAPHIC_CAPTION becomes the picture alt text.
Without an image, GRAPHIC_CAPTION fills Text Box 14.

Layout: the four quadrant boxes are moved and resized to tile the 2x2 grid
below the title band (the CLOVER example chart's extents, read from
reference/examples/CLOVER Overview Chart.docx). Positions are page EMU from
the top left of the 9 x 6.5 in text area (inside the 1 in margins):

| Key        | x                  | y       | cx                 | cy      |
|------------|--------------------|---------|--------------------|---------|
| INNOVATION | 114953             | 726295  | to image left      | 2440142 |
| IMPACT     | from image right   | 726295  | to 8177349         | 2440940 |
| MISSION    | 114953             | 3380666 | to image left      | 2508069 |
| APPROACH   | from image right   | 3380666 | to 8177349         | 2508069 |

The y values and heights are CLOVER's. The picture is fitted into the
central graphic box (Rectangle 11, 2467000 x 1707000 EMU) and centered on the
crossing of the two divider lines. It hides whatever lies under it, so the
left boxes end 20000 EMU left of the picture and the right boxes start 20000
EMU right of it.

Only extent and position change (wp:extent, a:ext, a:off, wp:posOffset and
the VML style of the Fallback copy). Impact and Mission are children of the
template group, so their page values are divided by the group scale before
they are written. The image is centered on the crossing of the two divider
lines, at the size of the central graphic box.

Run formatting in every replaced box: Arial, size at least 12 pt (bullets are
set to 12 pt; the template label and title sizes are kept).

Package: every part is copied byte for byte except word/document.xml,
word/_rels/document.xml.rels and [Content_Types].xml (the last two only when
an image is added). Standard library, python-docx and lxml only.
"""
import argparse
import copy
import re
import sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")  # Windows cp1252 consoles
import zipfile

from lxml import etree

NS = {
    "w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main",
    "w14": "http://schemas.microsoft.com/office/word/2010/wordml",
    "wp": "http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing",
    "a": "http://schemas.openxmlformats.org/drawingml/2006/main",
    "pic": "http://schemas.openxmlformats.org/drawingml/2006/picture",
    "r": "http://schemas.openxmlformats.org/officeDocument/2006/relationships",
}
W = "{%s}" % NS["w"]
XML_SPACE = "{http://www.w3.org/XML/1998/namespace}space"

KEYS = ["TITLE", "INNOVATION", "IMPACT", "MISSION", "APPROACH",
        "GRAPHIC_CAPTION"]
BULLET_KEYS = ["INNOVATION", "IMPACT", "MISSION", "APPROACH"]
BODY_HALF_PT = 24  # 12 pt in half points
BULLET_NUM_ID = "1"

# first-paragraph text -> key
BOX_MATCH = [("Project Title", "TITLE"), ("Innovation", "INNOVATION"),
             ("Impact", "IMPACT"), ("Mission", "MISSION"),
             ("Approach", "APPROACH"),
             ("High resolution graphic", "GRAPHIC_CAPTION")]

# Rectangle 11 (central graphic box) in page EMU: group child coordinates
# (off 2505972,2213041 ext 2182484x1575643) scaled by the group transform
# (ext 8229600x5943600 over chExt 7280694x5486400).
GRAPHIC_BOX = (int(2505972 * 8229600 / 7280694.0),
               int(2213041 * 5943600 / 5486400.0),
               int(2182484 * 8229600 / 7280694.0),
               int(1575643 * 5943600 / 5486400.0))


# group transform of the template group (child space to page EMU)
GRP_SX = 8229600 / 7280694.0
GRP_SY = 5943600 / 5486400.0
# divider crossing in page EMU (vertical connector x, horizontal connector y)
CROSS = (int(3640347 * GRP_SX), int(3019245 * GRP_SY))
GAP = 20000
LEFT_X, RIGHT_END = 114953, 8177349
ROWS = {"INNOVATION": (726295, 2440142), "IMPACT": (726295, 2440940),
        "MISSION": (3380666, 2508069), "APPROACH": (3380666, 2508069)}


def quadrants(img_w):
    """Page-EMU (x, y, cx, cy) per quadrant key, given the picture width."""
    left_end = CROSS[0] - img_w // 2 - GAP
    right_start = CROSS[0] + img_w // 2 + GAP
    out = {}
    for k, (y, h) in ROWS.items():
        if k in ("INNOVATION", "MISSION"):
            out[k] = (LEFT_X, y, left_end - LEFT_X, h)
        else:
            out[k] = (right_start, y, RIGHT_END - right_start, h)
    return out


def set_style(el, vals):
    """Set CSS keys in a VML style attribute."""
    st = el.get("style", "")
    for k, v in vals.items():
        if re.search(r"(^|;)%s:" % re.escape(k), st):
            st = re.sub(r"(^|;)(%s:)[^;]*" % re.escape(k),
                        lambda m: m.group(1) + m.group(2) + v, st)
        else:
            st += ";%s:%s" % (k, v)
    el.set("style", st)


def ancestor(el, local):
    for a in el.iterancestors():
        if etree.QName(a).localname == local:
            return a
    return None


def place_box(box, geom):
    """Move and resize the shape that holds txbxContent `box` to page EMU
    geom=(x, y, cx, cy). Handles the DrawingML (Choice) and VML (Fallback)
    copies, anchored text boxes and group children."""
    x, y, cx, cy = geom
    nsw = NS["wp"]
    anchor = ancestor(box, "anchor")
    wsp = ancestor(box, "wsp")
    if anchor is not None and ancestor(box, "wgp") is None:
        for tag, v in (("positionH", x), ("positionV", y)):
            anchor.find("{%s}%s/{%s}posOffset" % (nsw, tag, nsw)).text = str(v)
        e = anchor.find("{%s}extent" % nsw)
        e.set("cx", str(cx))
        e.set("cy", str(cy))
        ext = wsp.find("{*}spPr/{%s}xfrm/{%s}ext" % (NS["a"], NS["a"]))
        ext.set("cx", str(cx))
        ext.set("cy", str(cy))
        return
    if wsp is not None:  # group child: write child coordinates
        off = wsp.find("{*}spPr/{%s}xfrm/{%s}off" % (NS["a"], NS["a"]))
        ext = wsp.find("{*}spPr/{%s}xfrm/{%s}ext" % (NS["a"], NS["a"]))
        off.set("x", str(int(x / GRP_SX)))
        off.set("y", str(int(y / GRP_SY)))
        ext.set("cx", str(int(cx / GRP_SX)))
        ext.set("cy", str(int(cy / GRP_SY)))
        return
    vml = ancestor(box, "shape")
    if vml is None:
        vml = ancestor(box, "rect")
    grp = ancestor(box, "group")
    if grp is not None:  # VML group child, units are child EMU / 100
        set_style(vml, {"left": str(int(x / GRP_SX / 100)),
                        "top": str(int(y / GRP_SY / 100)),
                        "width": str(int(cx / GRP_SX / 100)),
                        "height": str(int(cy / GRP_SY / 100))})
    else:
        set_style(vml, {"margin-left": "%.1fpt" % (x / 12700.0),
                        "margin-top": "%.1fpt" % (y / 12700.0),
                        "width": "%.1fpt" % (cx / 12700.0),
                        "height": "%.1fpt" % (cy / 12700.0)})


def parse_brief(path):
    vals = {k: {"text": "", "bullets": []} for k in KEYS}
    seen = set()
    last = None
    for raw in open(path, encoding="utf-8").read().splitlines():
        line = raw.rstrip()
        m = re.match(r"^([A-Z_]+):[ \t]*(.*)$", line)
        if m and m.group(1) in KEYS:
            last = m.group(1)
            seen.add(last)
            vals[last]["text"] = m.group(2).strip()
            continue
        if last and re.match(r"^-[ \t]", line + " "):
            b = line[1:].strip()
            if b:
                vals[last]["bullets"].append(b)
    for k in KEYS:
        v = vals[k]
        if k not in seen or not (v["text"] or v["bullets"]):
            print("MISSING KEY %s" % k)
            sys.exit(2)
    return vals


def para_text(p):
    return "".join(t.text or "" for t in p.iter(W + "t"))


def set_run_text(r, text):
    for c in list(r):
        if c.tag != W + "rPr":
            r.remove(c)
    t = etree.SubElement(r, W + "t")
    t.text = text
    if text != text.strip() or "  " in text:
        t.set(XML_SPACE, "preserve")


def set_para_text(p, text):
    """Keep the first run (and its rPr), drop the other runs, set the text."""
    runs = p.findall(W + "r")
    if not runs:
        r = etree.SubElement(p, W + "r")
        ppr = p.find(W + "pPr")
        if ppr is not None and ppr.find(W + "rPr") is not None:
            r.insert(0, copy.deepcopy(ppr.find(W + "rPr")))
        runs = [r]
    for extra in runs[1:]:
        p.remove(extra)
    set_run_text(runs[0], text)


def set_size(p, half_pts):
    """Set sz and szCs on every run rPr and on the paragraph mark rPr."""
    rprs = [r.find(W + "rPr") for r in p.findall(W + "r")]
    ppr = p.find(W + "pPr")
    if ppr is not None:
        rprs.append(ppr.find(W + "rPr"))
    for rpr in rprs:
        if rpr is None:
            continue
        for tag in ("sz", "szCs"):
            el = rpr.find(W + tag)
            if el is not None:
                el.set(W + "val", str(half_pts))


def strip_ids(p):
    for att in list(p.attrib):
        if att.startswith("{%s}" % NS["w14"]) and att.endswith(
                ("paraId", "textId")):
            del p.attrib[att]


def make_bullet(proto, text):
    p = copy.deepcopy(proto)
    strip_ids(p)
    set_para_text(p, text)
    set_size(p, BODY_HALF_PT)
    ppr = p.find(W + "pPr")
    if ppr is None:
        ppr = etree.Element(W + "pPr")
        p.insert(0, ppr)
    for old in ppr.findall(W + "numPr") + ppr.findall(W + "ind"):
        ppr.remove(old)
    numpr = etree.Element(W + "numPr")
    etree.SubElement(numpr, W + "ilvl").set(W + "val", "0")
    etree.SubElement(numpr, W + "numId").set(W + "val", BULLET_NUM_ID)
    ind = etree.Element(W + "ind")
    ind.set(W + "left", "288")
    ind.set(W + "hanging", "288")
    # schema order: pStyle, ..., numPr, ..., spacing, ind, ..., jc, ..., rPr
    pos = 0
    for i, c in enumerate(ppr):
        if c.tag == W + "pStyle":
            pos = i + 1
    ppr.insert(pos, numpr)
    after = pos + 1
    for i, c in enumerate(ppr):
        if c.tag == W + "spacing":
            after = i + 1
    ppr.insert(after, ind)
    return p


def plain_para(proto, text):
    p = copy.deepcopy(proto)
    strip_ids(p)
    set_para_text(p, text)
    set_size(p, BODY_HALF_PT)
    return p


def fix_rpr(rpr):
    rf = rpr.find(W + "rFonts")
    if rf is None:
        rf = etree.Element(W + "rFonts")
        rpr.insert(0, rf)
    for att in ("ascii", "hAnsi", "cs"):
        rf.set(W + att, "Arial")
    for tag in ("sz", "szCs"):
        el = rpr.find(W + tag)
        if el is None:
            el = etree.SubElement(rpr, W + tag)
            el.set(W + "val", str(BODY_HALF_PT))
        elif int(el.get(W + "val")) < BODY_HALF_PT:
            el.set(W + "val", str(BODY_HALF_PT))
    # keep schema order for sz/szCs relative to rFonts-led block: move to end
    for tag in ("sz", "szCs"):
        el = rpr.find(W + tag)
        rpr.remove(el)
        rpr.append(el)


def enforce_arial12(box):
    for r in box.iter(W + "r"):
        rpr = r.find(W + "rPr")
        if rpr is None:
            rpr = etree.Element(W + "rPr")
            r.insert(0, rpr)
        fix_rpr(rpr)
    for rpr in box.iter(W + "rPr"):
        if rpr.getparent().tag == W + "pPr":
            fix_rpr(rpr)


def fill_box(box, key, val, has_image):
    paras = box.findall(W + "p")
    if key == "TITLE":
        set_para_text(paras[0], val["text"] or " ".join(val["bullets"]))
        for p in paras[1:]:
            box.remove(p)
    elif key == "GRAPHIC_CAPTION":
        cap = val["text"] or " ".join(val["bullets"])
        set_para_text(paras[0], "" if has_image else cap)
    else:
        proto = paras[1] if len(paras) > 1 else paras[0]
        keep = paras[0]
        new = []
        if val["text"]:
            new.append(plain_para(proto, val["text"]))
        for b in val["bullets"]:
            new.append(make_bullet(proto, b))
        for p in paras[1:]:
            box.remove(p)
        at = list(box).index(keep) + 1
        for i, p in enumerate(new):
            box.insert(at + i, p)
    enforce_arial12(box)


def find_boxes(root):
    found = {k: [] for k in KEYS}
    for box in root.iter(W + "txbxContent"):
        p0 = box.find(W + "p")
        if p0 is None:
            continue
        text = para_text(p0).strip()
        for start, key in BOX_MATCH:
            if text == start or (key in ("TITLE", "GRAPHIC_CAPTION")
                                 and text.startswith(start)):
                found[key].append(box)
                break
    return found


def next_rid(rels_root):
    ids = [int(re.sub(r"\D", "", e.get("Id")) or 0) for e in rels_root]
    return "rId%d" % (max(ids + [0]) + 1)


def anchor_xml(rid, cx, cy, ox, oy, rel_h, docpr_id, name, descr):
    return (
        '<w:r xmlns:w="%(w)s" xmlns:wp="%(wp)s" xmlns:a="%(a)s" '
        'xmlns:pic="%(pic)s" xmlns:r="%(r)s"><w:drawing>'
        '<wp:anchor distT="0" distB="0" distL="0" distR="0" simplePos="0" '
        'relativeHeight="%(rh)d" behindDoc="0" locked="0" layoutInCell="1" '
        'allowOverlap="1"><wp:simplePos x="0" y="0"/>'
        '<wp:positionH relativeFrom="column"><wp:posOffset>%(ox)d'
        '</wp:posOffset></wp:positionH>'
        '<wp:positionV relativeFrom="paragraph"><wp:posOffset>%(oy)d'
        '</wp:posOffset></wp:positionV>'
        '<wp:extent cx="%(cx)d" cy="%(cy)d"/>'
        '<wp:effectExtent l="0" t="0" r="0" b="0"/><wp:wrapNone/>'
        '<wp:docPr id="%(id)d" name="Picture %(id)d" descr="%(descr)s"/>'
        '<wp:cNvGraphicFramePr><a:graphicFrameLocks noChangeAspect="1"/>'
        '</wp:cNvGraphicFramePr>'
        '<a:graphic><a:graphicData uri="%(pic)s"><pic:pic>'
        '<pic:nvPicPr><pic:cNvPr id="0" name="%(name)s" descr="%(descr)s"/>'
        '<pic:cNvPicPr/></pic:nvPicPr>'
        '<pic:blipFill><a:blip r:embed="%(rid)s"/><a:stretch><a:fillRect/>'
        '</a:stretch></pic:blipFill>'
        '<pic:spPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="%(cx)d" '
        'cy="%(cy)d"/></a:xfrm><a:prstGeom prst="rect"><a:avLst/>'
        '</a:prstGeom></pic:spPr></pic:pic></a:graphicData></a:graphic>'
        '</wp:anchor></w:drawing></w:r>'
        % dict(w=NS["w"], wp=NS["wp"], a=NS["a"], pic=NS["pic"], r=NS["r"],
               rh=rel_h, ox=ox, oy=oy, cx=cx, cy=cy, id=docpr_id,
               name=name, descr=descr, rid=rid))


def xml_attr(s):
    return (s.replace("&", "&amp;").replace("<", "&lt;")
            .replace(">", "&gt;").replace('"', "&quot;"))


def serialize(root):
    return etree.tostring(root, xml_declaration=True, encoding="UTF-8",
                          standalone=True)


def clear_graphic_fill(root):
    """With an image placed, Rectangle 11 (the placeholder rectangle) gets no
    fill and no line, so no template color shows around the picture. Both
    copies are changed: wps shape (mc:Choice) and v:rect (mc:Fallback)."""
    A = "{%s}" % NS["a"]
    WPS = "{http://schemas.microsoft.com/office/word/2010/wordprocessingShape}"
    V = "{urn:schemas-microsoft-com:vml}"
    for wsp in root.iter(WPS + "wsp"):
        nv = wsp.find(WPS + "cNvPr")
        if nv is None or nv.get("name") != "Rectangle 11":
            continue
        sp = wsp.find(WPS + "spPr")
        for kids, parent in ((sp, sp), (sp.find(A + "ln"), sp.find(A + "ln"))):
            if parent is None:
                continue
            for c in list(parent):
                if c.tag in (A + "solidFill", A + "noFill", A + "gradFill"):
                    parent.remove(c)
        fill = etree.Element(A + "noFill")
        ln = sp.find(A + "ln")
        geom = sp.find(A + "prstGeom")
        geom.addnext(fill)
        if ln is None:
            ln = etree.Element(A + "ln")
            fill.addnext(ln)
        ln.insert(0, etree.Element(A + "noFill"))
    for rect in root.iter(V + "rect"):
        if rect.get("id") == "Rectangle 11":
            for k in ("fillcolor", "strokecolor"):
                rect.attrib.pop(k, None)
            rect.set("filled", "f")
            rect.set("stroked", "f")


def build(brief, template, image, out):
    vals = parse_brief(brief)
    zin = zipfile.ZipFile(template)
    root = etree.fromstring(zin.read("word/document.xml"))
    found = find_boxes(root)
    for k in KEYS:
        if not found[k]:
            print("TEMPLATE BOX NOT FOUND %s" % k)
            return 3
    img_w = GRAPHIC_BOX[2]
    img = None
    if image:
        from docx.image.image import Image
        blob = open(image, "rb").read()
        img = Image.from_blob(blob)
        bw, bh = GRAPHIC_BOX[2], GRAPHIC_BOX[3]
        img_w = int(img.px_width * min(bw / float(img.px_width),
                                       bh / float(img.px_height)))
    quad = quadrants(img_w)
    for k in KEYS:
        for box in found[k]:
            fill_box(box, k, vals[k], bool(image))
            if k in quad:
                place_box(box, quad[k])

    extra = {}
    rels_bytes = ctypes_bytes = None
    if image:
        ext = img.ext.lower().lstrip(".")
        if ext == "jpeg":
            ext = "jpg"
        media = "word/media/image1.%s" % ext
        bx, by, bw, bh = GRAPHIC_BOX
        scale = min(bw / float(img.px_width), bh / float(img.px_height))
        cx, cy = int(img.px_width * scale), int(img.px_height * scale)
        ox, oy = CROSS[0] - cx // 2, CROSS[1] - cy // 2
        rels = etree.fromstring(zin.read("word/_rels/document.xml.rels"))
        rid = next_rid(rels)
        rel = etree.SubElement(rels, "{%s}Relationship" % rels.nsmap[None])
        rel.set("Id", rid)
        rel.set("Type", NS["r"] + "/image")
        rel.set("Target", "media/image1.%s" % ext)
        rels_bytes = serialize(rels)
        ct = etree.fromstring(zin.read("[Content_Types].xml"))
        ctns = "{%s}" % ct.nsmap[None]
        if not any(d.get("Extension", "").lower() == ext
                   for d in ct.findall(ctns + "Default")):
            d = etree.Element(ctns + "Default")
            d.set("Extension", ext)
            d.set("ContentType", img.content_type)
            ct.insert(0, d)
        ctypes_bytes = serialize(ct)
        ids = [int(e.get("id")) for e in root.iter("{%s}docPr" % NS["wp"])]
        rel_h = max([int(e.get("relativeHeight", "0"))
                     for e in root.iter("{%s}anchor" % NS["wp"])] + [0]) + 1024
        run = etree.fromstring(anchor_xml(
            rid, cx, cy, ox, oy, rel_h, max(ids + [0]) + 1, "image1." + ext,
            xml_attr(vals["GRAPHIC_CAPTION"]["text"]
                     or " ".join(vals["GRAPHIC_CAPTION"]["bullets"]))))
        body_p = root.find(W + "body").find(W + "p")
        body_p.append(run)
        clear_graphic_fill(root)
        extra[media] = blob

    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as zout:
        for info in zin.infolist():
            data = zin.read(info.filename)
            if info.filename == "word/document.xml":
                data = serialize(root)
            elif info.filename == "word/_rels/document.xml.rels" and rels_bytes:
                data = rels_bytes
            elif info.filename == "[Content_Types].xml" and ctypes_bytes:
                data = ctypes_bytes
            zout.writestr(info, data)
        for name, data in extra.items():
            zout.writestr(name, data)
    print("WROTE %s" % out)
    return 0


def main(argv):
    ap = argparse.ArgumentParser(
        description="Fill the NIAC 2027 overview chart template from a brief "
                    "of KEY: text lines (TITLE, INNOVATION, IMPACT, MISSION, "
                    "APPROACH, GRAPHIC_CAPTION). Replaces only the text of "
                    "the template boxes, sets Arial at least 12 pt, and "
                    "places one image in the central graphic box. Missing "
                    "key: prints MISSING KEY <name>, exit 2.")
    ap.add_argument("--brief", required=True, help="brief .md file")
    ap.add_argument("--template", required=True, help="template .docx")
    ap.add_argument("--image", help="central graphic (png or jpg)")
    ap.add_argument("--out", required=True, help="output .docx")
    a = ap.parse_args(argv[1:])
    return build(a.brief, a.template, a.image, a.out)


if __name__ == "__main__":
    sys.exit(main(sys.argv))
