"""Baut den Bereich B.A.B.E.L.: babel/index.html (Titel, Kabel zu den fünf Spielen, die Welt) und je eine Seite pro Spiel.

Außerdem schaltet es die beiden alten Archive ab: Jede Seite unter archiv/ und archiv2/ wird zu einer Weiterleitung auf babel/.
make_archiv.py und make_archiv2.py deshalb nicht mehr laufen lassen, sie würden die Archive wieder herstellen.

    python tools/make_babel.py
"""
import os

from babel_details import copy_images, extra

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")

# Reihenfolge wie im Wort: B, A, B, E, L
GAMES = [
    dict(slug="bots-and-buddies", letter="B", name="Bots &amp; Buddies", color="#ffb000",
         status=("dev", "In Arbeit"),
         where="Werkstatt und Schrottschacht",
         pitch="Roboter pflegen, ausrüsten und als Team hinunter in den Schrottschacht schicken. Dort unten warten die Roboter, "
               "die beim langen Stillstand heruntergefallen sind, und man holt sie Schicht für Schicht zurück.",
         play=["Roboter füttern, reparieren und bei Laune halten, ein bisschen wie ein Tamagotchi.",
               "Expeditionen als Auto-Kämpfe: Das Team kämpft selbst, du stellst es zusammen und rüstest es aus.",
               "Gerettete Roboter ziehen in die Werkstatt ein und machen in den anderen Spielen mit."],
         places=["Werkstatt in einem leeren Laufwerksschacht", "Schraubenhalde", "Kabelsalat", "Lüftergrund", "Netzteil mit dem Brummtrafo"],
         links=[("Datenschutz / Privacy", "../../bolt-buddies/")]),
    dict(slug="amps-and-arcs", letter="A", name="Amps &amp; Arcs", color="#ff5252",
         status=("plan", "Konzept"),
         where="Anschlüsse und Steckkarten",
         pitch="Ein actionreiches Roguelite. Über die Anschlüsse rieselt Rauschen in den PC: Störsignale, Datenmüll, Funken. "
               "Ein Roboter läuft durch die Leitungen, entstört Welle um Welle und baut sich dabei Bauteil für Bauteil zu einer kleinen Störschutz-Maschine aus.",
         play=["Mit einem Daumen laufen, gefeuert wird von selbst.",
               "Alle paar Sekunden ein neues Bauteil aus dreien wählen: Kondensator, Spule, Diode, Quarz und mehr.",
               "Am Ende jedes Abschnitts wartet ein großer Störer, der Torwächter."],
         places=["Anschlüsse", "Netzwerkkarte", "Grafikkarte"],
         links=[]),
    dict(slug="bits-and-bolts", letter="B", name="Bits &amp; Bolts", color="#4ade80",
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
    dict(slug="echoes-and-encores", letter="E", name="Echoes &amp; Encores", color="#c084fc",
         status=("plan", "Konzept"),
         where="Soundkarte und PC-Lautsprecher",
         pitch="Ein gemütliches Rhythmusspiel. Seit dem Neustart ist der PC stumm. Die Roboter spielen als Band und holen Lied für Lied "
               "die alten Klänge zurück, bis am Ende der Startton des PCs wieder erklingt.",
         play=["Töne laufen als Impulse über Leiterbahnen zum Lautsprecher, du tippst im Takt.",
               "Die Roboter spielen die Kanäle: Melodie, Bass, Schlagzeug, Begleitung. Jeder bringt eine Eigenart mit.",
               "Kein Game Over, nur wie sauber das Lied klang."],
         places=["Soundkarte", "Kabel zur Front", "PC-Lautsprecher"],
         links=[]),
    dict(slug="lines-and-loads", letter="L", name="Lines &amp; Loads", color="#60a5fa",
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
<link rel="stylesheet" href="{depth}style.css">
</head>
<body class="babel-page">

<header class="site">
  <div class="wrap{' wrap-wide' if wide else ''}">
    <a class="brand" href="{depth}">B31G3L<i>_</i></a>
    <nav><a href="{depth}#spiele">Spiele</a><a href="{depth}babel/">B.A.B.E.L.</a></nav>
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


# ── Titel mit Kabeln ─────────────────────────────────────────────────────────
# Das SVG skaliert als Ganzes mit der Breite. Die Kabel enden genau über der Mitte der fünf gleich breiten Spalten darunter.
W, H, TOP = 1000, 400, 150
LX = [260, 380, 500, 620, 740]


def title_svg():
    parts = []
    for i, g in enumerate(GAMES):
        lx, cx = LX[i], 100 + 200 * i
        d = f"M{lx} {TOP} C{lx} {TOP + 120} {cx} {TOP + 100} {cx} {H - 60} L{cx} {H}"
        parts.append(
            f'  <g style="--c:{g["color"]}">\n'
            f'    <path class="babel-cable" d="{d}" pathLength="100"/>\n'
            f'    <path class="babel-pulse" d="{d}" pathLength="100" style="animation-delay:{-0.7 * i:.1f}s"/>\n'
            f'    <circle class="babel-solder" cx="{lx}" cy="{TOP}" r="7"/>\n'
            f'    <text class="babel-letter" x="{lx}" y="122">{g["letter"]}</text>\n'
            f'    <text class="babel-dot" x="{lx + 60}" y="122">.</text>\n'
            f'  </g>')
    return (f'<svg class="babel-title" viewBox="0 0 {W} {H}" role="img" aria-label="B.A.B.E.L.">\n'
            + "\n".join(parts) + "\n</svg>")


def node(g):
    cls, label = g["status"]
    return (f'      <li><a class="babel-node" href="{g["slug"]}/" style="--c:{g["color"]}">\n'
            f'        <span class="babel-node-letter">{g["letter"]}</span>\n'
            f'        <span class="babel-node-name">{g["name"]}</span>\n'
            f'        <span class="babel-node-where">{g["where"]}</span>\n'
            f'        <span class="badge {BADGE[cls]}">{label}</span>\n'
            f'      </a></li>')


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

index_body = f"""  <div class="wrap wrap-wide">
    <section class="babel-hero">
      <h1 class="babel-sr">B.A.B.E.L.</h1>
      <p class="eyebrow">Fünf Spiele · ein Rechner</p>
{title_svg()}
      <ul class="babel-nodes">
{chr(10).join(node(g) for g in GAMES)}
      </ul>
    </section>
{WORLD}
  </div>"""

write("babel", skeleton("../", "B.A.B.E.L. – fünf Spiele in einem alten PC",
                        "B.A.B.E.L.: Bots &amp; Buddies, Amps &amp; Arcs, Bits &amp; Bolts, Echoes &amp; Encores und Lines &amp; Loads. Fünf Spiele mit Robotern in einem alten Tower-PC.",
                        index_body))


copy_images()

# ── Seiten der Spiele ────────────────────────────────────────────────────────
for i, g in enumerate(GAMES):
    cls, label = g["status"]
    prev_g, next_g = GAMES[i - 1], GAMES[(i + 1) % len(GAMES)]
    links = "".join(f'<a href="{u}"{" target=\"_blank\" rel=\"noopener\"" if u.startswith("http") else ""}>{t}</a>' for t, u in g["links"])
    links_html = f'\n      <div class="app-links babel-links">{links}</div>' if links else ""
    body = f"""  <div class="wrap babel-game" style="--c:{g['color']}">
    <a class="back-link" href="../">← B.A.B.E.L.</a>
    <div class="babel-game-head">
      <span class="babel-game-letter" aria-hidden="true">{g['letter']}</span>
      <div>
        <p class="eyebrow">{g['letter']} in B.A.B.E.L. · {g['where']}</p>
        <h1 class="page-title">{g['name']}</h1>
        <span class="badge {BADGE[cls]}">{label}</span>
      </div>
    </div>
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
