"""Baut den Bereich B.A.B.E.L.: babel/index.html (Titel, Kabel zu den fünf Spielen, die Welt) und je eine Seite pro Spiel.

Außerdem schaltet es die beiden alten Archive ab: Jede Seite unter archiv/ und archiv2/ wird zu einer Weiterleitung auf babel/.
make_archiv.py und make_archiv2.py deshalb nicht mehr laufen lassen, sie würden die Archive wieder herstellen.

    python tools/make_babel.py
"""
import os

import babel_art
from archiv_data import ORDER
from babel_details import FOES, copy_images, extra

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")

# Reihenfolge wie im Wort: B, A, B, E, L
GAMES = [
    dict(slug="bots-and-buddies", letter="B", name="Bots &amp; Buddies", color="#3dff7a", category="Roboter-Pflege &amp; Auto-Kampf",
         status=("dev", "In Arbeit"),
         where="Werkstatt und Schrottschacht",
         pitch="Roboter pflegen, ausrüsten und als Team hinunter in den Schrottschacht schicken. Dort unten warten die Roboter, "
               "die beim langen Stillstand heruntergefallen sind, und man holt sie Schicht für Schicht zurück.",
         play=["Roboter füttern, reparieren und bei Laune halten, ein bisschen wie ein Tamagotchi.",
               "Expeditionen als Auto-Kämpfe: Das Team kämpft selbst, du stellst es zusammen und rüstest es aus.",
               "Gerettete Roboter ziehen in die Werkstatt ein und machen in den anderen Spielen mit."],
         places=["Werkstatt in einem leeren Laufwerksschacht", "Schraubenhalde", "Kabelsalat", "Lüftergrund", "Netzteil mit dem Brummtrafo"],
         links=[("Datenschutz / Privacy", "../../bolt-buddies/")]),
    dict(slug="amps-and-arcs", letter="A", name="Amps &amp; Arcs", color="#ff5252", category="Action-Roguelite",
         status=("plan", "Konzept"),
         where="Anschlüsse und Steckkarten",
         pitch="Ein actionreiches Roguelite. Über die Anschlüsse rieselt Rauschen in den PC: Störsignale, Datenmüll, Funken. "
               "Ein Roboter läuft durch die Leitungen, entstört Welle um Welle und baut sich dabei Bauteil für Bauteil zu einer kleinen Störschutz-Maschine aus.",
         play=["Mit einem Daumen laufen, gefeuert wird von selbst.",
               "Alle paar Sekunden ein neues Bauteil aus dreien wählen: Kondensator, Spule, Diode, Quarz und mehr.",
               "Am Ende jedes Abschnitts wartet ein großer Störer, der Torwächter."],
         places=["Anschlüsse", "Netzwerkkarte", "Grafikkarte"],
         links=[]),
    dict(slug="bits-and-bolts", letter="B", name="Bits &amp; Bolts", color="#ffb000", category="Rätsel-Roguelite",
         status=("live", "Im Play Store"),
         where="Platine bis zum Hauptrechner",
         pitch="Binär-Rätsel als Roguelite. Ein Roboter klettert Etage für Etage über die Platine hinauf zum Hauptrechner, "
               "dem Gedächtnis des PCs. Jedes Rätsel setzt alte Daten wieder zusammen und holt ein Stück Erinnerung zurück.",
         play=["Nullen und Einsen nach wenigen, klaren Regeln eintragen.",
               "22 Roboter, jeder mit einer eigenen Regel, die das Rätsel verändert.",
               "Unterwegs Ereignisse wie Stromausfall oder Störsignal, oben der Hauptrechner als Ziel jedes Aufstiegs."],
         places=["Steckkarten", "Knopfzelle", "Chipsatz", "Arbeitsspeicher", "Hauptrechner"],
         links=[("Im Play Store ↗", "https://play.google.com/store/apps/details?id=com.beigel.bitsandbolts"),
                ("Datenschutz / Privacy", "../../bits-and-bolts/")]),
    dict(slug="echoes-and-encores", letter="E", name="Echoes &amp; Encores", color="#ff5cf0", category="Rhythmusspiel",
         status=("plan", "Konzept"),
         where="Soundkarte und PC-Lautsprecher",
         pitch="Ein gemütliches Rhythmusspiel. Seit dem Neustart ist der PC stumm. Die Roboter spielen als Band und holen Lied für Lied "
               "die alten Klänge zurück, bis am Ende der Startton des PCs wieder erklingt.",
         play=["Töne laufen als Impulse über Leiterbahnen zum Lautsprecher, du tippst im Takt.",
               "Die Roboter spielen die Kanäle: Melodie, Bass, Schlagzeug, Begleitung. Jeder bringt eine Eigenart mit.",
               "Kein Game Over, nur wie sauber das Lied klang."],
         places=["Soundkarte", "Kabel zur Front", "PC-Lautsprecher"],
         links=[]),
    dict(slug="lines-and-loads", letter="L", name="Lines &amp; Loads", color="#4de8ff", category="Aufbau &amp; Automatisierung",
         status=("proto", "Prototyp"),
         where="Laufwerke",
         pitch="Ein Automatisierungsspiel. In den halb erwachten Laufwerken bauen die Roboter eine Fabrik: Schächte holen Schrott herauf, "
               "Flachbandkabel tragen ihn weiter, Maschinen machen daraus Module und fertige Ausrüstung.",
         play=["Maschinen setzen und mit Förderbändern verbinden, in sauberen Verhältnissen.",
               "Dieselben wenigen Maschinen bauen alles. Was herauskommt, hängt davon ab, was hineinkommt.",
               "Laufwerk für Laufwerk reparieren, die Roboter arbeiten mit."],
         places=["Festplatte", "CD-Laufwerk", "Flachbandkabel", "später Diskettenlaufwerk und Frontblende"],
         links=[]),
]

BADGE = {"live": "badge-live", "dev": "badge-dev", "proto": "badge-dev", "plan": "badge-plan"}


def skeleton(depth, title, desc, body, wide=True):
    return f"""<!DOCTYPE html>
<html lang="de">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="icon" href="{depth}favicon.svg" type="image/svg+xml">
<link rel="icon" href="{depth}favicon-32.png" sizes="32x32" type="image/png">
<link rel="apple-touch-icon" href="{depth}apple-touch-icon.png">
<link rel="stylesheet" href="{depth}style.css?v=202611171215">
</head>
<body class="babel-page">

<header class="site">
  <div class="wrap wrap-wide">
    <a class="brand" href="{depth}">B31G3L<i>_</i></a>
    <nav>
      <a href="{depth}#apps">Apps</a>
      <a href="{depth}#spiele">Spiele</a>
      <a href="{depth}babel/">B.A.B.E.L.</a>
      <a href="https://github.com/B31G3L" target="_blank" rel="noopener">GitHub</a>
    </nav>
  </div>
</header>

<main>
{body}
</main>

<footer class="site">
  <div class="wrap{' wrap-wide' if wide else ''}">
    <span>© 2026 Christian Beigelbeck</span>
    <span><a href="{depth}impressum/">Impressum &amp; Datenschutz dieser Website</a></span>
  </div>
</footer>
</body>
</html>
"""


def write(rel, html):
    d = os.path.join(OUT, rel)
    os.makedirs(d, exist_ok=True)
    with open(os.path.join(d, "index.html"), "w", encoding="utf-8", newline="\n") as f:
        f.write(html)


# ── Titel und PC mit den fünf Spielen ────────────────────────────────────────
# Ein Koordinatensystem für alles: Das SVG hat viewBox 0 0 W H, die Kacheln sitzen in Prozent darüber.
# So treffen die Kabel die Kacheln auf jeder Breite.
W, H = 1000, 1340
LX = [300, 400, 500, 600, 700]
LETTER_Y = 120
# Mitte jeder Kachel im PC, in der Reihenfolge von GAMES (B, A, B, E, L)
SPOTS = {
    "bits-and-bolts": (330, 470),      # Platine, oben der Hauptrechner
    "lines-and-loads": (690, 440),     # Laufwerke vorn oben
    "amps-and-arcs": (330, 860),       # Anschlüsse und Steckkarten hinten unten
    "echoes-and-encores": (705, 830),  # Lautsprecher in der Front
    "bots-and-buddies": (500, 1180),   # Werkstatt und Schacht ganz unten
}
# Jede Kachel ist gleich groß, in Einheiten des SVG: halbe Breite und halbe Höhe (siehe .babel-tile im CSS:
# 29 % breit, 17.5 % hoch). So enden die Kabel genau am Rand, auf jeder Bildschirmbreite.
TILE_HW, TILE_HH = 145, 117
# Die Kabel laufen in eigenen Bahnen, damit sie keine Kachel kreuzen und sich nicht schneiden.
# Je Kabel die Knickpunkte nach dem Lötpunkt unter dem Buchstaben, der letzte liegt am Rand der Kachel.
ROUTES = {
    # B: außen links ganz hinunter, dann von links in die Werkstatt
    "bots-and-buddies": [(300, 185), (135, 185), (135, 1180), (500 - TILE_HW, 1180)],
    # A: links innen hinunter, von links an die Anschlüsse
    "amps-and-arcs": [(400, 225), (162, 225), (162, 860), (330 - TILE_HW, 860)],
    # B: kurz nach links, von oben auf die Platine
    "bits-and-bolts": [(500, 265), (330, 265), (330, 470 - TILE_HH)],
    # E: durch die Mitte zwischen Platine und Laufwerken, von links an den Lautsprecher
    "echoes-and-encores": [(600, 225), (512, 225), (512, 830), (705 - TILE_HW, 830)],
    # L: gerade hinunter auf die Laufwerke
    "lines-and-loads": [(700, 440 - TILE_HH)],
}


def route_path(x0, y0, pts, r=22):
    """Pfad über die Knickpunkte mit abgerundeten Ecken."""
    full = [(x0, y0)] + pts
    d = f"M{x0} {y0}"
    for k in range(1, len(full) - 1):
        (ax, ay), (bx, by), (cx, cy) = full[k - 1], full[k], full[k + 1]
        def toward(px, py, qx, qy, dist):
            length = max(1.0, ((qx - px) ** 2 + (qy - py) ** 2) ** 0.5)
            dd = min(dist, length / 2)
            return px + (qx - px) / length * dd, py + (qy - py) / length * dd
        p1 = toward(bx, by, ax, ay, r)
        p2 = toward(bx, by, cx, cy, r)
        d += f" L{p1[0]:.0f} {p1[1]:.0f} Q{bx} {by} {p2[0]:.0f} {p2[1]:.0f}"
    ex, ey = full[-1]
    d += f" L{ex} {ey}"
    return d


def pc_svg():
    """Ein schemenhafter offener Tower von der Seite: hinten die Platine, vorn die Laufwerke, unten Schacht und Netzteil."""
    case = '<rect class="pc-case" x="110" y="250" width="780" height="1060" rx="34"/>'
    parts = [case,
             # Platine mit Hauptrechner, Speicher, Chipsatz und Steckplätzen
             '<rect class="pc-board" x="150" y="290" width="380" height="720" rx="10"/>',
             '<rect class="pc-chip" x="280" y="330" width="110" height="110" rx="6"/>',
             '<path class="pc-trace" d="M335 440 V520 H240 M390 385 H470 M335 330 V300"/>',
             '<rect class="pc-part" x="430" y="320" width="18" height="160" rx="3"/>',
             '<rect class="pc-part" x="458" y="320" width="18" height="160" rx="3"/>',
             '<rect class="pc-part" x="240" y="560" width="70" height="70" rx="5"/>',
             '<circle class="pc-part" cx="420" cy="600" r="26"/>',
             '<rect class="pc-part" x="180" y="760" width="320" height="22" rx="3"/>',
             '<rect class="pc-part" x="180" y="830" width="320" height="22" rx="3"/>',
             '<rect class="pc-part" x="180" y="900" width="320" height="22" rx="3"/>',
             # Anschlüsse hinten
             '<rect class="pc-port" x="96" y="760" width="28" height="40" rx="4"/>',
             '<rect class="pc-port" x="96" y="830" width="28" height="40" rx="4"/>',
             '<rect class="pc-port" x="96" y="900" width="28" height="40" rx="4"/>',
             # Laufwerke vorn
             '<rect class="pc-bay" x="580" y="300" width="270" height="80" rx="6"/>',
             '<rect class="pc-bay" x="580" y="400" width="270" height="80" rx="6"/>',
             '<rect class="pc-bay" x="580" y="500" width="270" height="80" rx="6"/>',
             '<path class="pc-trace" d="M580 440 H530"/>',
             # Front mit Lautsprecher
             '<circle class="pc-part" cx="790" cy="760" r="38"/>',
             '<circle class="pc-part" cx="790" cy="760" r="20"/>',
             # Aufzug und Schacht, Netzteil
             '<path class="pc-shaft" d="M560 600 V1060 M620 600 V1060"/>',
             '<rect class="pc-bay" x="150" y="1060" width="700" height="210" rx="10"/>',
             '<path class="pc-trace" d="M190 1110 H330 M190 1150 H290 M700 1220 h110"/>']
    cables = []
    for i, g in enumerate(GAMES):
        x0 = LX[i]
        d = route_path(x0, LETTER_Y + 30, ROUTES[g["slug"]])
        cables.append(
            f'  <g style="--c:{g["color"]}">\n'
            f'    <path class="babel-cable" d="{d}" pathLength="100"/>\n'
            f'    <path class="babel-pulse" d="{d}" pathLength="100" style="animation-delay:{-0.7 * i:.1f}s"/>\n'
            f'    <circle class="babel-solder" cx="{x0}" cy="{LETTER_Y + 30}" r="7"/>\n'
            f'    <text class="babel-letter" x="{x0}" y="{LETTER_Y}">{g["letter"]}</text>\n'
            f'    <text class="babel-dot" x="{x0 + 50}" y="{LETTER_Y}">.</text>\n'
            f'  </g>')
    return (f'<svg class="babel-pc-svg" viewBox="0 0 {W} {H}" preserveAspectRatio="none" aria-hidden="true">\n'
            + "\n".join("  " + p for p in parts) + "\n" + "\n".join(cables) + "\n</svg>")


def tile(g):
    cls, label = g["status"]
    x, y = SPOTS[g["slug"]]
    return (f'      <a class="babel-tile" href="{g["slug"]}/" style="--c:{g["color"]};left:{x / W * 100:.2f}%;top:{y / H * 100:.2f}%">\n'
            f'        <img class="pix" src="img/logo_{g["slug"]}.png" alt="" width="96" height="96">\n'
            f'        <span class="babel-tile-name">{g["name"]}</span>\n'
            f'        <span class="babel-tile-cat">{g["category"]}</span>\n'
            f'        <span class="badge {BADGE[cls]}">{label}</span>\n'
            f'      </a>')


WORLD = """
    <section class="babel-world" id="welt">
      <h2 class="section-title">Die Welt <span>// ein alter Tower-PC</span></h2>
      <p class="lead">BABEL ist ein alter Tower-PC. Jahrelang stand er ausgeschaltet in einer Ecke, jetzt läuft er wieder. Mit dem Strom sind die Roboter aufgewacht, BYTE als Erster.</p>
      <p>Für die Roboter ist der PC eine ganze Welt. Hinten ragt die Platine auf: unten die Steckkarten, darüber Knopfzelle, Chipsatz und Arbeitsspeicher, ganz oben der Hauptrechner. Er ist das Gedächtnis des PCs, und jeder Roboter hat dort eine Spur hinterlassen. Vorne stecken die Laufwerke, in einem leeren Schacht dazwischen liegt die Werkstatt. Ein Aufzug führt hinunter in den Schrottschacht, wo sich alles sammelt, was in all den Jahren heruntergefallen ist: Staub, Schrauben, abgebrochene Teile.</p>
      <p>Und die Roboter selbst. Beim langen Stillstand sind sie alle hinuntergefallen. Unten in <a href="bots-and-buddies/">Bots &amp; Buddies</a> holt man sie zurück, oben in <a href="bits-and-bolts/">Bits &amp; Bolts</a> ihre Erinnerungen. In den Laufwerken bauen sie mit <a href="lines-and-loads/">Lines &amp; Loads</a> eine Fabrik, an den Anschlüssen halten sie in <a href="amps-and-arcs/">Amps &amp; Arcs</a> das Rauschen fern, und in <a href="echoes-and-encores/">Echoes &amp; Encores</a> bringen sie den stummen Lautsprecher wieder zum Klingen.</p>
      <ul class="babel-facts">
        <li><b>Keine Menschen.</b> Wer den PC eingeschaltet hat, spielt keine Rolle.</li>
        <li><b>Keine Bedrohung.</b> Kein Feind, kein Zeitdruck. Es geht um Neugier, Freunde finden und den PC Stück für Stück herrichten.</li>
        <li><b>Störungen</b> gehören dazu wie Wetter: Oben auf der Platine flackern Wackelkontakte, Störsignale, Stromausfälle und Überspannung. Unten im Schacht wuchern sie zu Getier.</li>
        <li><b>22 Roboter</b> leben hier, jeder mit einer Heimat im PC und einer Eigenart, die er in jedes Spiel mitbringt.</li>
      </ul>
      <p class="babel-name"><b>Der Name.</b> Wie der Turm von Babel ist BABEL ein Turm, in dem jeder anders spricht: in Bits, in Strömen, in Tönen. Und die Anfangsbuchstaben der fünf Spiele ergeben genau dieses Wort.</p>
    </section>"""

PEOPLE = """
    <section class="babel-band" id="bewohner">
      <h2 class="section-title">Die Bewohner <span>// 22 Roboter</span></h2>
      <p>Sie sind mit dem Strom aufgewacht, jeder mit einer Heimat irgendwo im PC und einer Eigenart, die er in jedes Spiel mitbringt.
      In <a href="bots-and-buddies/">Bots &amp; Buddies</a> holt man sie aus dem Schacht, in <a href="bits-and-bolts/">Bits &amp; Bolts</a> ihre Erinnerungen zurück.</p>
      <img class="pix babel-crowd" src="img/crowd.png" alt="Alle 22 Roboter als Gruppenbild" width="1160" height="392" loading="lazy">
    </section>

    <section class="babel-band" id="stoerungen">
      <h2 class="section-title">Die Störungen <span>// Getier im Schacht</span></h2>
      <p>Keine Feinde mit Absicht. Wo im PC kein Roboter wohnt, wuchern Störungen: oben auf der Platine wie Wetter, unten im Schacht wie Getier.
      Bugs, Spam-Drohnen und Rostwürmer, und in jeder Schicht ein Wächter, bis hinunter zum Brummtrafo im Netzteil.</p>
      <img class="pix babel-foes" src="img/foes.png" alt="Die Störungen aus dem Schacht" width="990" height="360" loading="lazy">
    </section>"""

index_body = f"""  <div class="wrap wrap-wide">
    <section class="babel-hero">
      <h1 class="babel-sr">B.A.B.E.L.</h1>
      <p class="eyebrow">Fünf Spiele · ein alter PC</p>
      <div class="babel-pc">
{pc_svg()}
{chr(10).join(tile(g) for g in GAMES)}
      </div>
    </section>
{WORLD}
{PEOPLE}
  </div>"""

copy_images()
babel_art.logos()
babel_art.crowd(ORDER)
babel_art.foes([f[0] for f in FOES])

write("babel", skeleton("../", "B.A.B.E.L. – fünf Spiele in einem alten PC",
                        "B.A.B.E.L.: Bots &amp; Buddies, Amps &amp; Arcs, Bits &amp; Bolts, Echoes &amp; Encores und Lines &amp; Loads. Fünf Spiele mit Robotern in einem alten Tower-PC.",
                        index_body))


# ── Seiten der Spiele ────────────────────────────────────────────────────────
for i, g in enumerate(GAMES):
    cls, label = g["status"]
    prev_g, next_g = GAMES[i - 1], GAMES[(i + 1) % len(GAMES)]
    links = "".join(f'<a href="{u}"{" target=\"_blank\" rel=\"noopener\"" if u.startswith("http") else ""}>{t}</a>' for t, u in g["links"])
    links_html = f'\n      <div class="app-links babel-links">{links}</div>' if links else ""
    body = f"""  <div class="wrap babel-game" style="--c:{g['color']}">
    <a class="back-link" href="../">← B.A.B.E.L.</a>
    <div class="babel-game-head">
      <img class="pix babel-game-logo" src="../img/logo_{g['slug']}.png" alt="" width="96" height="96">
      <div>
        <p class="eyebrow">{g['letter']} in B.A.B.E.L. · {g['category']}</p>
        <h1 class="page-title">{g['name']}</h1>
        <span class="badge {BADGE[cls]}">{label}</span>
      </div>
    </div>
    <p class="babel-where">Spielt in: {g['where']}</p>
    <p class="lead">{g['pitch']}</p>{links_html}

    <h2>So spielt es sich</h2>
    <ul class="babel-list">
{chr(10).join(f'      <li>{p}</li>' for p in g['play'])}
    </ul>

    <h2>Wo es spielt</h2>
    <ul class="babel-places">
{chr(10).join(f'      <li>{p}</li>' for p in g['places'])}
    </ul>
{extra(g['slug'])}
    <nav class="babel-pager">
      <a href="../{prev_g['slug']}/" style="--c:{prev_g['color']}">← <b>{prev_g['letter']}</b> {prev_g['name']}</a>
      <a href="../{next_g['slug']}/" style="--c:{next_g['color']}"><b>{next_g['letter']}</b> {next_g['name']} →</a>
    </nav>
  </div>"""
    write("babel/" + g["slug"], skeleton("../../", f"{g['name']} – B.A.B.E.L.", g["pitch"].split(". ")[0] + ".", body, wide=False))


# ── Alte Archive abschalten ──────────────────────────────────────────────────
def redirect(depth):
    return f"""<!DOCTYPE html>
<html lang="de">
<head>
<meta charset="UTF-8">
<meta name="robots" content="noindex">
<meta http-equiv="refresh" content="0; url={depth}babel/">
<link rel="canonical" href="https://b31g3l.github.io/babel/">
<title>Weitergeleitet zu B.A.B.E.L.</title>
</head>
<body><p>Das Archiv gibt es nicht mehr. Weiter zu <a href="{depth}babel/">B.A.B.E.L.</a></p></body>
</html>
"""


for root in ("archiv", "archiv2"):
    for dp, dn, fn in os.walk(os.path.join(OUT, root)):
        if "index.html" in fn:
            depth = "../" * (os.path.relpath(dp, OUT).replace("\\", "/").count("/") + 1)
            with open(os.path.join(dp, "index.html"), "w", encoding="utf-8", newline="\n") as f:
                f.write(redirect(depth))
print("ok")
