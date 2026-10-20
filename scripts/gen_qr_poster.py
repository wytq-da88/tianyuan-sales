#!/usr/bin/env python3
# 生成农哈哈田园部（喷灌机）宣传物料：
# 1) site.png      —— 二维码 + 农哈哈 logo 居中
# 2) site_nologo.png —— 纯二维码
# 3) poster.png    —— 横版卡片 2000×880（画册风格，A4 可印）
# 4) banner.png    —— 竖版易拉宝 80×200cm，100 DPI（3150×7874）
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "public" / "qr"
OUT.mkdir(parents=True, exist_ok=True)

URL = "https://wytq-da88.github.io/tianyuan-sales/"
LOGO = ROOT / "public" / "logo.png"

NAME = "河北农哈哈机械集团 · 田园部"
COLOR = (26, 110, 200)        # 农哈哈蓝
LIGHT = (214, 231, 243)
DARK = (26, 42, 58)
GREY = (120, 138, 152)
HEADLINE = ["买 喷灌机", "田园部销售通讯录"]
TAGLINE = "扫一扫 · 查您所在区域的业务员"
INFO = [
    ("销售热线", "0311-87513850"),
    ("地址", "河北省石家庄市深泽县北环路222号"),
    ("网址", "www.nonghaha.com"),
]
SITE_LABEL = "www.nonghaha.com"


def font(size, bold=False):
    from PIL import ImageFont
    for p in ([r"C:\Windows\Fonts\msyhbd.ttc", r"C:\Windows\Fonts\simhei.ttf"]
              if bold else [r"C:\Windows\Fonts\msyh.ttc", r"C:\Windows\Fonts\simhei.ttf"]):
        try:
            return ImageFont.truetype(p, size)
        except OSError:
            continue
    return ImageFont.load_default()


def make_qr(fill="#16243a"):
    import qrcode
    from qrcode.constants import ERROR_CORRECT_H
    qr = qrcode.QRCode(version=None, error_correction=ERROR_CORRECT_H,
                       box_size=18, border=4)
    qr.add_data(URL)
    qr.make(fit=True)
    return qr.make_image(fill_color=fill, back_color="white").convert("RGB")


def load_logo_rgba():
    from PIL import Image
    logo = Image.open(LOGO).convert("RGBA")
    # 白底抠透明（纯白 248+ 视为背景），让 logo 在蓝底上也干净
    px = logo.load()
    w, h = logo.size
    for y in range(h):
        for x in range(w):
            r, g, b, a = px[x, y]
            if min(r, g, b) > 248:
                px[x, y] = (r, g, b, 0)
    return logo


def embed_logo(img, ratio=0.20):
    from PIL import Image
    logo = load_logo_rgba()
    bbox = logo.getbbox()
    if bbox:
        logo = logo.crop(bbox)
    lw = int(img.size[0] * ratio)
    logo = logo.resize((lw, lw), Image.LANCZOS)
    pad = int(lw * 0.10)
    tray = Image.new("RGBA", (lw + pad * 2, lw + pad * 2), (255, 255, 255, 255))
    tray.paste(logo, (pad, pad), logo)
    pos = ((img.size[0] - tray.size[0]) // 2, (img.size[1] - tray.size[1]) // 2)
    img.paste(tray, pos, tray)
    return img


def text_w(d, s, f):
    b = d.textbbox((0, 0), s, font=f)
    return b[2] - b[0]


def make_poster():
    from PIL import Image, ImageDraw
    W, H = 2000, 880
    card = Image.new("RGB", (W, H), (255, 255, 255))
    d = ImageDraw.Draw(card)
    qr = embed_logo(make_qr())
    qr = qr.resize((640, 640), Image.LANCZOS)
    pad = 36
    block = Image.new("RGB", (qr.size[0] + pad * 2, qr.size[1] + pad * 2), (255, 255, 255))
    block.paste(qr, (pad, pad))
    qx = 190
    qy = (H - block.size[1]) // 2
    card.paste(block, (qx, qy))
    d.rectangle([qx - 2, qy - 2, qx + block.size[0] + 1, qy + block.size[1] + 1],
                outline=(223, 230, 236), width=2)
    d.rectangle([0, 0, 110, H], fill=COLOR)
    d.rectangle([110, 0, 118, H], fill=LIGHT)

    tx = qx + block.size[0] + 110
    f_company = font(58, bold=True)
    f_line = font(40)
    f_tag = font(34)
    y = 190
    d.text((tx, y), NAME, fill=DARK, font=f_company)
    y += 100
    d.line([tx, y, tx + 880, y], fill=COLOR, width=3)
    y += 52
    for k, v in INFO:
        d.text((tx, y), f"{k}：", fill=COLOR, font=f_line)
        d.text((tx + 240, y), v, fill=DARK, font=f_line)
        y += 88
    y += 56
    d.text((tx, y), TAGLINE, fill=GREY, font=f_tag)
    d.rectangle([0, H - 90, W, H], fill=(240, 246, 250))
    d.text((W // 2 - 220, H - 74), SITE_LABEL, fill=COLOR, font=font(36))
    out = OUT / "poster.png"
    card.save(out)
    print("saved:", out, card.size)


def make_banner():
    from PIL import Image, ImageDraw
    W, H = 3150, 7874
    c = COLOR
    img = Image.new("RGB", (W, H), (255, 255, 255))
    d = ImageDraw.Draw(img)

    top_h = 1750
    d.rectangle([0, 0, W, top_h], fill=c)
    d.rectangle([0, top_h, W, top_h + 26], fill=LIGHT)

    logo = load_logo_rgba()
    bbox = logo.getbbox()
    if bbox:
        logo = logo.crop(bbox)
    ls = 620
    logo = logo.resize((ls, ls), Image.LANCZOS)
    tray = Image.new("RGBA", (ls + 60, ls + 60), (255, 255, 255, 255))
    tray.paste(logo, (30, 30), logo)
    img.paste(tray, ((W - tray.size[0]) // 2, 180), tray)

    f_name = font(96, bold=True)
    y = 180 + tray.size[1] + 60
    d.text(((W - text_w(d, NAME, f_name)) // 2, y), NAME,
           fill=(255, 255, 255), font=f_name)

    y = top_h + 220
    f_head = font(200, bold=True)
    for line in HEADLINE:
        d.text(((W - text_w(d, line, f_head)) // 2, y), line, fill=DARK, font=f_head)
        y += 280
    y += 30
    f_sub = font(78)
    d.text(((W - text_w(d, TAGLINE, f_sub)) // 2, y), TAGLINE, fill=GREY, font=f_sub)
    sub_bottom = y + 100

    # ---- 二维码（在副标题与底部信息区之间垂直居中）----
    qr = embed_logo(make_qr(), ratio=0.22)
    qs = 1700
    qr = qr.resize((qs, qs), Image.LANCZOS)
    qx = (W - qs) // 2
    foot_h = 320
    n = len(INFO)
    divider_y = H - foot_h - 220 - n * 130 - 80
    qy = sub_bottom + (divider_y - sub_bottom - qs) // 2
    d.rounded_rectangle([qx - 50, qy - 50, qx + qs + 49, qy + qs + 49],
                        radius=40, fill=(244, 248, 251))
    d.rounded_rectangle([qx - 36, qy - 36, qx + qs + 35, qy + qs + 35],
                        radius=30, fill=(255, 255, 255), outline=(223, 230, 236), width=4)
    img.paste(qr, (qx, qy))

    y = divider_y + 80
    d.line([W // 2 - 500, y - 80, W // 2 + 500, y - 80], fill=LIGHT, width=8)
    f_k = font(72, bold=True)
    f_v = font(72)
    for k, v in INFO:
        d.text((W // 2 - 640, y), f"{k}：", fill=c, font=f_k)
        d.text((W // 2 - 100, y), v, fill=DARK, font=f_v)
        y += 130

    d.rectangle([0, H - foot_h, W, H], fill=c)
    f_foot = font(84, bold=True)
    d.text(((W - text_w(d, SITE_LABEL, f_foot)) // 2, H - foot_h + 100),
           SITE_LABEL, fill=(255, 255, 255), font=f_foot)

    out = OUT / "banner.png"
    img.save(out, dpi=(100, 100))
    print("saved:", out, img.size, "-> 80x200cm @100dpi")


if __name__ == "__main__":
    site = embed_logo(make_qr())
    site.save(OUT / "site.png")
    print("saved:", OUT / "site.png", site.size)
    plain = make_qr()
    plain.save(OUT / "site_nologo.png")
    print("saved:", OUT / "site_nologo.png", plain.size)
    make_poster()
    make_banner()
