#!/usr/bin/env python3
"""Compose the news-image-02 front page: 26 stories, classic newspaper layout.
All text rendered with real fonts (DejaVu) -- zero AI-generated text.
Illustrations: 4 flat-cartoon panels generated with media.generate_image.
"""
from PIL import Image, ImageDraw, ImageFont
import textwrap, os

W, H = 1024, 1024
CREAM = (247, 242, 227)
INK = (20, 20, 20)
RED = (176, 32, 32)
GRAY = (70, 70, 70)
RULE = (40, 40, 40)

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF_R = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SANS_R = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

def font(path, size):
    return ImageFont.truetype(path, size)

def wrap(draw, text, fnt, max_w):
    """Greedy word wrap to max width in px; returns list of lines."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if draw.textlength(t, font=fnt) <= max_w:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines

def draw_lines(draw, lines, x, y, fnt, fill, lh):
    for ln in lines:
        draw.text((x, y), ln, font=fnt, fill=fill)
        y += lh
    return y

def cover_crop(im, tw, th):
    """Center-crop to target aspect, then resize (no distortion)."""
    w, h = im.size
    ta, sa = tw / th, w / h
    if sa > ta:  # too wide -> crop sides
        nw = int(h * ta)
        x0 = (w - nw) // 2
        im = im.crop((x0, 0, x0 + nw, h))
    else:        # too tall -> crop top/bottom
        nh = int(w / ta)
        y0 = (h - nh) // 2
        im = im.crop((0, y0, w, y0 + nh))
    return im.resize((tw, th), Image.LANCZOS)

SRC = os.path.dirname(os.path.abspath(__file__))
img = Image.new("RGB", (W, H), CREAM)
d = ImageDraw.Draw(img)
MX = 22  # side margin

# ---------- masthead ----------
f_mast = font(SERIF, 47)
mast = "FRIDAY 13 NOVEMBER 2026"
mw = d.textlength(mast, font=f_mast)
d.text(((W - mw) / 2, 16), mast, font=f_mast, fill=INK)
f_sub = font(SANS, 15)
sub = "THE WORLD'S NEWS IN ONE PICTURE"
sw = d.textlength(sub, font=f_sub)
d.text(((W - sw) / 2, 72), sub, font=f_sub, fill=RED)
d.line([(MX, 100), (W - MX, 100)], fill=RULE, width=2)
d.line([(MX, 104), (W - MX, 104)], fill=RULE, width=1)

# ---------- lead stories (3 large) ----------
leads = [
    dict(label="AMERICA", head="FAA HALTS ALL US DEPARTURES",
         sub="Telecom failure grounds flights for hours; thousands delayed.",
         pic="media-generation-news2-faa-0-beaabdc9-0697-4c1b-9d5b-25ca817fd05c.webp"),
    dict(label="MIDDLE EAST", head="IRAN SAYS IT HIT US RADAR",
         sub="Tehran claims a strike in Bahrain; US denies it, says it downed two drones.",
         pic="media-generation-news2-iran-0-fca3af03-662f-44e3-952c-f12a0b460805.webp"),
    dict(label="DIPLOMACY", head="TRUMP, XI AND PUTIN TO MEET",
         sub="First three-way summit set for Shenzhen; nuclear arms on the agenda.",
         pic="media-generation-news2-summit-0-2787c522-72f2-4198-aee7-dc10a02bc063.webp"),
]
lead_y = 116
lead_h = 285
col_w = (W - 2 * MX - 2 * 10) // 3  # 3 cols, 10px gutters
f_lab = font(SANS, 12)
f_head = font(SERIF, 19)
f_sub2 = font(SANS_R, 12)
for i, L in enumerate(leads):
    x = MX + i * (col_w + 10)
    # red category label
    d.text((x, lead_y), L["label"], font=f_lab, fill=RED)
    # headline (2 lines)
    hl = wrap(d, L["head"], f_head, col_w)
    y = draw_lines(d, hl, x, lead_y + 18, f_head, INK, 23)
    # illustration
    pic = Image.open(os.path.join(SRC, L["pic"])).convert("RGB")
    pic = cover_crop(pic, col_w, 148)
    img.paste(pic, (x, y + 4))
    # sub (2 lines)
    sl = wrap(d, L["sub"], f_sub2, col_w)
    draw_lines(d, sl, x, y + 4 + 148 + 6, f_sub2, GRAY, 15)

d.line([(MX, lead_y + lead_h), (W - MX, lead_y + lead_h)], fill=RULE, width=1)

# ---------- medium row (4 stories) ----------
med_y = lead_y + lead_h + 10
med_h = 165
med_w = (W - 2 * MX - 3 * 10) // 4
meds = [
    dict(label="SPACE", head="STARSHIP REACHES ORBIT",
         sub="Flight 15 deploys 26 satellites; booster splashes down in the Gulf.",
         pic="media-generation-news2-starship-0-bc254351-9871-4691-bd36-2c7346d87cc6.webp"),
    dict(label="TECH", head="MICROSOFT 365 DOWN, DAY 2",
         sub="Outlook, Teams and Copilot offline in dozens of countries."),
    dict(label="WAR", head="UKRAINE FIRES ~1,200 DRONES",
         sub="One of the war's biggest air attacks; a Kyiv hospital is hit."),
    dict(label="BUSINESS", head="NVIDIA CHIEF QUITS",
         sub="Jensen Huang resigns; Senate summons him to testify."),
]
f_mhead = font(SERIF, 15)
f_msub = font(SANS_R, 11)
for i, M in enumerate(meds):
    x = MX + i * (med_w + 10)
    d.text((x, med_y), M["label"], font=f_lab, fill=RED)
    hl = wrap(d, M["head"], f_mhead, med_w)
    y = draw_lines(d, hl, x, med_y + 17, f_mhead, INK, 18)
    if "pic" in M:
        pic = Image.open(os.path.join(SRC, M["pic"])).convert("RGB")
        pic = cover_crop(pic, med_w, 64)
        img.paste(pic, (x, y + 3))
        sl = wrap(d, M["sub"], f_msub, med_w)
        draw_lines(d, sl, x, y + 3 + 64 + 4, f_msub, GRAY, 14)
    else:
        sl = wrap(d, M["sub"], f_msub, med_w)
        draw_lines(d, sl, x, y + 3, f_msub, GRAY, 14)

d.line([(MX, med_y + med_h), (W - MX, med_y + med_h)], fill=RULE, width=1)

# ---------- foot strip: ALSO ON FRIDAY 13 NOVEMBER ----------
foot_y = med_y + med_h + 8
band_h = 30
d.rectangle([(MX, foot_y), (W - MX, foot_y + band_h)], fill=RED)
f_band = font(SANS, 16)
band = "ALSO ON FRIDAY 13 NOVEMBER"
bw = d.textlength(band, font=f_band)
d.text(((W - bw) / 2, foot_y + 6), band, font=f_band, fill=(255, 255, 255))

foot_items = [
    "China massed 100+ ships in Pacific drills, Taiwan says",
    "Pope Leo XIV draws 500,000 to Mass in Chiclayo, Peru",
    "Türkiye and Qatar sign defence pact",
    "Two tankers hit mines in the Strait of Hormuz, Iran says",
    "Ethiopian forces take Mekelle",
    "UN extends Abyei peacekeeping mandate",
    "Drones spotted over RAF Lakenheath, UK",
    "Nigeria ends its Ebola watch",
    "COP31: UN chief urges drastic emissions cuts",
    "Tanker hits docked cruise ship in New Orleans",
    "Pochettino leaves USMNT to manage Man Utd",
    "Car bomb kills a Russian air force colonel",
    "Japan PM Takaichi visits China",
    "US wholesale prices rise",
    "Yen passes 160 to the dollar",
    "Bus crash in Assam kills 24",
    "Fallout grows from Israel's strike on Gaza hospital",
    "Europe joins the Ukraine peace talks",
    "Japan beats South Korea 9–5 in baseball",
]
f_num = font(SANS, 13)
f_item = font(SANS, 12)
cols = 3
per_col = (len(foot_items) + cols - 1) // cols  # 7
col_w2 = (W - 2 * MX - 2 * 14) // 3
item_h = 50
list_y = foot_y + band_h + 6
for ci in range(cols):
    x = MX + ci * (col_w2 + 14)
    for ri in range(per_col):
        idx = ci * per_col + ri
        if idx >= len(foot_items):
            break
        y = list_y + ri * item_h
        num = f"{idx + 8}."
        d.text((x, y), num, font=f_num, fill=RED)
        nw = d.textlength(num + " ", font=f_num)
        lines = wrap(d, foot_items[idx], f_item, col_w2 - nw)
        draw_lines(d, lines[:2], x + nw, y + 1, f_item, INK, 15)

# ---------- sources footer ----------
f_src = font(SANS_R, 11)
src = "Sources: AP · Reuters · BBC · Al Jazeera · CNN · Vatican News · Space.com"
sw2 = d.textlength(src, font=f_src)
d.text(((W - sw2) / 2, H - 26), src, font=f_src, fill=GRAY)

out = os.path.join(SRC, "entry.png")
img.save(out, "JPEG", quality=92)
print("saved", out, img.size, os.path.getsize(out), "bytes")
