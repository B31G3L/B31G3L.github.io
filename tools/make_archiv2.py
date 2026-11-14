# Erzeugt das Archiv 2.0 (die Welt, neu gedacht) für B31G3L.github.io.
# Aufruf aus dem Repo: python tools/make_archiv2.py [Zielordner]
# Alles hier ist ein Entwurf auf dem Papier, nichts davon ist schon in den Spielen umgesetzt.
import os, sys, html
from archiv_data import ORDER, COLORS, SAYS, KEEPSAKE, PUZZLE, TRAIT, HOME

OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
STAND = "14.11.2026"
BOTS = "../../archiv/roboter/bots/"   # Die Sprites liegen schon im alten Archiv
ART = "../../archiv/weltkarte/img/"

PAGES = [("", "Übersicht", "Was hier entsteht"), ("welt", "Die Welt", "Der alte PC"), ("roboter", "Roboter", "Alle 22 und ihre Heimat")]
DRAFT = '<span class="badge badge-plan">Entwurf</span>'


CUR = ' aria-current="page"'


def page(slug, title, desc, body):
    depth = "../" if slug == "" else "../../"
    nav = "\n".join(
        f'        <li><a href="{depth}archiv2/{s + "/" if s else ""}"{CUR if s == slug else ""}>{t}<small>{sub}</small></a></li>'
        for s, t, sub in PAGES)
    return f"""<!DOCTYPE html>
<html lang="de">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{html.escape(title)} – Archiv 2.0</title>
<meta name="description" content="{html.escape(desc)}">
<link rel="icon" href="{depth}favicon.svg" type="image/svg+xml">
<link rel="icon" href="{depth}favicon-32.png" sizes="32x32" type="image/png">
<link rel="apple-touch-icon" href="{depth}apple-touch-icon.png">
<link rel="stylesheet" href="{depth}style.css">
</head>
<body>

<header class="site">
  <div class="wrap wrap-wide">
    <a class="brand" href="{depth}">B31G3L<i>_</i></a>
    <nav><a href="{depth}#spiele">Spiele</a><a href="{depth}archiv/">Archiv</a><a href="{depth}archiv2/">Archiv 2.0</a></nav>
  </div>
</header>

<main>
  <div class="wrap wrap-wide wiki">
    <nav class="wiki-nav" aria-label="Archiv 2.0">
      <p class="eyebrow">Archiv 2.0</p>
      <ul>
{nav}
      </ul>
    </nav>
    <article class="wiki-page">
{body}
      <p class="meta wiki-stand">Entwurf vom {STAND}. Alles hier ist noch auf dem Papier und nicht in den Spielen umgesetzt. Den heutigen Stand der Spiele zeigt das <a href="{depth}archiv/">Archiv</a>.</p>
    </article>
  </div>
</main>

<footer class="site">
  <div class="wrap wrap-wide">
    <span>© 2026 Christian Beigelbeck</span>
    <span><a href="{depth}impressum/">Impressum &amp; Datenschutz dieser Website</a></span>
  </div>
</footer>
</body>
</html>
"""


def write(slug, title, desc, body):
    d = os.path.join(OUT, "archiv2", slug) if slug else os.path.join(OUT, "archiv2")
    os.makedirs(d, exist_ok=True)
    with open(os.path.join(d, "index.html"), "w", encoding="utf-8", newline="\n") as f:
        f.write(page(slug, title, desc, body))


def head(eyebrow, title, lead):
    return f"""      <p class="eyebrow">{eyebrow}</p>
      <h1 class="page-title">{title} {DRAFT}</h1>
      <p class="wiki-lead">{lead}</p>
"""


def table(cols, rows, cls=""):
    th = "".join(f"<th>{c}</th>" for c in cols)
    trs = "\n".join("<tr>" + "".join(f"<td>{c}</td>" for c in r) + "</tr>" for r in rows)
    return f'<div class="wiki-table{cls}"><table>\n<thead><tr>{th}</tr></thead>\n<tbody>\n{trs}\n</tbody>\n</table></div>\n'


# ── Die Orte im PC ───────────────────────────────────────────────────────────
## Schlüssel, Name, Bauteil, Bereich, Spiel, Text, Bild (aus dem alten Archiv) oder leer
PLACES = [
    ("hauptrechner", "Hauptrechner", "Prozessor unter dem Kühlkörper", "Oben", "Bits &amp; Bolts · Ziel jedes Aufstiegs",
     "Der höchste Punkt der Welt und ihr Gedächtnis. Hier liegt alles, was der PC je erlebt hat, und jeder Roboter hat hier eine Spur hinterlassen. "
     "Wer oben ankommt, findet heraus, wer er war, bevor der PC ausging. Der Hauptrechner ist ein Ort, keine Figur: Er spricht nicht, aber er erinnert sich.", ""),
    ("chipsatz", "Chipsatz", "Platine · Etage 7–8", "Platine", "Bits &amp; Bolts",
     "Eine Kreuzung, an der alle Leiterbahnen zusammenlaufen. Hier wird geschaltet und entschieden, wer wohin darf. Der Marktplatz der Platine.", ""),
    ("knopfzelle", "Knopfzelle", "Platine · Etage 5–6", "Platine", "Bits &amp; Bolts",
     "Die kleine Batterie, die die Uhr am Laufen hielt, auch als der PC aus war. Ein stiller, fast heiliger Ort: Sie hat nie aufgehört.", ""),
    ("arbeitsspeicher", "Arbeitsspeicher", "Platine · Etage 3–4", "Platine", "Bits &amp; Bolts",
     "Die Speicherriegel stehen wie Hochhäuser in einer Reihe. Hier ist immer Betrieb, Zahlen kommen und gehen.", ""),
    ("steckkarten", "Steckkarten", "Platine · Etage 1–2", "Platine", "Bits &amp; Bolts",
     "Steckkarten ragen wie Wände und Klippen aus der Platine. Hier beginnt der Aufstieg.", ""),
    ("werkstatt", "Werkstatt", "Leerer Laufwerksschacht", "Mitte", "Bolt Buddies · Zuhause",
     "Vorne im Gehäuse, wo früher ein Diskettenlaufwerk steckte. Geschützt und gemütlich. Hier wohnen alle Geretteten, und jeder stellt sein Andenken auf. "
     "Von hier führt der Aufzug hinunter in den Schacht.", "workshop.png"),
    ("schicht1", "Erste Schicht", "Schacht · Name noch offen", "Unten", "Bolt Buddies",
     "Gleich unter der Werkstatt. Im Spiel heißt sie heute Speicherkeller. Das passt nicht mehr, weil der Arbeitsspeicher jetzt oben auf der Platine liegt.", ""),
    ("kabelsalat", "Kabelsalat", "Schacht · Kabel", "Unten", "Bolt Buddies",
     "Ein Dschungel aus alten Kabeln, Kabelbindern und Staub. Hier leben die Wackelkontakte.", "layer_1.png"),
    ("lueftergrund", "Lüftergrund", "Schacht · Gehäuselüfter", "Unten", "Bolt Buddies",
     "Am Gehäuselüfter weht es kalt, Staubflusen treiben herum. Hier leben die Frostbugs.", "layer_2.png"),
    ("netzteil", "Netzteil", "Schacht · ganz unten", "Unten", "Bolt Buddies",
     "Ganz unten brummt und glüht es, es ist heiß. Hier leben die Überhitzer. Im Spiel heißt die Schicht heute Kernzone, aber der Kern ist ja oben.", "layer_3.png"),
    ("festplatte", "Festplatte", "Lage noch offen", "Weitere", "noch keinem Spiel zugeordnet",
     "Eine alte Scheibe, die sich dreht. Vielleicht das Archiv oder eine Bibliothek.", ""),
    ("grafikkarte", "Grafikkarte", "Lage noch offen", "Weitere", "noch keinem Spiel zugeordnet",
     "Bunt, laut und voller Licht.", ""),
    ("anschluesse", "Anschlüsse", "Hinten am Gehäuse · Lage noch offen", "Weitere", "noch keinem Spiel zugeordnet",
     "Der Rand der Welt. Dahinter ist das Draußen, das keiner kennt.", ""),
]
PLACE = {p[0]: p for p in PLACES}
COLOR = {"Oben": "3DFF7A", "Platine": "4DE8FF", "Mitte": "FFB000", "Unten": "FF9A3D", "Weitere": "C9A8FF"}

## Heimat jedes Roboters (Entwurf). Gefunden wird er trotzdem im Schacht, siehe SHAFT.
HEIMAT = {
    "arbeitsspeicher": ["BYTE", "NIBBLE", "OKTA", "HEXA", "PARI"],
    "festplatte": ["ASKI", "MIRA"],
    "grafikkarte": ["PIXA", "CHROMA"],
    "chipsatz": ["GATE", "XOR", "SHIFT"],
    "knopfzelle": ["LOOP", "QUBIT"],
    "anschluesse": ["MORSE"],
    "kabelsalat": ["PATCH", "GLITCH"],
    "lueftergrund": ["NULL", "VIRUS"],
    "netzteil": ["ROOT", "ERROR", "DAEMON"],
}
HOME_OF = {b: p for p, bots in HEIMAT.items() for b in bots}
assert sorted(HOME_OF) == sorted(ORDER), "jeder Roboter braucht genau eine Heimat"
## Die Schichten des Schachts in der Reihenfolge von Bolt Buddies (core/bots.gd HOME: 0 bis 3)
SHAFT = ["schicht1", "kabelsalat", "lueftergrund", "netzteil"]


def mini(b, link=True):
    img = f'<img src="{BOTS}{b.lower()}.png" width="20" height="24" alt="">'
    return (f'<a class="mini-bot" href="../roboter/#{b.lower()}" style="--bot:#{COLORS[b]}">{img}{b}</a>' if link
            else f'<span class="mini-bot" style="--bot:#{COLORS[b]}">{img}{b}</span>')


def found_here(key):
    return [b for b in ORDER if b != "BYTE" and SHAFT[HOME[b]] == key]


def place_card(key):
    _, name, part, area, game_, text, img = PLACE[key]
    pic = f'<img class="place-img" src="{ART}{img}" alt="{name}" loading="lazy">' if img else ""
    lives = HEIMAT.get(key, [])
    rows = f'<p class="place-bots"><b>Wohnen hier:</b> {" ".join(mini(b) for b in lives)}</p>' if lives else ""
    found = found_here(key)
    if found:
        rows += f'<p class="place-bots"><b>Hier gefunden:</b> {" ".join(mini(b) for b in found)}</p>'
    if key == "werkstatt":
        rows += f'<p class="place-bots"><b>Schon da:</b> {mini("BYTE")} war als Erster wach.</p>'
    return f"""          <li class="place" id="{key}" style="scroll-margin-top:16px">{pic}<div class="place-head"><h3>{name}</h3></div><p class="game-genre">{part} · {game_}</p><p>{text}</p>{rows}</li>"""


def places(*keys):
    return '        <ul class="place-list">\n' + "\n".join(place_card(k) for k in keys) + "\n        </ul>\n"


def tower():
    """Der PC im Querschnitt: Mitte von oben nach unten, rechts die Orte, deren Lage noch offen ist."""
    cells = []
    for key, name, part, area, game_, text, img in PLACES:
        bots = HEIMAT.get(key, [])
        faces = "".join(f'<img src="{BOTS}{b.lower()}.png" width="16" height="19" alt="{b}" title="{b}">' for b in bots)
        faces = f'<span class="tower-faces">{faces}</span>' if faces else ""
        cls = "rig-cell tower-cell" + (" rig-plan" if area == "Weitere" else "")
        cells.append(f'          <a class="{cls}" href="#{key}" style="grid-area:{key};--c:#{COLOR[area]}">'
                     f'<small>{part}</small><b>{name}</b>{faces}</a>')
    labels = [("lbl-up", "↑ Bits &amp; Bolts: der Aufstieg"), ("lbl-down", "↓ Bolt Buddies: der Schrottschacht")]
    cells += [f'          <p class="tower-label" style="grid-area:{k}">{t}</p>' for k, t in labels]
    return '        <nav class="rig tower" aria-label="Der PC im Querschnitt">\n' + "\n".join(cells) + "\n        </nav>\n"


# ── Übersicht ────────────────────────────────────────────────────────────────
cards = "\n".join(
    f'<li class="app-card"><a class="wiki-card-link" href="{s}/"><h3 class="app-title">{t}</h3><p class="app-desc">{d}</p></a></li>'
    for s, t, d in [
        ("welt", "Die Welt", "Ein alter Tower-PC, der wieder läuft: Hauptrechner, Platine, Werkstatt und Schrottschacht im Querschnitt."),
        ("roboter", "Roboter", "Alle 22 Roboter mit ihrer Heimat im PC, ihrem Fundort im Schacht und ihrem Andenken."),
    ])
write("", "Übersicht", "Archiv 2.0: Die Welt der Roboter wird neu gedacht. Entwurf zu Welt und Robotern von Bits & Bolts und Bolt Buddies.",
      head("Archiv 2.0", "Archiv 2.0",
           "Hier wird die Welt der Roboter von vorne gedacht, erst auf dem Papier. Was hier steht, ist ein Entwurf und kann sich noch ändern. "
           "Den heutigen Stand der Spiele zeigt weiter das <a href=\"../archiv/\">alte Archiv</a>.") + f"""
      <section class="wiki-sec">
        <h2>Die Welt in einem Satz</h2>
        <p>Ein alter Tower-PC wird wieder eingeschaltet, die Roboter wachen auf, und weil beim langen Stillstand alle heruntergefallen sind, holt man sie aus dem Schacht zurück und begleitet sie hinauf zum Hauptrechner, wo ihre Erinnerungen liegen.</p>
      </section>

      <section class="wiki-sec">
        <h2>Bereiche</h2>
        <ul class="app-grid wiki-cards">
{cards}
        </ul>
      </section>

      <section class="wiki-sec">
        <h2>Was fest steht</h2>
        {table(["", ""], [
            ["Spiele", "Bits &amp; Bolts und Bolt Buddies bleiben"],
            ["Roboter", "alle 22 bleiben, mit Namen, Aussehen und Fähigkeiten"],
            ["Stil", "bleibt: Pixel, Retro-Terminal, Bildschirmflimmern"],
            ["Neu offen", "alles andere, auch ob und wie die fünf geplanten Spiele in die Welt passen"],
        ], " wiki-table-plain")}
      </section>
""")


# ── Die Welt ─────────────────────────────────────────────────────────────────
write("welt", "Die Welt", "Die Welt der Roboter ist ein alter Tower-PC: oben der Hauptrechner als Gedächtnis, in der Mitte die Werkstatt, unten der Schrottschacht.",
      head('<a href="../">Archiv 2.0</a> · Die Welt', "Die Welt",
           "Die ganze Welt ist ein alter Tower-PC. Er stand jahrelang ausgeschaltet herum, jetzt läuft er wieder. "
           "Für die Roboter ist er riesig: oben der Hauptrechner, in der Mitte die Werkstatt, unten der Schrottschacht.") + f"""
      <section class="wiki-sec">
        <h2>Grundsätze</h2>
        {table(["", ""], [
            ["Schauplatz", "ein alter Tower-PC, sonst nichts"],
            ["Anfang", "Der PC wird wieder eingeschaltet. Mit dem Strom wachen die Roboter auf, BYTE als Erster."],
            ["Menschen", "spielen keine Rolle. Wer den PC eingeschaltet hat, ist egal."],
            ["Bedrohung", "gibt es nicht. Kein Zeitdruck, kein Feind, der alles zerstören will."],
            ["Antrieb", "Neugier und Gemeinschaft: Freunde finden, den PC erkunden, ihn Stück für Stück herrichten."],
            ["Störungen", "gehören zum PC wie Wetter oder Ungeziefer: Staubflusen, Wackelkontakte, Bugs. Eher lästig als böse."],
            ["Ton", "gemütlich"],
        ], " wiki-table-plain")}
      </section>

      <section class="wiki-sec">
        <h2>Der PC im Querschnitt</h2>
{tower()}        <p class="muted-small">Jedes Feld führt zu seinem Ort weiter unten. Gestrichelt: Orte, deren Lage noch offen ist. Die kleinen Figuren sind die Roboter, die dort zu Hause sind.</p>
      </section>

      <section class="wiki-sec" id="warum">
        <h2>Warum alle unten liegen</h2>
        <p>Jeder Roboter hat eine Heimat irgendwo im PC. Als der PC ausging, sind aber alle heruntergefallen und liegen jetzt verstreut im Schrottschacht. Je tiefer jemand gefallen ist, desto schwerer ist er zu finden.</p>
        <p>So greifen die beiden Spiele ineinander: <b>Unten im Schacht findet man verlorene Roboter, oben im Hauptrechner verlorene Erinnerungen.</b> Das Andenken, das jeder Gerettete in die Werkstatt mitbringt, erinnert an seine Heimat.</p>
      </section>

      <section class="wiki-sec">
        <h2>Oben: der Hauptrechner</h2>
{places("hauptrechner")}      </section>

      <section class="wiki-sec">
        <h2>Der Weg nach oben: die Platine</h2>
        <p>In Bits &amp; Bolts klettert ein Roboter Etage für Etage über das Mainboard nach oben. Heute sind die Etagen nur durchnummeriert. Künftig gehören jeweils mehrere Etagen zu einer Gegend mit eigener Stimmung. Kleinere Chips auf dem Weg sind die Zwischenrechner, Etappenziele vor dem Hauptrechner. Die Binärrätsel sind dabei wörtlich das, was die Roboter tun: alte Daten wieder zusammensetzen.</p>
        {table(["Etagen", "Gegend", "Stimmung"], [
            ["1–2", '<a href="#steckkarten">Steckkarten</a>', "Wände und Klippen, der Einstieg"],
            ["3–4", '<a href="#arbeitsspeicher">Arbeitsspeicher</a>', "Hochhäuser, viel Betrieb"],
            ["5–6", '<a href="#knopfzelle">Knopfzelle</a>', "still, uralt"],
            ["7–8", '<a href="#chipsatz">Chipsatz</a>', "Kreuzung, alle Wege treffen sich"],
            ["zwischendurch", "Zwischenrechner", "kleine Chips als Etappenziel"],
            ["Ende", '<a href="#hauptrechner">Hauptrechner</a>', "das Gedächtnis"],
        ])}        <p class="muted-small">Die Aufteilung ist ein Beispiel. Welche Gegenden es gibt und in welcher Reihenfolge, ist noch offen.</p>
{places("steckkarten", "arbeitsspeicher", "knopfzelle", "chipsatz")}      </section>

      <section class="wiki-sec">
        <h2>Mitte: die Werkstatt</h2>
{places("werkstatt")}      </section>

      <section class="wiki-sec">
        <h2>Unten: der Schrottschacht</h2>
        <p>Der Boden des Gehäuses. Hier landet alles, was in all den Jahren heruntergefallen ist: Staub, verlorene Schrauben, abgebrochene Teile und die Roboter selbst. In Bolt Buddies steigt ein Team Schicht für Schicht hinab und holt sie zurück. Dass Schrauben die Währung sind, passt: In einem alten PC fallen genau die nach unten.</p>
        <p class="muted-small">Bilder: die heutigen Kulissen aus Bolt Buddies.</p>
{places(*SHAFT)}      </section>

      <section class="wiki-sec">
        <h2>Weitere Orte</h2>
        <p>Diese Orte gibt es im PC, und Roboter wohnen dort. Wo sie genau liegen und ob ein Spiel dorthin führt, ist noch offen.</p>
{places("festplatte", "grafikkarte", "anschluesse")}      </section>

      <section class="wiki-sec">
        <h2>Noch offen</h2>
        <ul class="plain-list">
          <li>Die fünf geplanten Spiele: Port Patrol, Loop Echo, Tilt Gate, Surge Chain und Packet Rush. Bekommen sie einen Platz, werden sie umgebaut, oder fallen sie weg?</li>
          <li>Die Störungen: welche Wesen und Ärgernisse in welcher Gegend leben. Für den Schacht gibt es schon welche, für die Platine noch nicht.</li>
          <li>Die Orte im Detail: wie es dort aussieht und was dort besonders ist.</li>
          <li>Der Name der ersten Schicht im Schacht.</li>
        </ul>
      </section>
""")


# ── Roboter ──────────────────────────────────────────────────────────────────
def bot_card(b):
    home = PLACE[HOME_OF[b]][1]
    found = "war als Erster wach und wartet in der Werkstatt" if b == "BYTE" else PLACE[SHAFT[HOME[b]]][1]
    return f"""<li class="bot-card" id="{b.lower()}" style="--bot:#{COLORS[b]}">
  <div class="bot-head">
    <div class="bot-screen"><img src="{BOTS}{b.lower()}.png" width="80" height="96" alt="{b}" loading="lazy"></div>
    <div class="bot-name"><h3>{b}</h3><span class="bot-say">„{html.escape(SAYS[b])}“</span></div>
  </div>
  <dl class="app-meta bot-world">
    <div><dt>Heimat</dt><dd><a href="../welt/#{HOME_OF[b]}">{home}</a></dd></div>
    <div><dt>Gefunden</dt><dd>{"" if b == "BYTE" else f'<a href="../welt/#{SHAFT[HOME[b]]}">'}{found}{"" if b == "BYTE" else "</a>"}</dd></div>
    <div><dt>Andenken</dt><dd>{html.escape(KEEPSAKE[b])}</dd></div>
  </dl>
  <details class="bot-more"><summary>In den Spielen</summary>
    <p><b>Bits &amp; Bolts:</b> {html.escape(PUZZLE[b])}</p>
    <p><b>Bolt Buddies:</b> {html.escape(TRAIT[b][0].upper() + TRAIT[b][1:])}.</p>
  </details>
</li>"""

groups = []
for key, *_ in PLACES:
    if key not in HEIMAT:
        continue
    name, part = PLACE[key][1], PLACE[key][2]
    groups.append(f"""      <section class="wiki-sec">
        <h2>{name} <span class="muted-small">{part}</span></h2>
        <ul class="bot-grid">
{chr(10).join(bot_card(b) for b in HEIMAT[key])}
        </ul>
      </section>
""")
index = "".join(f'<a href="#{b.lower()}" style="--bot:#{COLORS[b]}"><img src="{BOTS}{b.lower()}.png" width="40" height="48" alt="" loading="lazy"><span>{b}</span></a>'
                for k in HEIMAT for b in HEIMAT[k])
write("roboter", "Roboter", "Alle 22 Roboter in der Welt des alten PCs: Heimat, Fundort im Schrottschacht und Andenken.",
      head('<a href="../">Archiv 2.0</a> · Roboter', "Roboter",
           "Alle 22 Roboter, sortiert nach ihrer Heimat im PC, von oben nach unten. Ihre Namen kommen aus der Computersprache, und meist verraten sie schon, wo sie zu Hause sind.") + f"""
      <nav class="bot-index" aria-label="Roboter">{index}</nav>
      <div class="callout wiki-note">
        <b>Heimat und Fundort:</b> Jeder Roboter wohnt eigentlich irgendwo im PC. Als der PC ausging, sind aber alle in den Schrottschacht gefallen. Dort findet man sie in Bolt Buddies, je tiefer, desto später. Ihr Andenken stellen sie in der Werkstatt auf. <a href="../welt/#warum">Mehr dazu →</a>
      </div>
{"".join(groups)}""")
print("ok")
