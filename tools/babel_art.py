"""Bilder für B.A.B.E.L.: Logos der fünf Spiele, ein Gruppenbild aller Roboter und ein Bild mit den Störungen aus dem Schacht.

Wird von make_babel.py aufgerufen. Pixelgrafik: klein gezeichnet und ohne Glättung vergrößert, wie in den Spielen.
Die vorhandenen Logos (Bits & Bolts, Bots & Buddies, Lines & Loads) kommen aus icons/ bzw. dem Spielordner daneben,
die zwei Konzepte bekommen hier ein eigenes im selben Stil.
"""
import os
import random
import shutil

from PIL import Image, ImageDraw

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
IMG = os.path.join(OUT, "babel", "img")
BG = (7, 11, 8, 255)
PANEL = (12, 20, 14, 255)


def _hex(c, a=255):
    c = c.lstrip("#")
    return (int(c[0:2], 16), int(c[2:4], 16), int(c[4:6], 16), a)


def _frame(col):
    """48×48 Kachel wie bei den anderen Logos: dunkle Fläche, Rahmen in der Akzentfarbe."""
    im = Image.new("RGBA", (48, 48), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle((0, 0, 47, 47), radius=8, fill=BG)
    d.rounded_rectangle((2, 2, 45, 45), radius=7, fill=PANEL, outline=_hex(col), width=2)
    return im, d


def _amps():
    im, d = _frame("#FF5252")
    # Blitz mit hellem Kern
    bolt = [(27, 7), (13, 26), (22, 26), (18, 41), (35, 20), (26, 20), (31, 7)]
    d.polygon(bolt, fill=_hex("#FF5252"))
    inner = [(27, 10), (17, 24), (25, 24), (22, 35), (31, 22), (23, 22), (28, 10)]
    d.polygon(inner, fill=_hex("#FFE9E0"))
    # Funken
    for x, y in [(10, 12), (37, 10), (39, 32), (9, 34), (34, 38), (12, 21)]:
        d.rectangle((x, y, x + 1, y + 1), fill=_hex("#FFB000"))
    return im


def _echoes():
    im, d = _frame("#FF5CF0")
    pink = _hex("#FF5CF0")
    # Lautsprecher mit Schallwellen
    d.rectangle((9, 19, 15, 29), fill=pink)
    d.polygon([(15, 19), (23, 12), (23, 36), (15, 29)], fill=pink)
    d.rectangle((11, 21, 13, 27), fill=_hex("#FFD6FA"))
    for k, r in enumerate((6, 11, 16)):
        d.arc((23 - r, 24 - r, 23 + r, 24 + r), start=-50, end=50, fill=_hex("#FF5CF0", 255 - k * 60), width=2)
    return im


def logos():
    os.makedirs(IMG, exist_ok=True)
    for name, fn in (("logo_amps-and-arcs.png", _amps), ("logo_echoes-and-encores.png", _echoes)):
        fn().resize((192, 192), Image.NEAREST).save(os.path.join(IMG, name))
    copies = [
        (os.path.join(OUT, "icons", "bits-and-bolts.png"), "logo_bits-and-bolts.png"),
        (os.path.join(OUT, "icons", "bolt-buddies.png"), "logo_bots-and-buddies.png"),
        (os.path.join(OUT, "..", "Lines-and-Loads", "assets", "icon", "icon_192.png"), "logo_lines-and-loads.png"),
    ]
    for src, dst in copies:
        if os.path.exists(src):
            shutil.copyfile(src, os.path.join(IMG, dst))


def crowd(order):
    """Alle Roboter als Gruppenbild in drei versetzten Reihen, BYTE vorn in der Mitte."""
    sprites = [Image.open(os.path.join(IMG, "bots", b.lower() + ".png")).convert("RGBA") for b in order]
    rows = [sprites[14:22], sprites[7:14], sprites[0:7]]
    # Hintere Reihe zuerst, vorne zuletzt, damit die vorderen über den hinteren stehen
    step, w = 34, 40
    width = step * 7 + w + 12
    canvas = Image.new("RGBA", (width, 48 + 2 * 22 + 6), (0, 0, 0, 0))
    for ri, row in enumerate(rows):
        offset = (width - (step * (len(row) - 1) + w)) // 2
        for k, sp in enumerate(row):
            y = ri * 22 + (2 if k % 2 else 0)
            canvas.alpha_composite(sp, (offset + k * step, y))
    canvas.resize((canvas.width * 4, canvas.height * 4), Image.NEAREST).save(os.path.join(IMG, "crowd.png"))


def foes(keys):
    """Die Störungen aus dem Schacht, locker verstreut auf dunklem Grund mit Schrauben und Staub."""
    rng = random.Random(7)
    W, H = 330, 120
    canvas = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(canvas)
    for _ in range(70):
        x, y = rng.randrange(W), rng.randrange(H)
        c = rng.choice([(58, 74, 66, 140), (168, 184, 176, 110), (107, 74, 0, 140)])
        d.rectangle((x, y, x + rng.choice((0, 1)), y), fill=c)
    slots = []
    cols = 6
    for i, key in enumerate(keys):
        sp = Image.open(os.path.join(IMG, "foes", key + ".png")).convert("RGBA")
        cx = 8 + (i % cols) * 54 + rng.randrange(-4, 10) + (27 if (i // cols) % 2 else 0)
        cy = 6 + (i // cols) * 58 + rng.randrange(-4, 8)
        cx = max(0, min(W - sp.width, cx))
        cy = max(0, min(H - sp.height, cy))
        slots.append((cy, cx, sp))
    for cy, cx, sp in sorted(slots, key=lambda s: s[0]):
        canvas.alpha_composite(sp, (cx, cy))
    canvas.resize((W * 3, H * 3), Image.NEAREST).save(os.path.join(IMG, "foes.png"))
