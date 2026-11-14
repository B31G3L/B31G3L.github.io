# Erzeugt die Archiv-Seiten (Wiki zum Roboter-Universum) für B31G3L.github.io.
# Aufruf aus dem Repo: python tools/make_archiv.py
import os, sys, html, shutil

OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
STAND = "14.11.2026"

PAGES = [  # slug, Titel im Menü, Untertitel
    ("", "Das Archiv", "Übersicht"),
    ("roboter", "Roboter-Register", "Alle 22 Roboter"),
    ("stoerungen", "Störungsprotokoll", "Gegner und Ereignisse"),
    ("weltkarte", "Weltkarte", "Der Rechner und seine Spiele"),
    ("ersatzteile", "Ersatzteillager", "Ausrüstung und Werte"),
    ("funk", "Funkverbindung", "Spiele verbinden"),
]

def page(slug, body, desc):
    depth = "../" if slug == "" else "../../"
    title = next(p[1] for p in PAGES if p[0] == slug)
    nav = []
    for s, t, sub in PAGES:
        href = depth + "archiv/" + (s + "/" if s else "")
        cur = ' aria-current="page"' if s == slug else ""
        nav.append(f'<li><a href="{href}"{cur}>{t}<small>{sub}</small></a></li>')
    return f"""<!DOCTYPE html>
<html lang="de">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{html.escape(title)} – Archiv der Roboter</title>
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
    <nav><a href="{depth}#spiele">Spiele</a><a href="{depth}archiv/">Archiv</a></nav>
  </div>
</header>

<main>
  <div class="wrap wrap-wide wiki">
    <nav class="wiki-nav" aria-label="Archiv">
      <p class="eyebrow">Archiv</p>
      <ul>
        {chr(10).join("        " + n for n in nav).strip()}
      </ul>
    </nav>
    <article class="wiki-page">
{body}
      <p class="meta wiki-stand">Stand der Einträge: {STAND}. Spiele mit „In Entwicklung“ oder „Geplant“ können sich noch ändern.</p>
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

## Filter nach Spiel: Jede Seite hat oben eine Leiste, die nur Inhalte eines Spiels zeigt.
## Inhalte tragen data-game mit einem oder mehreren Kürzeln, ungetaggtes bleibt immer sichtbar.
## Alles läuft über CSS (:has auf den Radioknöpfen), ohne Skript.
GAMES = [("bnb", "Bits &amp; Bolts"), ("bb", "Bolt Buddies"), ("plan", "Geplante Spiele")]

def g(tags):
    """Attribut für Inhalte, die zu einem oder mehreren Spielen gehören."""
    return f' data-game="{tags}"'

def filter_bar(body):
    """Die Leiste mit Alle und den Spielen. Für Spiele ohne Inhalt auf der Seite gibt es einen Hinweis."""
    chips = ['<input type="radio" name="flt" id="flt-all" checked><label for="flt-all">Alle</label>']
    empty = []
    for key, name in GAMES:
        chips.append(f'<input type="radio" name="flt" id="flt-{key}"><label for="flt-{key}">{name}</label>')
        tagged = [m for m in body.split('data-game="')[1:] if key in m.split('"')[0].split()]
        if not tagged:
            empty.append(f'<p class="flt-empty" data-empty="{key}">Zu {name} gibt es auf dieser Seite nichts.</p>')
    return ('      <fieldset class="flt"><legend>Nach Spiel filtern</legend>' + "".join(chips) + "</fieldset>\n"
            + "".join("      " + e + "\n" for e in empty))

def write(slug, body, desc):
    d = os.path.join(OUT, "archiv", slug) if slug else os.path.join(OUT, "archiv")
    os.makedirs(d, exist_ok=True)
    # Die Filterleiste steht direkt unter dem Einleitungstext
    at = body.find("</p>", body.find('class="wiki-lead"')) + len("</p>\n")
    body = body[:at] + filter_bar(body) + body[at:]
    with open(os.path.join(d, "index.html"), "w", encoding="utf-8", newline="\n") as f:
        f.write(page(slug, body, desc))

def head(eyebrow, title, lead):
    return f"""      <p class="eyebrow">{eyebrow}</p>
      <h1 class="page-title">{title}</h1>
      <p class="wiki-lead">{lead}</p>
"""

def table(cols, rows, cls="", tags=None):
    """tags: je Zeile die Spiele für den Filter, leer heißt immer sichtbar."""
    th = "".join(f"<th>{c}</th>" for c in cols)
    tags = tags or [""] * len(rows)
    trs = "\n".join(f"<tr{g(t) if t else ''}>" + "".join(f"<td>{c}</td>" for c in r) + "</tr>" for r, t in zip(rows, tags))
    return f'<div class="wiki-table{cls}"><table>\n<thead><tr>{th}</tr></thead>\n<tbody>\n{trs}\n</tbody>\n</table></div>\n'

LIVE = '<span class="badge badge-dev">In Entwicklung</span>'
STORE = '<span class="badge badge-live">Im Play Store</span>'
PLAN = '<span class="badge badge-plan">Geplant</span>'

# ── Daten aus den Spielen ────────────────────────────────────────────────────
ORDER = ["BYTE", "OKTA", "GATE", "NULL", "HEXA", "PARI", "ASKI", "QUBIT", "CHROMA", "NIBBLE", "GLITCH",
         "PATCH", "LOOP", "XOR", "MIRA", "PIXA", "SHIFT", "ROOT", "VIRUS", "ERROR", "DAEMON", "MORSE"]
BASE = {
    "BYTE": [3, 3, 3, 3], "OKTA": [4, 3, 2, 3], "HEXA": [2, 3, 5, 2], "ASKI": [2, 2, 5, 3],
    "PIXA": [2, 4, 3, 3], "CHROMA": [3, 3, 4, 2], "GATE": [3, 1, 2, 6], "LOOP": [2, 5, 3, 2],
    "NULL": [2, 4, 4, 2], "PARI": [3, 3, 3, 3], "MIRA": [2, 3, 3, 4], "SHIFT": [3, 5, 2, 2],
    "XOR": [5, 3, 2, 2], "GLITCH": [4, 4, 3, 1], "PATCH": [2, 2, 3, 5], "NIBBLE": [4, 3, 1, 4],
    "QUBIT": [1, 5, 5, 1], "ROOT": [5, 1, 3, 3], "VIRUS": [3, 3, 4, 2], "ERROR": [6, 2, 2, 2],
    "DAEMON": [4, 2, 4, 2], "MORSE": [2, 4, 4, 2],
}
TRAIT = {
    "BYTE": "heilt 2 Leben je Zug", "OKTA": "trifft alle Gegner zugleich", "HEXA": "+20 % Volltreffer",
    "ASKI": "+30 % Schrauben fürs Team", "PIXA": "heilt 3 Leben je Zug", "CHROMA": "+50 % Erfahrung fürs Team",
    "GATE": "lenkt Angriffe auf sich, 2 Panzerung", "LOOP": "+20 % Tempo", "NULL": "+20 % Ausweichen",
    "PARI": "heilt sich um 30 % des Schadens", "MIRA": "3 Schaden an Angreifern",
    "SHIFT": "ist als Erster dran, +10 % Ausweichen", "XOR": "zielt auf den hintersten Gegner, +15 % Volltreffer",
    "GLITCH": "+30 % Volltreffer", "PATCH": "blockt 2 Treffer je Kampf",
    "NIBBLE": "heilt sich um 20 % des Schadens, +15 % Schrauben fürs Team", "QUBIT": "+30 % Ausweichen",
    "ROOT": "2 Panzerung", "VIRUS": "Getroffene rosten: 2 Schaden je Zug", "ERROR": "2 Schaden an Angreifern, +10 % Volltreffer",
    "DAEMON": "ist als Erster dran, heilt sich um 15 % des Schadens", "MORSE": "zielt auf den hintersten Gegner, +25 % Erfahrung fürs Team",
}
PUZZLE = {
    "BYTE": "Der Allrounder. 5 Ladungen, 3 Tipps, keine Besonderheiten.",
    "OKTA": "Liest Oktalzahlen an den Zeilen, startet aber mit 1 Ladung weniger.",
    "GATE": "Bringt in jedes Rätsel Zeichen zwischen Zellen: = heißt gleich, × heißt verschieden.",
    "NULL": "Zeigt, wo in einer Linie die erste 0 steht, hat aber nur 2 Tipps.",
    "HEXA": "Liest Hexzahlen an den Zeilen. 4 Tipps, aber 1 Ladung weniger.",
    "PARI": "Bringt in jedes Rätsel Blöcke mit gleich vielen Nullen und Einsen.",
    "ASKI": "Liest ASCII-Zeichen an den Zeilen. 5 Ladungen, aber nur 2 Tipps.",
    "QUBIT": "Verschränkt Zellen: Von zwei Zellen mit gleichem Buchstaben ist genau eine 1.",
    "CHROMA": "Liest Farbbalken an den Zeilen, hat aber nur 2 Tipps.",
    "NIBBLE": "Zählt in Häppchen: Rahmen um vier Zellen sagen, wie viele Einsen darin stehen.",
    "GLITCH": "Zeigt zwei Zahlen an einer Linie, nur eine stimmt. 4 Tipps, aber 1 Ladung weniger.",
    "PATCH": "Flickt sich selbst: Der erste Kurzschluss in jedem Rätsel kostet nichts. Dafür 2 Ladungen weniger.",
    "LOOP": "Seine Raster haben keinen Rand: Nie drei gleiche gilt auch über den Rand hinweg.",
    "XOR": "Zählt, an wie vielen Stellen sich zwei Nachbarlinien unterscheiden. Dafür 4 Tipps.",
    "MIRA": "Verbindet Linien, die Spiegelbilder sind. 5 Ladungen, 3 Tipps.",
    "PIXA": "Zeigt Pixelblöcke an Zeilen und Spalten. 5 Ladungen, 3 Tipps.",
    "SHIFT": "Verbindet Nachbarlinien, die um eine Stelle verschoben sind. 5 Ladungen, 3 Tipps.",
    "ROOT": "Sieht auch schräg: Nie drei gleiche gilt bei ihm auch diagonal. Dafür 1 Tipp mehr.",
    "VIRUS": "Steckt an: Bei einem Kurzschluss erlischt auch eine Ziffer daneben. Dafür 1 Ladung mehr.",
    "ERROR": "Baut Fehler ein: Eine Vorgabe ist falsch. Dafür 1 Tipp mehr.",
    "DAEMON": "Läuft im Hintergrund: Wer zu lange nichts Richtiges einträgt, verliert Ladung. Dafür 1 Ladung mehr.",
    "MORSE": "Funkt im Nebel: Klar zu sehen ist nur die Umgebung der letzten Zelle. Dafür 1 Tipp mehr.",
}
UNLOCK = {"OKTA": (1, 0), "GATE": (2, 0), "NULL": (3, 1), "HEXA": (4, 1), "PARI": (5, 2), "ASKI": (6, 2),
          "QUBIT": (8, 3), "CHROMA": (10, 3), "NIBBLE": (12, 4), "GLITCH": (14, 4), "PATCH": (16, 4),
          "LOOP": (18, 5), "XOR": (20, 5), "MIRA": (22, 5), "PIXA": (24, 5), "SHIFT": (26, 5), "ROOT": (28, 5),
          "VIRUS": (30, 5), "ERROR": (32, 5), "DAEMON": (34, 5), "MORSE": (36, 5)}
SAYS = {"GATE": "Zutritt!", "LOOP": "Und nochmal!", "NULL": "...", "PARI": "Halbe-halbe!", "MIRA": "!ollaH",
        "SHIFT": "Rutsch rüber!", "XOR": "Anders!", "GLITCH": "H#ll§!", "BYTE": "Hallo!", "OKTA": "Blubb!",
        "HEXA": "0xF00D!", "ASKI": "Hi :)", "CHROMA": "Ooh, bunt!", "PIXA": "Piep!", "PATCH": "Hält schon!",
        "NIBBLE": "Happs!", "QUBIT": "0 und 1!", "ROOT": "sudo hallo", "VIRUS": "Hatschi!", "ERROR": "404!",
        "DAEMON": "Läuft…", "MORSE": "·– ·–"}
ROLE = {"OKTA": "Rätselhinweis", "HEXA": "Rätselhinweis", "ASKI": "Rätselhinweis", "PIXA": "Rätselhinweis",
        "CHROMA": "Rätselhinweis", "NULL": "Rätselhinweis", "MIRA": "Rätselhinweis", "SHIFT": "Rätselhinweis",
        "XOR": "Rätselhinweis", "GLITCH": "Rätselhinweis", "GATE": "Zusatzregel", "PARI": "Zusatzregel",
        "LOOP": "Zusatzregel", "NIBBLE": "Zusatzregel", "QUBIT": "Zusatzregel", "ROOT": "Zusatzregel",
        "ERROR": "Ereignis", "VIRUS": "Ereignis", "DAEMON": "Ereignis", "MORSE": "Ereignis",
        "PATCH": "Fähigkeit", "BYTE": "Allrounder"}
HERO = {"BYTE": "Bits & Bolts, Bolt Buddies", "LOOP": "Loop Runner (geplant)", "GATE": "Kippwelt (geplant)",
        "ROOT": "Kippwelt (geplant)", "ERROR": "Zündkette (geplant)", "GLITCH": "Zündkette (geplant)",
        "SHIFT": "Loop Runner (geplant)", "QUBIT": "Loop Runner (geplant)"}
ATTR = ["Leistung", "Takt", "Logik", "Gehäuse"]
## Bolt Buddies: In welcher Ebene ein Roboter auf Rettung wartet (core/bots.gd HOME) und was er mitbringt (i18n ks_*)
LAYERS = [("Speicherkeller", 1), ("Kabelschacht", 11), ("Kühlkreislauf", 21), ("Kernzone", 31)]
HOME = {
    "BYTE": 0, "OKTA": 0, "HEXA": 0, "ASKI": 0, "PIXA": 0, "NIBBLE": 0, "PARI": 0, "MIRA": 0,
    "GATE": 1, "LOOP": 1, "SHIFT": 1, "XOR": 1, "MORSE": 1, "PATCH": 1,
    "NULL": 2, "CHROMA": 2, "GLITCH": 2, "QUBIT": 2, "VIRUS": 2,
    "ROOT": 3, "ERROR": 3, "DAEMON": 3,
}
KEEPSAKE = {
    "BYTE": "Pinnwand mit Fotos", "OKTA": "Aquarium", "HEXA": "Snackautomat", "ASKI": "Altes Terminal",
    "PIXA": "Staffelei mit Pixelbild", "CHROMA": "Farbeimer", "GATE": "Schranke", "LOOP": "Hamsterrad",
    "NULL": "Leerer Bilderrahmen", "PARI": "Waage", "MIRA": "Spiegel", "SHIFT": "Rutsche", "XOR": "Schachbrett",
    "GLITCH": "Flackernder Fernseher", "PATCH": "Verbandskasten", "NIBBLE": "Keksdose", "QUBIT": "Kristallkugel",
    "ROOT": "Chefsessel", "VIRUS": "Kaktus", "ERROR": "Warnschild 404", "DAEMON": "Kaffeemaschine", "MORSE": "Morsetaste",
}

## Farben der Roboter wie in Bolt Buddies (ui/style.gd), für den Rahmen ums Sprite
COLORS = {
    "BYTE": "3DFF7A", "OKTA": "FF9E2C", "HEXA": "4DE8FF", "PIXA": "FF5CF0", "ASKI": "E8F0FF", "CHROMA": "7FB2FF",
    "GATE": "FFD34D", "LOOP": "7CFFB0", "NULL": "B4BECC", "PARI": "2CE6B0", "MIRA": "C9A8FF", "SHIFT": "6FC3FF",
    "XOR": "FF7A45", "GLITCH": "B07CFF", "PATCH": "5C8DFF", "NIBBLE": "C6FF3D", "QUBIT": "7DF9FF", "ROOT": "4CC26A",
    "VIRUS": "8CFF4D", "ERROR": "FF4D4D", "DAEMON": "C04DFF", "MORSE": "FFC66B",
}


## Familien (geplant für Bolt Buddies 1.1): Name, Bonus, Mitglieder
FAMILIES = [
    ("Zahlensysteme", "mehr Volltreffer", ["OKTA", "HEXA", "ASKI", "CHROMA", "PIXA", "NIBBLE"]),
    ("Logikgatter", "mehr Panzerung", ["GATE", "XOR", "NULL", "PARI", "QUBIT", "MIRA"]),
    ("Prozesse", "mehr Tempo", ["BYTE", "LOOP", "SHIFT", "DAEMON", "ROOT", "MORSE"]),
    ("Störenfriede", "mehr Schaden, mehr Rost", ["VIRUS", "ERROR", "GLITCH", "PATCH"]),
]
FAMILY = {b: name for name, _, members in FAMILIES for b in members}


def copy_sprites():
    """Holt die Sprites aus Bolt Buddies, wenn der Ordner daneben liegt. Sonst bleiben die vorhandenen."""
    src = os.path.join(OUT, "..", "Bolt-Buddies", "assets", "robots")
    dst = os.path.join(OUT, "archiv", "roboter", "bots")
    if not os.path.isdir(src):
        return
    os.makedirs(dst, exist_ok=True)
    for b in ORDER:
        shutil.copyfile(os.path.join(src, b.lower() + ".png"), os.path.join(dst, b.lower() + ".png"))


def bar(v):
    return f'<span class="pips" aria-label="{v} von 6">' + "".join(
        f'<i class="{"on" if i < v else ""}"></i>' for i in range(6)) + "</span>"

def bot_card(b):
    u = UNLOCK.get(b)
    unlock = "von Anfang an" if not u else f"nach {u[0]} {'Sieg' if u[0] == 1 else 'Siegen'}, Stufe {u[1]} geschafft"
    stats = "".join(f"<div><dt>{a}</dt><dd>{bar(v)}<span class=\"num\">{v}</span></dd></div>"
                    for a, v in zip(ATTR, BASE[b]))
    hero = f'<p class="bot-hero"{g("plan")}>Held in {html.escape(HERO[b])}</p>' if b in HERO and "geplant" in HERO[b] else ""
    home = "wartet schon in der Werkstatt" if b == "BYTE" else "{}, ab Kampf {}".format(*LAYERS[HOME[b]])
    return f"""<li class="bot-card" id="{b.lower()}" style="--bot:#{COLORS[b]}">
  <div class="bot-head">
    <div class="bot-screen"><img src="bots/{b.lower()}.png" width="80" height="96" alt="{b}" loading="lazy"></div>
    <div class="bot-name"><h3>{b}</h3><span class="bot-say">„{html.escape(SAYS[b])}“</span><a class="bot-family" href="#familien">Familie: {FAMILY[b]}</a>{hero}</div>
  </div>
  <section class="bot-game bot-game-puzzle"{g("bnb")}>
    <h4><img src="../../icons/bits-and-bolts.png" alt="" width="20" height="20">Bits &amp; Bolts<span class="bot-role">{ROLE[b]}</span></h4>
    <p>{html.escape(PUZZLE[b])}</p>
    <p class="bot-unlock">Freigeschaltet {unlock}</p>
  </section>
  <section class="bot-game bot-game-fight"{g("bb")}>
    <h4><img src="../../icons/bolt-buddies.png" alt="" width="20" height="20">Bolt Buddies<span class="bot-role">Kampf</span></h4>
    <p><b>Eigenheit:</b> {html.escape(TRAIT[b])}</p>
    <dl class="bot-stats">{stats}</dl>
    <p class="bot-unlock"><b>Fundort:</b> {home}</p>
    <p class="bot-unlock"><b>Mitgebracht:</b> {html.escape(KEEPSAKE[b])}</p>
  </section>
</li>"""

# ── Seiten ───────────────────────────────────────────────────────────────────

# Übersicht
links = "\n".join(
    f'<li class="app-card"{g(tags)}><a class="wiki-card-link" href="{s}/"><h3 class="app-title">{t}</h3><p class="app-desc">{d}</p></a></li>'
    for s, t, d, tags in [
        ("roboter", "Roboter-Register", "Alle 22 Roboter mit Rätselfähigkeit, Kampfwerten, Eigenheit, Fundort und Spruch.", "bnb bb plan"),
        ("stoerungen", "Störungsprotokoll", "Alle Gegner mit Sprite, Werten und Beute, dazu die Ereignisse im Hauptrechner.", "bnb bb plan"),
        ("weltkarte", "Weltkarte", "Die Welt ist ein alter Rechner: welches Spiel in welchem Bauteil spielt, mit Bildern aller Orte.", "bnb bb plan"),
        ("ersatzteile", "Ersatzteillager", "Ausrüstung, Module, Vorräte und Stationen der Werkstatt, mit Bild und Werten.", "bb"),
        ("funk", "Funkverbindung", "Wie die Spiele später miteinander reden, damit Roboter überall stärker werden.", "bnb bb plan"),
    ])
write("", head("Archiv der Roboter", "Das Archiv",
    "Hier steht alles über die Welt von BYTE und seinen 21 Freunden: wer sie sind, wo sie unterwegs sind und was ihnen das Leben schwer macht.") + f"""
      <section class="wiki-sec">
        <h2>Die Welt in drei Sätzen</h2>
        <p>Tief in einem alten Rechner sind kleine Roboter abgeschaltet worden. BYTE fährt als Erster wieder hoch und repariert sich Etage für Etage bis zum Hauptrechner. Unterwegs weckt er andere Roboter auf, die in einer gemeinsamen Werkstatt leben, gepflegt werden und im Schrottschacht gegen Bugs und Viren antreten.</p>
      </section>

      <section class="wiki-sec">
        <h2>Bereiche des Archivs</h2>
        <ul class="app-grid wiki-cards">
{links}
        </ul>
      </section>

      <section class="wiki-sec">
        <h2>Kurz nachgeschlagen</h2>
        {table(["", ""], [
            ["Roboter", "22, alle mit eigener Rätselfähigkeit und Kampf-Eigenheit"],
            ["Spiele", "1 im Play Store, 1 in Entwicklung, 5 geplant"],
            ["Attribute", "Leistung, Takt, Logik, Gehäuse"],
            ["Welt", "ein alter Rechner, jedes Spiel spielt in einem Bauteil"],
            ["Gegner", "Bug, Spam-Drohne, Firewall, Rostwurm, Frostbug, Wackelkontakt, Überhitzer und drei Bosse"],
            ["Ereignisse", "8 Störungen im Hauptrechner, von Stromausfall bis Nebel"],
            ["Währung", "Schrauben und Schrott in der Werkstatt"],
        ], " wiki-table-plain", ["bnb bb", "", "bb", "", "bb plan", "bnb", "bb"])}
      </section>
""", "Das Archiv der Roboter: Wiki zu Bits & Bolts, Bolt Buddies und allen Spielen im Roboter-Universum von B31G3L.")

# Roboter
cards = "\n".join(bot_card(b) for b in ORDER)
index = "".join(f'<a href="#{b.lower()}" style="--bot:#{COLORS[b]}"><img src="bots/{b.lower()}.png" width="40" height="48" alt="" loading="lazy"><span>{b}</span></a>' for b in ORDER)
assert sorted(FAMILY) == sorted(ORDER), "jeder Roboter braucht genau eine Familie"
assert sorted(HOME) == sorted(ORDER) and sorted(KEEPSAKE) == sorted(ORDER), "jeder Roboter braucht Fundort und Teil"
copy_sprites()
write("roboter", head("Archiv · Roboter-Register", "Roboter-Register",
    "Alle 22 Roboter in der Reihenfolge, in der man sie in Bits &amp; Bolts freischaltet. Jeder bringt ins Rätsel eine eigene Fähigkeit mit und hat in Bolt Buddies eigene Kampfwerte.") + f"""
      <nav class="bot-index" aria-label="Roboter">{index}</nav>
      <div class="callout wiki-note">
        <b>So liest du die Karten:</b> Jede Karte zeigt, was der Roboter in beiden Spielen kann: oben in Bits &amp; Bolts, unten in Bolt Buddies. Die Punkte sind die Grundwerte auf Stufe 1, zusammen immer 12. Je Stufe wächst jedes Attribut um 12 % seines Grundwerts, höchstens bis Stufe 20.
        In Bolt Buddies findet man neue Roboter im Schrottschacht, nach Kampf 2, 5, 8 und so weiter. Jeder wartet in seiner Ebene: Wer im Kühlkreislauf sitzt, lässt sich erst ab dort retten.
        Jeder Gerettete bringt ein persönliches Teil mit, das ab dann in der Werkstatt steht.
      </div>
      <ul class="bot-grid">
{cards}
      </ul>
      <section class="wiki-sec" id="familien" style="margin-top:40px"{g("bb")}>
        <h2>Familien <span class="badge badge-plan">Geplant</span></h2>
        <p>Geplant für Bolt Buddies 1.1: Zwei Roboter derselben Familie im Team geben einen kleinen Bonus, drei einen größeren.</p>
        {table(["Familie", "Roboter", "Bonus"], [[f"<b>{name}</b>", " ".join(f'<a class="fam-bot" href="#{m.lower()}" style="--bot:#{COLORS[m]}"><img src="bots/{m.lower()}.png" width="20" height="24" alt="">{m}</a>' for m in members), bonus] for name, bonus, members in FAMILIES])}
      </section>
""", "Alle 22 Roboter aus Bits & Bolts und Bolt Buddies: Rätselfähigkeit, Freischaltung, Kampfwerte und Eigenheit.")

# Weltkarte: Die ganze Welt ist ein alter Rechner, jedes Spiel spielt in einem seiner Bauteile.
# Früher gab es dafür zwei Seiten (Einsatzorte und Weltkarte), jetzt steht alles hier.
def game(id_, part, name, status, genre, what, gives, bots, places, extra="", tags="plan"):
    """Ein Bauteil des Rechners mit seinem Spiel, den Orten darin und was das Spiel den Robotern bringt."""
    return f"""      <section class="wiki-sec game" id="{id_}"{g(tags)}>
        <p class="rig-part">Bauteil: {part}</p>
        <div class="game-head"><h2>{name}</h2>{status}</div>
        <p class="game-genre">{genre}</p>
        <p>{what}</p>
        <dl class="app-meta game-meta">
          <div><dt>Helden</dt><dd>{bots}</dd></div>
          <div><dt>Bringt</dt><dd>{gives}</dd></div>
        </dl>
        <ul class="place-list">
{chr(10).join(places)}
        </ul>
{extra}      </section>
"""

def place(name, game_, text, status="", img="", photo=False):
    """Ein Ort. img: Bild unter img/, photo: Bildschirmfoto statt Pixelgrafik (wird nicht kantig vergrößert)."""
    pic = f'<img class="place-img{" place-photo" if photo else ""}" src="img/{img}" alt="{name}" loading="lazy">' if img else ""
    return f"""        <li class="place">{pic}<div class="place-head"><h3>{name}</h3>{status}</div><p class="game-genre">{game_}</p><p>{text}</p></li>"""

## Der Querschnitt: Feld, Bauteil, Ort, Spiel mit Stand, Ziel, Farbe, geplant
RIG = [
    ("cpu", "Prozessor", "Hauptrechner", "Bits &amp; Bolts", "bits-and-bolts", "3DFF7A", False),
    ("floors", "Leiterbahnen", "Die Etagen ↑", "Bits &amp; Bolts", "bits-and-bolts", "3DFF7A", False),
    ("shop", "Gehäusemitte", "Die Werkstatt", "Bolt Buddies", "bolt-buddies", "FFB000", False),
    ("lift", "Schacht", "Der Aufzug ↕", "Bolt Buddies", "bolt-buddies", "FFB000", False),
    ("l1", "Arbeitsspeicher", "Speicherkeller", "Kampf 1–10", "ebenen", "3DFF7A", False),
    ("l2", "Kabel", "Kabelschacht", "Kampf 11–20", "ebenen", "FF9A3D", False),
    ("l3", "Kühlung", "Kühlkreislauf", "Kampf 21–30", "ebenen", "4DE8FF", False),
    ("l4", "Kern", "Kernzone", "ab Kampf 31", "ebenen", "FF5252", False),
    ("net", "Netzwerkanschluss", "Die Abwehrstellung", "Block Invaders", "block-invaders", "FF5252", True),
    ("clock", "Taktgeber", "Das Schleifenlabor", "Loop Runner", "loop-runner", "7CFFB0", True),
    ("psu", "Netzteil", "Das Kondensatorlager", "Zündkette", "zuendkette", "FF9A3D", True),
    ("sensor", "Lagesensor", "Das Schwerkraft-Labor", "Kippwelt", "kippwelt", "FFD34D", True),
    ("bus", "Datenbus und Anschlüsse", "Das Datenbus-Depot", "Snake Jam", "snake-jam", "B46CFF", True),
]
rig = "\n".join(
    f'          <a class="rig-cell{" rig-plan" if plan else ""}" href="#{to}" style="grid-area:{key};--c:#{col}"{g("plan" if plan else ("bnb" if to == "bits-and-bolts" else "bb"))}>'
    f'<small>{part}</small><b>{where}</b><span>{game_}{" · geplant" if plan else ""}</span></a>'
    for key, part, where, game_, to, col, plan in RIG)

write("weltkarte", head("Archiv · Weltkarte", "Weltkarte",
    "Die ganze Welt ist ein einziger alter Rechner. Jedes Spiel spielt in einem seiner Bauteile: BYTE klettert über die Etagen nach oben zum Hauptrechner, "
    "in der Mitte liegt die Werkstatt, darunter führt der Schrottschacht in die Tiefe. Die geplanten Spiele besetzen die übrigen Bauteile. "
    "Bolt Buddies ist die Heimat, in die alle Roboter später mit Erfahrung und Beute zurückkehren, siehe <a href=\"../funk/\">Funkverbindung</a>.") + f"""
      <section class="wiki-sec">
        <h2>Der Rechner im Querschnitt</h2>
        <nav class="rig" aria-label="Querschnitt des Rechners">
{rig}
        </nav>
        <p class="muted-small">Jedes Feld führt zu seinem Bauteil. Gestrichelt: Spiele, die noch geplant sind.</p>
      </section>
""" +
    game("bits-and-bolts", "Prozessor", "Bits &amp; Bolts", STORE, "Binär-Rätsel als Roguelite",
         "Ein Roboter arbeitet sich durch zehn Stationen bis zum Hauptrechner und repariert unterwegs durchgebrannte Raster aus Nullen und Einsen. Jede falsche Ziffer ist ein Kurzschluss und kostet Ladung. Siege schalten neue Roboter und höhere Schwierigkeitsstufen frei.",
         "Logik", "Alle 22 Roboter, als Erster BYTE", [
             place("Die Etagen", "Station 1–10", "Der Weg nach oben führt über zehn Stationen: sieben Rätsel und zwei Zwischenrechner an Station 4 und 7. In jedem Rätsel gelten drei Grundregeln: nur 0 und 1, nie drei gleiche nebeneinander, in jeder Zeile und Spalte gleich viele. Dazu bringt jeder Roboter eigene Hinweise mit.", img="bnb_etagen.jpg", photo=True),
             place("Zwischenrechner", "Station 4 und 7", "Hier gelten verschärfte Bedingungen, ab Stufe 1 mit einem Ereignis wie Nebel, Zeitdruck oder falschen Vorgaben.", img="bnb_ereignis.jpg", photo=True),
             place("Hauptrechner", "Ziel jedes Runs", "Bis zu vier Sektoren: die äußeren Leitungen unter Spannung, ein Sektor mit Stromausfall, der innere Ring unter Überspannung und der Kern in 8×8. Nach jedem Sektor gibt es eine Ladung zurück.", img="bnb_haupt.jpg", photo=True),
         ],
         '        <p><a href="../stoerungen/#ereignisse">Ereignisse →</a> · <a href="https://play.google.com/store/apps/details?id=com.beigel.bitsandbolts" target="_blank" rel="noopener">Play Store ↗</a> · <a href="../../bits-and-bolts/">Datenschutz</a></p>\n', "bnb") +
    game("bolt-buddies", "Gehäusemitte und Schacht", "Bolt Buddies", LIVE, "Roboter pflegen und Auto-Kämpfe",
         "Die Werkstatt ist das Zuhause aller geretteten Roboter. Sie brauchen Akku, Öl und Aufmerksamkeit. Ein Team aus bis zu drei Robotern zieht in den Schrottschacht, kämpft dort von selbst und bringt Schrauben, Ausrüstung und neue Freunde mit.",
         "Heimat aller Roboter: Stufen, Ausrüstung, Pflege", "Alle 22 Roboter, als Erster BYTE", [
             place("Die Werkstatt", "Zuhause", "Hier wohnen alle geretteten Roboter. Sie laufen frei herum, wollen gestreichelt, geölt und geladen werden und schlafen an der Ladeleiste. Jeder Gerettete bringt ein persönliches Teil mit, so füllt sich der Raum mit jedem Roboter.", img="workshop.png"),
             place("Der Aufzug", "zwischen den Kämpfen", "Nach jedem Kampf: weiter nach unten oder mit der ganzen Beute nach Hause. Die nächsten Gegner sind schon zu sehen, und es gibt zwei Wege: den Hauptschacht und einen Nebenschacht mit zäheren Gegnern und 75 % mehr Schrauben.", img="lift.png"),
             place("Der Schrottschacht", "unter der Werkstatt", "Kampf für Kampf geht es tiefer. Dort liegen Schrauben, Akkus, Öl und Ausrüstung, und abgeschaltete Roboter warten in ihrer Ebene auf Rettung."),
         ],
         '        <h3 class="wiki-sub" id="ebenen">Die Ebenen des Schrottschachts</h3>\n'
         '        <p>Kommt mit Bolt Buddies 1.0: Alle 10 Kämpfe beginnt eine neue Ebene mit eigener Kulisse und einem eigenen Gegner. In der Mitte wartet ein Boss, im letzten Kampf ihr Wächter. '
         'Wer ihn besiegt, kann künftig an der Haltestelle der nächsten Ebene einsteigen und bekommt dafür von der Werkstatt Module mit. Gegner und Werte stehen im <a href="../stoerungen/">Störungsprotokoll</a>.</p>\n'
         '        <ul class="place-list">\n'
         + "\n".join([
             place("Speicherkeller", "Arbeitsspeicher · Kampf 1–10 · Wächter: Bluescreen", "Zwischen alten Speicherriegeln blinken Lämpchen, auf dem Boden wandern Datenpakete über die Leiterbahnen. Bugs, Spam-Drohnen, Firewalls und Rostwürmer. Hier warten 7 Roboter auf Rettung.", PLAN, "layer_0.png"),
             place("Kabelschacht", "Kabel · Kampf 11–20 · Wächter: Kurzschluss", "Durchhängende Kabelstränge, an den Haltern sprühen Funken. Hier leben die Wackelkontakte: Wer sie trifft, bekommt einen Schlag. 6 Roboter warten hier.", PLAN, "layer_1.png"),
             place("Kühlkreislauf", "Kühlung · Kampf 21–30 · Wächter: Kältekern", "Vereiste Rohre, ein großer Lüfter, Schnee fällt. Frostbugs kühlen mit ihren Treffern ab. In der Mitte kehrt der Kurzschluss zurück. 5 Roboter warten hier.", PLAN, "layer_2.png"),
             place("Kernzone", "Kern · ab Kampf 31 · Wächter wechseln", "Der Kern glüht rot, Hitze steigt auf. Überhitzer treffen das ganze Team, die drei Wächter wechseln sich ab, und es geht endlos weiter. Hier warten ROOT, ERROR und DAEMON.", PLAN, "layer_3.png"),
         ]) + "\n        </ul>\n"
         + '        <h3 class="wiki-sub">Was noch kommt</h3>\n'
         + table(["Feature", "Worum es geht", "Version"], [
             ["<b>Schacht-Ebenen</b>", 'Umgesetzt: Alle 10 Kämpfe eine neue Ebene mit eigener Kulisse, eigenem Gegner, Boss und Wächter, dazu Haltestellen zum Direkteinstieg. Siehe <a href="#ebenen">oben</a>.', "1.0"],
             ["<b>Aufzug mit zwei Wegen</b>", "Umgesetzt: Vorschau auf die nächsten Gegner, dazu ein Nebenschacht mit zäheren Gegnern und mehr Schrauben.", "1.0"],
             ["<b>Rettung je Ebene</b>", 'Umgesetzt: Jeder Roboter wartet in seiner Ebene. Wo, steht im <a href="../roboter/">Roboter-Register</a>.', "1.0"],
             ["<b>Werkstatt</b>", 'Umgesetzt: eingerichtete Werkstatt, jeder Gerettete bringt ein persönliches Teil mit. Ladeleiste, Ölbad, Spielecke und Werkbank in drei Stufen, die Funkantenne folgt mit dem Funk. Siehe <a href="../ersatzteile/#ausbau">Ersatzteillager</a>.', "1.0"],
             ["<b>Werkbank</b>", 'Umgesetzt: Teile zu Schrott zerlegen und damit Teile aufwerten, auch angelegte. Siehe <a href="../ersatzteile/#werkbank">Ersatzteillager</a>.', "1.0"],
             ["<b>Tagesschacht</b>", 'Umgesetzt: einmal am Tag eine Expedition mit Vorgabe des Tages und einem Teil als Belohnung. Siehe <a href="#tagesschacht">unten</a>.', "1.0"],
             ["<b>Erste Schritte</b>", "Umgesetzt: BYTE zeigt Neuen der Reihe nach Akku, Ölen, Expedition, Ausrüstung und den ersten Ausbau. Jeder Hinweis erscheint erst, wenn er passt.", "1.0"],
             ["<b>Erinnerungen</b>", 'Umgesetzt: höchstens eine Benachrichtigung am Tag, nur zwischen 10 und 20 Uhr, standardmäßig aus. Siehe <a href="#erinnerungen">unten</a>.', "1.0"],
             ["<b>Vertrauen</b>", "Jeder Roboter sammelt Vertrauen durch Pflege und Expeditionen. Es schaltet Sprüche, Lackierungen und eine stärkere Eigenheit frei.", "1.1"],
             ["<b>Team-Familien</b>", 'Zwei oder drei Roboter derselben Familie im Team geben einen Bonus. Siehe <a href="../roboter/#familien">Roboter-Register</a>.', "1.1"],
             ["<b>Funk</b>", 'Post aus den anderen Spielen. Siehe <a href="../funk/">Funkverbindung</a>.', "1.2"],
         ])
         + '        <h3 class="wiki-sub" id="tagesschacht">Tagesschacht</h3>\n'
         + '        <p>Einmal am Tag gibt es eine Expedition, die für alle gleich ist: Seed und Vorgabe hängen am Datum, Start ist immer bei Kampf 1. Der Versuch zählt ab dem Start. Gezählt werden die Tage im Tagesschacht, ein verpasster Tag setzt nichts zurück.</p>\n'
         + table(["Vorgabe", "Was gilt"], [
             ["<b>Keine Reparatur</b>", "Reparatur wird nie angeboten. Wer angeschlagen ist, bleibt es."],
             ["<b>Allein</b>", "Nur der erste Roboter im Team darf mit."],
             ["<b>Glaskanonen</b>", "30 % weniger Leben, 30 % mehr Schaden."],
             ["<b>Schatzsuche</b>", "Keine Module, dafür doppelte Schrauben."]])
         + '        <p>Als Belohnung gibt es ein Teil, auch nach einem Ausfall: ab Kampf 10 mindestens solide, ab Kampf 20 und an jedem 7. Tag mindestens selten.</p>\n'
         + '        <h3 class="wiki-sub" id="erinnerungen">Erinnerungen</h3>\n'
         + '        <p>In den Optionen lassen sich Erinnerungen einschalten. Beim Schließen plant das Spiel dann höchstens eine Benachrichtigung: wenn der erste Roboter ausgeschlafen ist oder etwas braucht, oder wenn der Tagesschacht wartet. Nie in den ersten zwei Stunden, nie nachts, höchstens eine am Tag. Alles läuft auf dem Handy, ohne Server.</p>\n'
         + '        <p><a href="../ersatzteile/">Zum Ersatzteillager →</a> · <a href="../../bolt-buddies/">Datenschutz</a></p>\n', "bb") +
    game("block-invaders", "Netzwerkanschluss", "Block Invaders", PLAN, "Block-Puzzle gegen angreifende Störungen",
         "Bugs, Spam-Drohnen, Firewalls und Rostwürmer rücken von außen auf die Werkstatt vor. Volle Reihen feuern Salven, volle Spalten Laser. Jede fünfte Welle bringt einen Bluescreen. Der gewählte Roboter steht als Geschütz unten und feuert mit seiner Eigenheit, zum Beispiel trifft OKTA die ganze Reihe.",
         "Leistung, Waffen-Teile", "Wählbar, je nach Eigenheit", [
             place("Die Abwehrstellung", "am Netzwerkanschluss", "Der Rand des Rechners, an dem Störungen aus dem Netz in Formation anrücken.", PLAN)]) +
    game("loop-runner", "Taktgeber", "Loop Runner", PLAN, "Zeitschleifen-Plattformer",
         "LOOP hat 20 Sekunden und sich selbst als Team: Jede Schleife wird aufgezeichnet und läuft in der nächsten als Kopie mit. Zusammen halten sie Türen offen, graben Fallen und sammeln Bits, während Wachbots patrouillieren.",
         "Takt", "LOOP, später SHIFT und QUBIT", [
             place("Das Schleifenlabor", "im Taktgeber", "Ein Labor im Herzschlag des Rechners: Alle 20 Sekunden schlägt der Takt, und die Zeit beginnt von vorn.", PLAN)]) +
    game("kippwelt", "Lagesensor", "Kippwelt", PLAN, "Plattformer ohne Springen",
         "Der Roboter dreht die ganze Welt um 90 Grad, und alles Lose fällt nach unten. Erst den Zugangschip holen, dann zum Ausgang. Kisten zerquetschen Gegner, Stacheln sind gefährlich.",
         "Gehäuse, Rüstungsteile", "GATE oder ROOT, beide halten viel aus", [
             place("Das Schwerkraft-Labor", "im Lagesensor", "Räume, die sich drehen lassen. Unten ist immer da, wo der Sensor gerade unten meldet.", PLAN)]) +
    game("zuendkette", "Netzteil", "Zündkette", PLAN, "Kettenreaktions-Rätsel",
         "Ein einziger Überspannungsimpuls muss alle Viren erwischen. Kondensatoren geben die Ladung weiter, Schrottkisten brennen weg, Steine halten auf. Gesucht ist der eine Platz, von dem aus die Kette alles erreicht, nur den Roboter nicht.",
         "Schrottkisten mit zufälliger Ausrüstung", "ERROR oder GLITCH", [
             place("Das Kondensatorlager", "im Netzteil", "Hier wird der ganze Rechner mit Strom versorgt. Voller Kondensatoren und Schrottkisten, in denen sich Viren verstecken.", PLAN)]) +
    game("snake-jam", "Datenbus und Anschlüsse", "Snake Jam", PLAN, "Schiebe-Rätsel mit wachsenden Bussen",
         "Bunte Datenbusse müssen ihre Pakete einsammeln und zum Port hinausfahren. Jedes Paket macht den Bus länger, und lange Busse stehen sich selbst im Weg.",
         "Vorräte: Akkus, Öl, Schrauben", "Noch offen, eventuell bleibt das Spiel eigenständig", [
             place("Das Datenbus-Depot", "am Datenbus", "Ein voller Parkplatz für Datenbusse, nur eine Ausfahrt zum Port.", PLAN)]),
    "Die Welt der Roboter ist ein alter Rechner: Querschnitt mit allen Bauteilen, den Spielen darin und ihren Orten, von Bits & Bolts über Bolt Buddies bis zu den geplanten Spielen.")


def redirect(slug, target, title):
    """Alte Adresse, die auf die neue Seite weiterleitet. Ohne Skript, nur mit meta refresh."""
    d = os.path.join(OUT, "archiv", slug)
    os.makedirs(d, exist_ok=True)
    with open(os.path.join(d, "index.html"), "w", encoding="utf-8", newline="\n") as f:
        f.write(f"""<!DOCTYPE html>
<html lang="de">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title} – Archiv der Roboter</title>
<meta http-equiv="refresh" content="0; url={target}">
<link rel="canonical" href="{target}">
<link rel="stylesheet" href="../../style.css">
</head>
<body>
<main><div class="wrap"><p>Diese Seite ist umgezogen: <a href="{target}">{title} →</a></p></div></main>
</body>
</html>
""")

redirect("einsaetze", "../weltkarte/", "Weltkarte")

# Regelwerk: gibt es nicht mehr, die alte Adresse führt zu Bits & Bolts auf der Weltkarte
redirect("regelwerk", "../weltkarte/#bits-and-bolts", "Weltkarte")

# Störungsprotokoll
## Gegner aus Bolt Buddies (core/battle.gd): Schlüssel der Grafik, Name, Art, Rahmenfarbe,
## Leben, Schaden, Tempo, Schrauben, Erfahrung, wann, wo, Verhalten, neu mit 1.0, in Block Invaders
FOES = [
    ("bug", "Bug", "Gegner", "FF5252", 12, 3, 14, 3, 3, "ab Kampf 1", "alle Ebenen",
     "Der häufigste Gegner. Schwach, aber oft in Gruppen. Steht vorn.", False, "Rückt in der Formation vor."),
    ("drone", "Spam-Drohne", "Gegner", "B46CFF", 9, 4, 13, 4, 3, "ab Kampf 2", "alle Ebenen",
     "Fliegt über die vorderen Reihen hinweg und zielt auf den hintersten Roboter.", False, "Fliegt mit und wirft Bomben."),
    ("turret", "Firewall", "Gegner", "FF5252", 12, 8, 8, 6, 6, "ab Kampf 3", "alle Ebenen",
     "Langsam, schießt aber wild und hart auf irgendwen im Team.", False, "Schießt auf zufällige Blöcke."),
    ("worm", "Rostwurm", "Gegner", "D9773A", 34, 7, 7, 6, 6, "ab Kampf 4", "alle Ebenen, im Kabelschacht und in der Kernzone doppelt so oft",
     "Zäh und gepanzert (1 Panzerung). Hält lange durch.", False, "Braucht mehrere Treffer."),
    ("frost", "Frostbug", "Gegner", "4DE8FF", 16, 4, 11, 5, 5, "ab Kampf 21", "Kühlkreislauf (vor allem), Kernzone",
     "Seine Treffer kühlen ab: Wer getroffen wird, ist später wieder dran.", True, ""),
    ("spark", "Wackelkontakt", "Gegner", "FF9A3D", 11, 4, 16, 5, 5, "ab Kampf 11", "Kabelschacht (vor allem), Kühlkreislauf, Kernzone",
     "Schnell und geladen: Wer ihn trifft, bekommt einen Schlag zurück, der tiefer im Schacht stärker wird.", True, ""),
    ("heat", "Überhitzer", "Gegner", "FF5252", 18, 6, 9, 7, 7, "ab Kampf 31", "Kernzone (vor allem)",
     "Strahlt Hitze ab und trifft das ganze Team zugleich, jeden mit 60 % seines Schadens.", True, ""),
    ("boss", "Bluescreen", "Boss", "3B6BFF", 80, 8, 9, 25, 25, "Kampf 5, 10, 15",
     "Mitte von Speicherkeller und Kabelschacht (dort mit Wackelkontakten), Wächter des Speicherkellers, in der Kernzone im Wechsel",
     "Trifft das ganze Team zugleich. Hinterlässt ein seltenes Teil und einen Akku.", False, "Boss-Welle alle 5 Wellen."),
    ("short", "Kurzschluss", "Wächter", "FFB000", 75, 9, 14, 30, 30, "Kampf 20, 25",
     "Wächter des Kabelschachts, Boss in der Mitte des Kühlkreislaufs, in der Kernzone im Wechsel",
     "Schnell, schlägt wild um sich und landet viele Volltreffer (25 %). Kommt mit Wackelkontakt und Spam-Drohne.", True, ""),
    ("chiller", "Kältekern", "Wächter", "4DE8FF", 95, 7, 8, 35, 35, "Kampf 30, 35",
     "Wächter des Kühlkreislaufs, Boss in der Mitte der Kernzone, dort auch im Wechsel",
     "Trifft das ganze Team und kühlt alle zugleich ab. Kommt mit Frostbug und Bug.", True, ""),
]
## Ereignisse aus Bits & Bolts: Name, Roboter, der es mitbringt, Störungscode ohne Roboter, Wirkung
EVENTS = [
    ("Stromausfall", "", "0 V", "Nach einem Countdown erlöschen die Vorgaben. Richtige Ziffern direkt daneben holen sie zurück."),
    ("Überspannung", "", "!! V", "Ein Kurzschluss kostet 2 Ladungen statt 1."),
    ("Wackelkontakt", "", "~ ~", "Immer wieder erlischt eine deiner Ziffern und muss neu eingetragen werden."),
    ("Störsignal", "", "? !", "Immer wieder taucht eine falsche Notiz auf."),
    ("Falsche Vorgabe", "ERROR", "", "Eine Vorgabe zeigt die falsche Ziffer. Wische die andere Ziffer darauf. Wer eine richtige Vorgabe anzweifelt, bekommt einen Kurzschluss."),
    ("Ansteckung", "VIRUS", "", "Bei einem Kurzschluss erlischt auch eine eingetragene Ziffer daneben."),
    ("Zeitdruck", "DAEMON", "", "Wer zu lange nichts Richtiges einträgt, verliert eine Ladung. Jede richtige Ziffer setzt die Uhr zurück."),
    ("Nebel", "MORSE", "", "Klar zu sehen ist nur die Umgebung der zuletzt berührten Zelle."),
]


def foe_sprites():
    """Holt die Gegner-Sprites aus Bolt Buddies (assets/foes, gezeichnet von tools/foe_art.py). Ohne den Ordner bleiben die vorhandenen."""
    src = os.path.join(OUT, "..", "Bolt-Buddies", "assets", "foes")
    if not os.path.isdir(src):
        return
    dst = os.path.join(OUT, "archiv", "stoerungen", "foes")
    os.makedirs(dst, exist_ok=True)
    for key, *_ in FOES:
        shutil.copyfile(os.path.join(src, key + ".png"), os.path.join(dst, key + ".png"))


def foe_card(f):
    key, name, kind, col, hp, atk, speed, bolts, xp, when, where, does, new, invaders = f
    tag = f'<span class="foe-kind">{kind}</span>' + ('<span class="badge badge-plan">neu in 1.0</span>' if new else "")
    stats = "".join(f'<div><dt>{a}</dt><dd>{v}</dd></div>' for a, v in [("Leben", hp), ("Schaden", atk), ("Tempo", speed)])
    inv = f"""
  <section class="bot-game bot-game-plan"{g("plan")}>
    <h4>Block Invaders<span class="bot-role">geplant</span></h4>
    <p>{html.escape(invaders)}</p>
  </section>""" if invaders else ""
    return f"""<li class="bot-card" id="{key}" style="--bot:#{col}"{g("bb plan" if invaders else "bb")}>
  <div class="bot-head">
    <div class="bot-screen"><img class="{'foe-l' if kind != 'Gegner' else 'foe-s'}" src="foes/{key}.png" width="{96 if kind != 'Gegner' else 80}" height="{96 if kind != 'Gegner' else 80}" alt="{name}" loading="lazy"></div>
    <div class="bot-name"><h3>{name}</h3><div class="foe-tags">{tag}</div></div>
  </div>
  <section class="bot-game bot-game-fight"{g("bb")}>
    <h4><img src="../../icons/bolt-buddies.png" alt="" width="20" height="20">Bolt Buddies<span class="bot-role">Schrottschacht</span></h4>
    <p>{html.escape(does)}</p>
    <dl class="foe-stats">{stats}</dl>
    <p class="bot-unlock"><b>{html.escape(when)}</b> · {html.escape(where)}</p>
    <p class="bot-unlock">Beute: {bolts} Schrauben, {xp} Erfahrung</p>
  </section>{inv}
</li>"""


def event_card(e):
    name, bot, code, does = e
    if bot:
        screen = f'<div class="bot-screen" style="--bot:#{COLORS[bot]}"><img src="../roboter/bots/{bot.lower()}.png" width="80" height="96" alt="{bot}" loading="lazy"></div>'
        sub = f'<a class="bot-family" href="../roboter/#{bot.lower()}">bringt {bot} mit</a>'
    else:
        screen = f'<div class="bot-screen event-code" style="--bot:#FFB000"><span>{html.escape(code)}</span></div>'
        sub = '<span class="foe-kind">Ereignis</span>'
    return f"""<li class="bot-card">
  <div class="bot-head">
    {screen}
    <div class="bot-name"><h3>{name}</h3>{sub}</div>
  </div>
  <section class="bot-game bot-game-puzzle">
    <h4><img src="../../icons/bits-and-bolts.png" alt="" width="20" height="20">Bits &amp; Bolts<span class="bot-role">Hauptrechner</span></h4>
    <p>{html.escape(does)}</p>
  </section>
</li>"""


def copy_art():
    """Holt Bilder aus den Spielen, wenn die Ordner daneben liegen, sonst bleiben die vorhandenen.
    Bolt Buddies: Teile und Module (tools/item_art.py), gerenderte Ebenen, Werkstatt und Stationen (tools/archive_art.gd).
    Bits & Bolts: Ausschnitte aus den Store-Screenshots."""
    bb = os.path.join(OUT, "..", "Bolt-Buddies")
    parts = os.path.join(OUT, "archiv", "ersatzteile", "img")
    world = os.path.join(OUT, "archiv", "weltkarte", "img")
    if os.path.isdir(os.path.join(bb, "assets", "items")):
        for folder in ("items", "mods"):
            shutil.copytree(os.path.join(bb, "assets", folder), os.path.join(parts, folder), dirs_exist_ok=True,
                            ignore=shutil.ignore_patterns("*.import"))
    art = os.path.join(bb, "docs", "archive")
    if os.path.isdir(art):
        os.makedirs(parts, exist_ok=True)
        os.makedirs(world, exist_ok=True)
        for name in os.listdir(art):
            dst = world if name.startswith(("layer_", "workshop", "lift")) else parts
            shutil.copyfile(os.path.join(art, name), os.path.join(dst, name))
    shots = os.path.join(OUT, "..", "Bits-and-Bolts", "store", "de", "screenshots")
    if os.path.isdir(shots):
        from PIL import Image
        os.makedirs(world, exist_ok=True)
        # Der obere Teil des Handybilds: Titel und Raster, 16:10 wie die anderen Bilder
        for num, name in (("06", "bnb_etagen"), ("05", "bnb_ereignis"), ("07", "bnb_haupt")):
            im = Image.open(os.path.join(shots, num + ".png")).convert("RGB")
            im = im.crop((40, 330, 1040, 955)).resize((640, 400), Image.LANCZOS)
            im.save(os.path.join(world, name + ".jpg"), quality=82, optimize=True)


copy_art()
foe_sprites()
foe_index = "".join(f'<a href="#{f[0]}" style="--bot:#{f[3]}"><img src="foes/{f[0]}.png" width="40" height="40" alt="" loading="lazy"><span>{f[1]}</span></a>' for f in FOES)
write("stoerungen", head("Archiv · Störungsprotokoll", "Störungsprotokoll",
    "Alles, was im Rechner schiefgehen kann: Gegner, die im Schrottschacht angreifen, und Ereignisse, die Rätsel im Hauptrechner schwerer machen.") + f"""
      <nav class="bot-index foe-index" aria-label="Gegner">{foe_index}</nav>
      <div class="callout wiki-note"{g("bb plan")}>
        <b>So liest du die Karten:</b> Leben, Schaden und Tempo sind Grundwerte. Mit jedem Kampf werden Gegner zäher und stärker, in tieferen Ebenen langsamer,
        dafür macht der erste Kampf jeder Ebene einen Sprung. Je Ebene gibt es die Hälfte mehr Schrauben, im Nebenschacht noch einmal 75 % mehr.
        Der blaue Kasten zeigt, was in Block Invaders geplant ist.
      </div>
      <section class="wiki-sec"{g("bb plan")}>
        <h2>Gegner im Schrottschacht</h2>
        <ul class="bot-grid">
{chr(10).join(foe_card(f) for f in FOES)}
        </ul>
      </section>
      <section class="wiki-sec" id="ereignisse"{g("bnb")}>
        <h2>Ereignisse im Hauptrechner</h2>
        <p>Aus Bits &amp; Bolts. Sie treffen Zwischenrechner, den Hauptrechner und auf hohen Stufen auch normale Rätsel. Vier davon bringen Roboter als Eigenart in jedes Rätsel mit, dafür haben sie mehr Ladung oder Tipps.</p>
        <ul class="bot-grid">
{chr(10).join(event_card(e) for e in EVENTS)}
        </ul>
      </section>
""", "Gegner und Ereignisse im Roboter-Universum: Bug, Spam-Drohne, Firewall, Rostwurm, Frostbug, Wackelkontakt, Überhitzer, die Bosse und acht Störungen.")

# Ersatzteillager: alles, was einen Roboter in Bolt Buddies stark macht, mit Bildern aus dem Spiel.
## Ausrüstung (core/gear.gd): Grafik, Name, Platz, hebt
ITEMS = [("saw", "Kreissäge", "weapon", "Leistung"), ("laser", "Laser", "weapon", "Leistung, Logik"), ("taser", "Taser", "weapon", "Leistung, Takt"),
         ("plate", "Blechpanzer", "armor", "Gehäuse"), ("cooler", "Kühlkörper", "armor", "Gehäuse, Takt"), ("shell", "Gummihülle", "armor", "Gehäuse, Logik"),
         ("ram", "RAM-Riegel", "chip", "Logik"), ("quartz", "Taktquarz", "chip", "Takt"), ("turbo", "Turbolader", "chip", "Leistung, Takt"),
         ("cell", "Zusatzakku", "chip", "Gehäuse, Logik")]
SLOTS = [("weapon", "Waffe"), ("armor", "Rüstung"), ("chip", "Chip")]
## Module (core/battle.gd MODS)
MODS = [("overclock", "Übertakter", "+15 % Tempo"), ("sharp", "Schleifstein", "+20 % Schaden"), ("plating", "Panzerplatten", "+25 % Leben"),
        ("target", "Zielhilfe", "+15 % Volltreffer"), ("ghost", "Tarnlack", "+10 % Ausweichen"), ("spikes", "Stacheln", "2 Schaden an Angreifern"),
        ("leech", "Stromdieb", "heilt sich um 15 % des Schadens"), ("toxin", "Rostspray", "Getroffene rosten: 2 Schaden je Zug"),
        ("armor", "Dickes Blech", "1 Panzerung"), ("nano", "Nanobots", "heilt 2 Leben je Zug")]
## Shop (autoload/game.gd PRICES): Symbol, Name, Preis, was man bekommt
SHOP = [("akku", "Akku", "12 Schrauben", "+35 Energie"), ("oil", "Ölkanne", "10 Schrauben", "+40 Pflege, +5 Laune"),
        ("armor", "Schrottkiste", "30 Schrauben", "ein zufälliges Teil, je tiefer der Rekord, desto besser"),
        ("capsule", "Tresorkiste", "260 Schrauben", "ein Teil, mindestens selten"),
        ("chip", "Trainingsdaten", "40 Schrauben, je Stufe 14 mehr", "eine halbe Stufe Erfahrung für den gewählten Roboter, bis Stufe 20")]
## Stationen (core/base.gd): Bild, Name, Stufe 1 / 2 / 3, Preise, wie sie in der Werkstatt aussieht
STATIONS = [
    ("dock", "Ladeleiste", "Schlafende laden 35 / 70 / 100 % schneller", "60 / 180 / 450", "Schlafende stehen auf der Leiste, ihr Steckplatz leuchtet. Jede Stufe bringt mehr Kabel."),
    ("bath", "Ölbad", "Pflege sinkt 15 / 30 / 45 % langsamer", "60 / 180 / 450", "Eine Wanne mit schwappendem Öl und Blasen. Auf Stufe 3 glüht eine Heizspirale."),
    ("play", "Spielecke", "Laune sinkt 15 / 30 / 45 % langsamer", "60 / 180 / 450", "Ein Teppich mit Bauklötzen, ab Stufe 2 mit Ball, ab Stufe 3 mit Kreisel."),
    ("bench", "Werkbank", "zerlegen und aufwerten / 25 % / 50 % günstiger", "80 / 200 / 450", "Mit Schraubstock, ab Stufe 2 mit Lampe, ab Stufe 3 mit Bohrmaschine, die Funken sprüht."),
    ("radio", "Funkantenne", "empfängt Post aus den anderen Spielen", "kommt später", 'Steht auf dem Regal und blinkt, siehe <a href="../funk/">Funkverbindung</a>.'),
]


def part_card(img, name, sub, text, cls="part"):
    return f"""          <li class="{cls}"><img src="img/{img}" alt="" loading="lazy"><div><h3>{name}</h3><p class="game-genre">{sub}</p><p>{text}</p></div></li>"""


items_html = ""
for slot, slot_name in SLOTS:
    cards = "\n".join(part_card(f"items/{k}.png", n, slot_name, f"hebt {h}") for k, n, s, h in ITEMS if s == slot)
    items_html += f"""        <h3 class="wiki-sub part-head"><img src="img/pix_{'weapon' if slot == 'weapon' else slot}.png" alt="">{slot_name}</h3>
        <ul class="part-grid">
{cards}
        </ul>
"""
mods_html = "\n".join(part_card(f"mods/{k}.png", n, "Modul", w, "part part-small") for k, n, w in MODS)
shop_html = "\n".join(part_card(f"pix_{k}.png", n, p, w, "part part-small") for k, n, p, w in SHOP)
stations_html = "\n".join(f"""          <li class="station"><img src="img/station_{k}.png" alt="{n}" loading="lazy"><div class="place-head"><h3>{n}</h3>{PLAN if k == "radio" else ""}</div>
            <p class="game-genre">{p} Schrauben</p><p><b>{e}</b></p><p>{look}</p></li>""" for k, n, e, p, look in STATIONS)

write("ersatzteile", head("Archiv · Ersatzteillager", "Ersatzteillager",
    "Was einen Roboter in Bolt Buddies stark macht: vier Attribute, drei Ausrüstungsplätze, Module für eine Expedition, Vorräte aus dem Shop "
    "und eine gut ausgebaute Werkstatt. Alle Bilder stammen direkt aus dem Spiel.") + f"""
      <section class="wiki-sec"{g("bb")}>
        <h2>Attribute</h2>
        {table(["Attribut", "Wirkt auf", "Soll später kommen aus"], [
            ["<b>Leistung</b>", "mehr Schaden", "Block Invaders"],
            ["<b>Takt</b>", "öfter dran, weicht aus", "Loop Runner"],
            ["<b>Logik</b>", "mehr Volltreffer", "Bits &amp; Bolts"],
            ["<b>Gehäuse</b>", "mehr Leben", "Kippwelt"]])}
      </section>
      <section class="wiki-sec"{g("bb")}>
        <h2>Ausrüstung</h2>
        <p>Jeder Roboter hat drei Plätze: Waffe, Rüstung und Chip. Teile gibt es im Schacht, aus Kisten im Shop und als Belohnung im Tagesschacht. Überzählige Teile lassen sich verkaufen oder an der Werkbank zerlegen.</p>
{items_html}        <p>Jedes Teil hat eine von vier Seltenheiten. Je seltener, desto mehr Punkte bringt es, und tiefer im Schacht wird es öfter selten:</p>
        <p class="rarity"><span class="r0">Schrott</span><span class="r1">solide</span><span class="r2">selten</span><span class="r3">legendär</span></p>
      </section>
      <section class="wiki-sec"{g("bb")}>
        <h2>Module</h2>
        <p>Nach jedem gewonnenen Kampf darf man eine Belohnung wählen. Ein Modul gilt für das ganze Team bis zum Ende der Expedition, gleiche Module stapeln sich.</p>
        <ul class="part-grid">
{mods_html}
        </ul>
      </section>
      <section class="wiki-sec" id="shop"{g("bb")}>
        <h2>Shop und Vorräte</h2>
        <p>Im Shop gibt es Vorräte für die Pflege und Kisten mit Ausrüstung. Trainingsdaten und Tresorkisten bleiben auch nach dem vollen Ausbau ein Ziel für Schrauben.</p>
        <ul class="part-grid">
{shop_html}
        </ul>
      </section>
      <section class="wiki-sec"{g("bb")}>
        <h2>Pflege</h2>
        {table(["Wert", "sinkt", "steigt durch", "Im Kampf"], [
            ["<b>Energie</b>", "1 Punkt in 6 Minuten", "Akku (+35), Schlafen", "ab 70: +10 % Leben · unter 30: −20 % Leben"],
            ["<b>Laune</b>", "1 Punkt in 5 Minuten, rostig doppelt so schnell", "Spielen (+18), Streicheln, Expedition", "ab 70: +10 % Volltreffer · unter 30: −20 % Schaden"],
            ["<b>Pflege</b>", "1 Punkt in 8 Minuten", "Ölkanne (+40)", "ab 70: +10 % Ausweichen · unter 30: −20 % Tempo"]])}
        <p>Werte sinken auch, wenn das Spiel zu ist, höchstens für 48 Stunden. Kaputt geht dabei nichts: Ein leerer Roboter schaltet ab und lädt an der Ladeleiste.</p>
      </section>
      <section class="wiki-sec" id="ausbau"{g("bb")}>
        <h2>Werkstatt-Ausbau</h2>
        <p>Kommt mit Bolt Buddies 1.0. Jede Station wird für Schrauben in drei Stufen ausgebaut und steht dann sichtbar in der Werkstatt, mit jeder Stufe größer. Sie machen die Pflege leichter, aber nie überflüssig: Auch ganz ausgebaut braucht ein Roboter nach zwei Tagen wieder etwas. Die Bilder zeigen Stufe 3.</p>
        <ul class="station-grid">
{stations_html}
        </ul>
        <p>Alles zusammen kostet 2830 Schrauben. Eine Expedition bringt je nach Stufe des Teams etwa 30 bis 290, für die erste Station reichen zwei frühe Expeditionen.</p>
      </section>
      <section class="wiki-sec" id="werkbank"{g("bb")}>
        <h2>Werkbank</h2>
        <p>An der Werkbank wird aus altem Kram ein Lieblingsteil. Zerlegen macht aus einem Teil im Lager Schrott. Aufwerten hebt ein Teil eine Seltenheit höher und gibt ihm 2 Punkte dazu, auch wenn es gerade ein Roboter trägt.</p>
        {table(["Seltenheit", "Schrott beim Zerlegen", "Aufwerten zur nächsten"], [
            ["<b>Schrott</b>", "1", "20 Schrauben, 3 Schrott"],
            ["<b>solide</b>", "3", "50 Schrauben, 6 Schrott"],
            ["<b>selten</b>", "5", "120 Schrauben, 12 Schrott"],
            ["<b>legendär</b>", "7", "geht nicht höher"]])}
      </section>
      <section class="wiki-sec"{g("bb")}>
        <h2>Schrauben und Schrott</h2>
        <ul class="part-grid">
{part_card("pix_bolts.png", "Schrauben", "Währung", "Gibt es im Schacht und für verkaufte Teile. Jede Ebene bringt die Hälfte mehr als die darüber, der Nebenschacht noch einmal 75 % mehr.", "part part-small")}
{part_card("pix_scrap.png", "Schrott", "nur an der Werkbank", "Entsteht beim Zerlegen und wird zum Aufwerten gebraucht.", "part part-small")}
        </ul>
      </section>
""", "Ausrüstung, Module, Shop, Pflegewerte und Werkstatt-Stationen der Roboter in Bolt Buddies, mit Bildern aus dem Spiel.")

# Funkverbindung
write("funk", head("Archiv · Funkverbindung", "Funkverbindung",
    "Geplant: Die Spiele sollen sich später auf deinem Handy gegenseitig Bescheid geben. Was ein Roboter in einem Spiel erlebt, macht ihn dann in Bolt Buddies stärker.") + f"""
      <div class="callout wiki-note"><b>Noch nicht verfügbar.</b> Diese Seite beschreibt den Plan. Die Spiele funktionieren schon jetzt jedes für sich.</div>
      <section class="wiki-sec">
        <h2>Wer funkt was</h2>
        {table(["Spiel", "Funkt an Bolt Buddies"], [
            ["<b>Bits &amp; Bolts</b>", "Erfahrung und Logik für den gespielten Roboter"],
            ["<b>Block Invaders</b>", "Erfahrung, Leistung, Waffen-Teile"],
            ["<b>Loop Runner</b>", "Erfahrung und Takt"],
            ["<b>Kippwelt</b>", "Erfahrung, Gehäuse, Rüstungsteile"],
            ["<b>Zündkette</b>", "Erfahrung, Schrottkisten"],
            ["<b>Snake Jam</b>", "Akkus, Öl, Schrauben"]], "", ["bnb", "plan", "plan", "plan", "plan", "plan"])}
        <p>Zurück funkt Bolt Buddies, welche Roboter schon gerettet sind. Die können dann auch in den anderen Spielen mitmachen.</p>
      </section>
      <section class="wiki-sec">
        <h2>Was dabei gilt</h2>
        <ul class="plain-list">
          <li><b>Jedes Spiel geht auch allein.</b> Wer nur ein Spiel hat, verpasst nichts Wichtiges.</li>
          <li><b>Kein Vorteil, der ein Rätsel löst.</b> In die Rätselspiele kommen nur Roboter, Aussehen und höchstens kleine Hilfen.</li>
          <li><b>Eine Obergrenze pro Tag.</b> Kein einzelnes Spiel levelt alle Roboter auf einmal hoch.</li>
          <li><b>Post in der Werkstatt.</b> Kommt ein Bericht an, sieht man es in Bolt Buddies: „BYTE kommt aus dem Hauptrechner zurück, +40 Erfahrung“.</li>
        </ul>
      </section>
      <section class="wiki-sec">
        <h2>Deine Daten</h2>
        <p>Die Verbindung soll nur auf deinem Gerät laufen: ohne Server, ohne Konto, ohne Internet. Nur meine eigenen Spiele dürfen sich gegenseitig Berichte schicken, andere Apps werden abgewiesen. Sobald das fertig ist, steht es auch in den Datenschutzerklärungen der Spiele.</p>
      </section>
""", "Geplante Verbindung der Spiele im Roboter-Universum: Wie Roboter in einem Spiel stärker werden, wenn man mit ihnen in einem anderen spielt.")

print("ok")
