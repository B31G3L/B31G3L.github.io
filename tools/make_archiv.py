# Erzeugt die Archiv-Seiten (Wiki zum Roboter-Universum) für B31G3L.github.io.
# Aufruf aus dem Repo: python tools/make_archiv.py
import os, sys, html, shutil

OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
STAND = "13.11.2026"

PAGES = [  # slug, Titel im Menü, Untertitel
    ("", "Das Archiv", "Übersicht"),
    ("roboter", "Roboter-Register", "Alle 22 Roboter"),
    ("stoerungen", "Störungsprotokoll", "Gegner und Ereignisse"),
    ("einsaetze", "Einsatzorte", "Die Spiele"),
    ("weltkarte", "Weltkarte", "Orte der Welt"),
    ("regelwerk", "Regelwerk", "Binär-Rätsel"),
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

def write(slug, body, desc):
    d = os.path.join(OUT, "archiv", slug) if slug else os.path.join(OUT, "archiv")
    os.makedirs(d, exist_ok=True)
    with open(os.path.join(d, "index.html"), "w", encoding="utf-8", newline="\n") as f:
        f.write(page(slug, body, desc))

def head(eyebrow, title, lead):
    return f"""      <p class="eyebrow">{eyebrow}</p>
      <h1 class="page-title">{title}</h1>
      <p class="wiki-lead">{lead}</p>
"""

def table(cols, rows, cls=""):
    th = "".join(f"<th>{c}</th>" for c in cols)
    trs = "\n".join("<tr>" + "".join(f"<td>{c}</td>" for c in r) + "</tr>" for r in rows)
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
    hero = f'<p class="bot-hero">Held in {html.escape(HERO[b])}</p>' if b in HERO and "geplant" in HERO[b] else ""
    return f"""<li class="bot-card" id="{b.lower()}" style="--bot:#{COLORS[b]}">
  <div class="bot-head">
    <div class="bot-screen"><img src="bots/{b.lower()}.png" width="80" height="96" alt="{b}" loading="lazy"></div>
    <div class="bot-name"><h3>{b}</h3><span class="bot-say">„{html.escape(SAYS[b])}“</span><a class="bot-family" href="#familien">Familie: {FAMILY[b]}</a>{hero}</div>
  </div>
  <section class="bot-game bot-game-puzzle">
    <h4><img src="../../icons/bits-and-bolts.png" alt="" width="20" height="20">Bits &amp; Bolts<span class="bot-role">{ROLE[b]}</span></h4>
    <p>{html.escape(PUZZLE[b])}</p>
    <p class="bot-unlock">Freigeschaltet {unlock}</p>
  </section>
  <section class="bot-game bot-game-fight">
    <h4><img src="../../icons/bolt-buddies.png" alt="" width="20" height="20">Bolt Buddies<span class="bot-role">Kampf</span></h4>
    <p><b>Eigenheit:</b> {html.escape(TRAIT[b])}</p>
    <dl class="bot-stats">{stats}</dl>
  </section>
</li>"""

# ── Seiten ───────────────────────────────────────────────────────────────────

# Übersicht
links = "\n".join(
    f'<li class="app-card"><a class="wiki-card-link" href="{s}/"><h3 class="app-title">{t}</h3><p class="app-desc">{d}</p></a></li>'
    for s, t, d in [
        ("roboter", "Roboter-Register", "Alle 22 Roboter mit Rätselfähigkeit, Kampfwerten, Eigenheit und Spruch."),
        ("stoerungen", "Störungsprotokoll", "Alle Gegner mit Sprite, Werten und Beute, dazu die Ereignisse im Hauptrechner."),
        ("einsaetze", "Einsatzorte", "Die Spiele des Universums: was man dort tut und was es den Robotern bringt."),
        ("weltkarte", "Weltkarte", "Hauptrechner, Werkstatt, Schrottschacht und die Orte, die noch kommen."),
        ("regelwerk", "Regelwerk", "Die Binär-Regeln aus Bits & Bolts, alle Zusatzregeln und die Schwierigkeitsstufen."),
        ("ersatzteile", "Ersatzteillager", "Attribute, Ausrüstung, Seltenheiten, Module und Vorräte."),
        ("funk", "Funkverbindung", "Wie die Spiele später miteinander reden, damit Roboter überall stärker werden."),
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
            ["Gegner", "Bug, Spam-Drohne, Firewall, Rostwurm, Bluescreen"],
            ["Ereignisse", "8 Störungen im Hauptrechner, von Stromausfall bis Nebel"],
            ["Währung", "Schrauben und Schrott in der Werkstatt"],
        ], " wiki-table-plain")}
      </section>
""", "Das Archiv der Roboter: Wiki zu Bits & Bolts, Bolt Buddies und allen Spielen im Roboter-Universum von B31G3L.")

# Roboter
cards = "\n".join(bot_card(b) for b in ORDER)
index = "".join(f'<a href="#{b.lower()}" style="--bot:#{COLORS[b]}"><img src="bots/{b.lower()}.png" width="40" height="48" alt="" loading="lazy"><span>{b}</span></a>' for b in ORDER)
assert sorted(FAMILY) == sorted(ORDER), "jeder Roboter braucht genau eine Familie"
copy_sprites()
write("roboter", head("Archiv · Roboter-Register", "Roboter-Register",
    "Alle 22 Roboter in der Reihenfolge, in der man sie in Bits &amp; Bolts freischaltet. Jeder bringt ins Rätsel eine eigene Fähigkeit mit und hat in Bolt Buddies eigene Kampfwerte.") + f"""
      <nav class="bot-index" aria-label="Roboter">{index}</nav>
      <div class="callout wiki-note">
        <b>So liest du die Karten:</b> Jede Karte zeigt, was der Roboter in beiden Spielen kann: oben in Bits &amp; Bolts, unten in Bolt Buddies. Die Punkte sind die Grundwerte auf Stufe 1, zusammen immer 12. Je Stufe wächst jedes Attribut um 12 % seines Grundwerts, höchstens bis Stufe 20.
        In Bolt Buddies findet man neue Roboter im Schrottschacht, nach Kampf 2, 5, 8 und so weiter.
      </div>
      <ul class="bot-grid">
{cards}
      </ul>
      <section class="wiki-sec" id="familien" style="margin-top:40px">
        <h2>Familien <span class="badge badge-plan">Geplant</span></h2>
        <p>Geplant für Bolt Buddies 1.1: Zwei Roboter derselben Familie im Team geben einen kleinen Bonus, drei einen größeren.</p>
        {table(["Familie", "Roboter", "Bonus"], [[f"<b>{name}</b>", " ".join(f'<a class="fam-bot" href="#{m.lower()}" style="--bot:#{COLORS[m]}"><img src="bots/{m.lower()}.png" width="20" height="24" alt="">{m}</a>' for m in members), bonus] for name, bonus, members in FAMILIES])}
      </section>
""", "Alle 22 Roboter aus Bits & Bolts und Bolt Buddies: Rätselfähigkeit, Freischaltung, Kampfwerte und Eigenheit.")

# Einsatzorte
def game(id_, name, status, genre, what, gives, bots, extra=""):
    return f"""      <section class="wiki-sec game" id="{id_}">
        <div class="game-head"><h2>{name}</h2>{status}</div>
        <p class="game-genre">{genre}</p>
        <p>{what}</p>
        <dl class="app-meta game-meta">
          <div><dt>Helden</dt><dd>{bots}</dd></div>
          <div><dt>Bringt</dt><dd>{gives}</dd></div>
        </dl>
{extra}      </section>
"""
write("einsaetze", head("Archiv · Einsatzorte", "Einsatzorte",
    "Jedes Spiel ist ein eigener Einsatz in derselben Welt. Bolt Buddies ist die Heimat, in der die Roboter wohnen. Die anderen Spiele schicken sie später mit Erfahrung und Beute dorthin zurück, siehe <a href=\"../funk/\">Funkverbindung</a>.") +
    game("bits-and-bolts", "Bits &amp; Bolts", STORE, "Binär-Rätsel als Roguelite",
         "Ein Roboter arbeitet sich durch zehn Stationen bis zum Hauptrechner und repariert unterwegs durchgebrannte Raster aus Nullen und Einsen. Jede falsche Ziffer ist ein Kurzschluss und kostet Ladung. Siege schalten neue Roboter und höhere Schwierigkeitsstufen frei.",
         "Logik", "Alle 22 Roboter, als Erster BYTE",
         '        <p><a href="../regelwerk/">Zum Regelwerk →</a> · <a href="https://play.google.com/store/apps/details?id=com.beigel.bitsandbolts" target="_blank" rel="noopener">Play Store ↗</a> · <a href="../../bits-and-bolts/">Datenschutz</a></p>\n') +
    game("bolt-buddies", "Bolt Buddies", LIVE, "Roboter pflegen und Auto-Kämpfe",
         "Die Werkstatt ist das Zuhause aller geretteten Roboter. Sie brauchen Akku, Öl und Aufmerksamkeit. Ein Team aus bis zu drei Robotern zieht in den Schrottschacht, kämpft dort von selbst und bringt Schrauben, Ausrüstung und neue Freunde mit.",
         "Heimat aller Roboter: Stufen, Ausrüstung, Pflege", "Alle 22 Roboter, als Erster BYTE",
         '        <h3 class="wiki-sub">Was noch kommt</h3>\n'
         + table(["Feature", "Worum es geht", "Version"], [
             ["<b>Schacht-Ebenen</b>", 'Umgesetzt: Alle 10 Kämpfe eine neue Ebene mit eigenen Gegnern und eigenem Wächter, dazu Haltestellen zum Direkteinstieg. Siehe <a href="../weltkarte/#ebenen">Weltkarte</a>.', "1.0"],
             ["<b>Werkstatt-Ausbau</b>", 'Umgesetzt: Ladeleiste, Ölbad, Spielecke und Werkbank in drei Stufen für Schrauben, die Funkantenne folgt mit dem Funk. Siehe <a href="../ersatzteile/#ausbau">Ersatzteillager</a>.', "1.0"],
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
         + '        <p><a href="../ersatzteile/">Zum Ersatzteillager →</a> · <a href="../../bolt-buddies/">Datenschutz</a></p>\n') +
    game("block-invaders", "Block Invaders", PLAN, "Block-Puzzle gegen angreifende Störungen",
         "Bugs, Spam-Drohnen, Firewalls und Rostwürmer rücken auf die Werkstatt vor. Volle Reihen feuern Salven, volle Spalten Laser. Jede fünfte Welle bringt einen Bluescreen. Der gewählte Roboter steht als Geschütz unten und feuert mit seiner Eigenheit, zum Beispiel trifft OKTA die ganze Reihe.",
         "Leistung, Waffen-Teile", "Wählbar, je nach Eigenheit") +
    game("loop-runner", "Loop Runner", PLAN, "Zeitschleifen-Plattformer",
         "LOOP hat 20 Sekunden und sich selbst als Team: Jede Schleife wird aufgezeichnet und läuft in der nächsten als Kopie mit. Zusammen halten sie Türen offen, graben Fallen und sammeln Bits, während Wachbots patrouillieren.",
         "Takt", "LOOP, später SHIFT und QUBIT") +
    game("kippwelt", "Kippwelt", PLAN, "Plattformer ohne Springen",
         "Im Schwerkraft-Labor dreht der Roboter die ganze Welt um 90 Grad, und alles Lose fällt nach unten. Erst den Zugangschip holen, dann zum Ausgang. Kisten zerquetschen Gegner, Stacheln sind gefährlich.",
         "Gehäuse, Rüstungsteile", "GATE oder ROOT, beide halten viel aus") +
    game("zuendkette", "Zündkette", PLAN, "Kettenreaktions-Rätsel",
         "Ein einziger Überspannungsimpuls muss alle Viren erwischen. Kondensatoren geben die Ladung weiter, Schrottkisten brennen weg, Steine halten auf. Gesucht ist der eine Platz, von dem aus die Kette alles erreicht, nur den Roboter nicht.",
         "Schrottkisten mit zufälliger Ausrüstung", "ERROR oder GLITCH") +
    game("snake-jam", "Snake Jam", PLAN, "Schiebe-Rätsel mit wachsenden Bussen",
         "Auf dem Datenbus-Depot müssen bunte Datenbusse ihre Pakete einsammeln und zum Port hinausfahren. Jedes Paket macht den Bus länger, und lange Busse stehen sich selbst im Weg.",
         "Vorräte: Akkus, Öl, Schrauben", "Noch offen, eventuell bleibt das Spiel eigenständig"),
    "Die Spiele im Roboter-Universum: Bits & Bolts, Bolt Buddies und die geplanten Einsätze Block Invaders, Loop Runner, Kippwelt, Zündkette und Snake Jam.")

# Weltkarte
def place(name, game_, text, status=""):
    return f"""        <li class="place"><div class="place-head"><h3>{name}</h3>{status}</div><p class="game-genre">{game_}</p><p>{text}</p></li>"""
write("weltkarte", head("Archiv · Weltkarte", "Weltkarte",
    "Alle Orte liegen im selben alten Rechner: oben die Etagen bis zum Hauptrechner, unten der Schrottschacht, dazwischen die Werkstatt.") + f"""
      <section class="wiki-sec">
        <h2>Bekannte Orte</h2>
        <ul class="place-list">
{place("Die Etagen", "Bits &amp; Bolts", "Der Weg zum Hauptrechner führt über zehn Stationen: sieben Rätsel und zwei Zwischenrechner an Station 4 und 7. Auf höheren Stufen treten unterwegs Ereignisse auf.")}
{place("Zwischenrechner", "Bits &amp; Bolts", "Hier gelten verschärfte Bedingungen, ab Stufe 1 mit einem Ereignis.")}
{place("Hauptrechner", "Bits &amp; Bolts", "Das Ziel jedes Runs. Er besteht aus bis zu vier Sektoren: den äußeren Leitungen unter Spannung, einem Sektor mit Stromausfall, dem inneren Ring unter Überspannung und dem Kern in 8×8. Nach jedem Sektor gibt es eine Ladung zurück.")}
{place("Die Werkstatt", "Bolt Buddies", "Hier wohnen alle geretteten Roboter. Sie laufen frei herum, wollen gestreichelt, geölt und geladen werden und schlafen an der Ladeleiste, wenn der Akku leer ist.")}
{place("Der Schrottschacht", "Bolt Buddies", "Unter der Werkstatt geht es Kampf für Kampf tiefer. Dort liegen Schrauben, Akkus, Öl und Ausrüstung, und abgeschaltete Roboter warten auf Rettung.")}
{place("Der Aufzug", "Bolt Buddies", "Nach jedem Kampf im Schacht: weiter nach unten oder mit der ganzen Beute nach Hause. Fällt das ganze Team aus, bleibt beim Abschleppen die halbe Beute liegen.")}
        </ul>
      </section>
      <section class="wiki-sec" id="ebenen">
        <h2>Die Ebenen des Schrottschachts</h2>
        <p>Kommt mit Bolt Buddies 1.0: Alle 10 Kämpfe beginnt eine neue Ebene, im letzten Kampf wartet ihr Wächter. Wer ihn besiegt, kann künftig an der Haltestelle der nächsten Ebene einsteigen und bekommt dafür von der Werkstatt Module mit.</p>
        <ul class="place-list">
{place("Speicherkeller", "Kampf 1–10 · Wächter: Bluescreen", "Bugs, Spam-Drohnen, Firewalls und Rostwürmer zwischen alten Speicherriegeln. Hier beginnt jede neue Werkstatt.", PLAN)}
{place("Kabelschacht", "Kampf 11–20 · Wächter: Kurzschluss", "Enge Gänge voller Leitungen, der Boden schimmert kupfern. Firewalls und Rostwürmer tauchen hier doppelt so oft auf.", PLAN)}
{place("Kühlkreislauf", "Kampf 21–30 · Wächter: Kältekern", "Kalt, nass und eisblau. Hier leben Frostbugs, deren Treffer die Roboter abkühlen.", PLAN)}
{place("Kernzone", "ab Kampf 31 · Wächter wechseln", "Der rote Kern des Rechners. Alle Gegner gemischt, die drei Wächter wechseln sich ab, und es geht endlos weiter.", PLAN)}
        </ul>
      </section>
      <section class="wiki-sec">
        <h2>Orte, die noch kommen</h2>
        <ul class="place-list">
{place("Die Abwehrstellung", "Block Invaders", "Der Rand der Werkstatt, an dem Störungen in Formation anrücken.", PLAN)}
{place("Das Schleifenlabor", "Loop Runner", "Ein Labor, in dem die Zeit alle 20 Sekunden von vorn beginnt.", PLAN)}
{place("Das Schwerkraft-Labor", "Kippwelt", "Räume, die sich drehen lassen. Unten ist immer da, wo gerade unten ist.", PLAN)}
{place("Das Kondensatorlager", "Zündkette", "Voller Kondensatoren und Schrottkisten, in denen sich Viren verstecken.", PLAN)}
{place("Das Datenbus-Depot", "Snake Jam", "Ein voller Parkplatz für Datenbusse, nur eine Ausfahrt zum Port.", PLAN)}
        </ul>
      </section>
""", "Die Orte im Roboter-Universum: Etagen und Hauptrechner, Werkstatt, Schrottschacht und die geplanten Einsatzorte.")

# Regelwerk
RULES = [
    ("Zeichen", "GATE", "= heißt gleich, × heißt verschieden."),
    ("Block", "PARI", "In jedem umrandeten Block stehen gleich viele Nullen und Einsen."),
    ("Schleife", "LOOP", "Das Ende einer Linie grenzt an ihren Anfang: Auch über den Rand hinweg stehen nie drei gleiche zusammen."),
    ("Summe", "NIBBLE", "Ein Rahmen umfasst vier Zellen einer Linie. Die Zahl am Rahmen sagt, wie viele Einsen darin stehen."),
    ("Paare", "QUBIT", "Zwei Zellen mit demselben Buchstaben sind verschränkt: Genau eine von ihnen ist 1, die andere 0."),
    ("Diagonale", "ROOT", "Nie drei gleiche gilt auch schräg."),
    ("Oktal", "OKTA", "Jede Oktalziffer steht für drei Bits: 4, 2, 1. ? heißt: Diese Ziffer bleibt offen."),
    ("Hex", "HEXA", "Jede Hexziffer steht für vier Bits: 8, 4, 2, 1. A bis F sind 10 bis 15."),
    ("ASCII", "ASKI", "Das Zeichen neben einer Zeile ist die ganze Zeile in Bits. Seinen Wert findest du in der ASCII-Tabelle."),
    ("Farbe", "CHROMA", "Drei Balken für Rot, Grün und Blau. Jede Höhe von 0 bis 3 steht für zwei Bits."),
    ("Pixel", "PIXA", "Die Blöcke an einer Linie zeigen, wie ihre Einsen zusammenstehen, aber nicht wo."),
    ("Nullstelle", "NULL", "Die Zahl zählt vom Hinweis aus bis zur ersten 0, davor stehen nur Einsen."),
    ("Spiegel", "MIRA", "Die Klammer verbindet zwei Linien, die Spiegelbilder sind."),
    ("Schieben", "SHIFT", "Die Linie mit dem Pfeil ist ihre Nachbarin, um eine Stelle geschoben. Was herausfällt, kommt vorn wieder herein."),
    ("XOR", "XOR", "Die Zahl sagt, an wie vielen Stellen sich zwei Nachbarlinien unterscheiden."),
    ("Glitch", "GLITCH", "Neben der Linie flackern zwei Dezimalzahlen, nur eine ist die Linie in Binär."),
    ("Sensor", "ab Stufe 2", "Die kleine Zahl in einer Zelle zählt die Einsen direkt darüber, darunter, links und rechts."),
    ("Einzigartig", "ab Stufe 3", "Keine zwei Zeilen und keine zwei Spalten sind gleich."),
]
LEVELS = [
    ("0", "nur 6×6, leichtere Rätsel, 1 Regel je Rätsel, keine Ereignisse"),
    ("1", "1 Tipp weniger, bis 2 Regeln je Rätsel, 1 Ereignis bei Rechnern"),
    ("2", "Rätsel ohne Erleichterung, Sensoren"),
    ("3", "Ereignisse ab Etage 5, bis 3 Regeln, Einzigartig, 2 Ereignisse im Hauptrechner"),
    ("4", "8×8 ab Etage 7, Hauptrechner in 8×8, 1 Ladung weniger"),
    ("5", "schwerere Rätsel, 8×8 ab Etage 4, Ereignisse ab Etage 3, bis 4 Regeln, noch 1 Tipp weniger"),
]
TECH = [("Zwilling", "Zwei gleiche nebeneinander: Die Zellen davor und danach bekommen die andere Ziffer."),
        ("Lücke", "Zwei gleiche mit einer Zelle dazwischen: Die Lücke bekommt die andere Ziffer."),
        ("Abzählen", "Hat eine Linie schon alle Nullen oder alle Einsen, ist der Rest klar."),
        ("Durchdenken", "Eine Ziffer probeweise annehmen. Führt sie zu einem Widerspruch, gilt die andere."),
        ("Hinweis übersetzen", "Hex, Oktal, ASCII oder Farbe in Bits umrechnen und eintragen.")]
write("regelwerk", head("Archiv · Regelwerk", "Regelwerk",
    "Die Regeln der Raster aus Bits &amp; Bolts. Drei gelten immer, alle anderen nur, wenn ein Rätsel sie ausdrücklich zeigt.") + f"""
      <section class="wiki-sec">
        <h2>Grundregeln</h2>
        <ol class="rule-list">
          <li>Jede Zelle bekommt eine 0 oder eine 1.</li>
          <li>Nie drei gleiche Ziffern direkt nebeneinander oder untereinander.</li>
          <li>Jede Zeile und jede Spalte hat gleich viele Nullen und Einsen.</li>
        </ol>
        <p class="muted-small">Bedienung: nach oben wischen setzt eine 1, nach unten eine 0, Tippen setzt eine Notiz.</p>
      </section>
      <section class="wiki-sec">
        <h2>Zusatzregeln und Hinweise</h2>
        <p>Die meisten Zusatzregeln gehören zu einem Roboter. Er bringt sie mit, wenn er im Run dabei ist, und erklärt sie beim ersten Mal in einem Probespiel.</p>
        {table(["Regel", "Von", "Bedeutung"], [[f"<b>{n}</b>", (f'<a href="../roboter/#{o.lower()}">{o}</a>' if o.isupper() else o), d] for n, o, d in RULES])}
      </section>
      <section class="wiki-sec">
        <h2>Werkzeugkasten</h2>
        <p>Diese Denkschritte nennt BYTE, wenn er einen Tipp gibt.</p>
        {table(["Schritt", "So geht's"], [[f"<b>{n}</b>", d] for n, d in TECH])}
      </section>
      <section class="wiki-sec">
        <h2>Schwierigkeitsstufen</h2>
        <p>Ein Sieg auf einer Stufe öffnet die nächste. Jede Stufe behält alles von den Stufen darunter.</p>
        {table(["Stufe", "Was dazukommt"], [[f"<b>{n}</b>", d] for n, d in LEVELS])}
      </section>
      <section class="wiki-sec">
        <h2>Ladung, Tipps und Bits</h2>
        <ul class="plain-list">
          <li><b>Ladung:</b> Ein Roboter startet mit 5 Ladungen, je nach Roboter mehr oder weniger. Jede falsche Ziffer ist ein Kurzschluss und kostet eine. Ist der Akku leer, ist der Run vorbei.</li>
          <li><b>Tipps:</b> Jeder Roboter hat eine feste Zahl an Tipps, meist 3. Ein Tipp erklärt den nächsten Denkschritt, statt die Lösung zu verraten.</li>
          <li><b>Seed:</b> Alles hängt am Seed des Runs. Ein fortgesetzter Run hat dieselben Rätsel und denselben Stand.</li>
        </ul>
      </section>
""", "Regelwerk der Binär-Rätsel aus Bits & Bolts: Grundregeln, 18 Zusatzregeln, Lösungsschritte und Schwierigkeitsstufen.")

# Störungsprotokoll
## Gegner aus Bolt Buddies (core/battle.gd): Schlüssel der Grafik, Name, Art, Rahmenfarbe,
## Leben, Schaden, Tempo, Schrauben, Erfahrung, wann, wo, Verhalten, neu mit 1.0, in Block Invaders
FOES = [
    ("bug", "Bug", "Gegner", "FF5252", 12, 3, 14, 3, 3, "ab Kampf 1", "alle Ebenen",
     "Der häufigste Gegner. Schwach, aber oft in Gruppen. Steht vorn.", False, "Rückt in der Formation vor."),
    ("drone", "Spam-Drohne", "Gegner", "B46CFF", 9, 4, 13, 4, 3, "ab Kampf 2", "alle Ebenen",
     "Fliegt über die vorderen Reihen hinweg und zielt auf den hintersten Roboter.", False, "Fliegt mit und wirft Bomben."),
    ("turret", "Firewall", "Gegner", "FF5252", 12, 8, 8, 6, 6, "ab Kampf 3", "alle Ebenen, im Kabelschacht doppelt so oft",
     "Langsam, schießt aber wild und hart auf irgendwen im Team.", False, "Schießt auf zufällige Blöcke."),
    ("worm", "Rostwurm", "Gegner", "D9773A", 34, 7, 7, 6, 6, "ab Kampf 4", "alle Ebenen, im Kabelschacht doppelt so oft",
     "Zäh und gepanzert (1 Panzerung). Hält lange durch.", False, "Braucht mehrere Treffer."),
    ("frost", "Frostbug", "Gegner", "4DE8FF", 16, 4, 11, 5, 5, "ab Kampf 21", "Kühlkreislauf (vor allem), Kernzone",
     "Seine Treffer kühlen ab: Wer getroffen wird, ist später wieder dran.", True, ""),
    ("boss", "Bluescreen", "Boss", "3B6BFF", 80, 8, 9, 25, 25, "Kampf 5, 10, 15, …", "Mitte jeder Ebene, Wächter des Speicherkellers",
     "Trifft das ganze Team zugleich. Hinterlässt ein seltenes Teil und einen Akku.", False, "Boss-Welle alle 5 Wellen."),
    ("short", "Kurzschluss", "Wächter", "FFB000", 75, 9, 14, 30, 30, "Kampf 20", "Wächter des Kabelschachts, in der Kernzone im Wechsel",
     "Schnell, schlägt wild um sich und landet viele Volltreffer (25 %). Kommt mit zwei Spam-Drohnen.", True, ""),
    ("chiller", "Kältekern", "Wächter", "4DE8FF", 95, 7, 8, 35, 35, "Kampf 30", "Wächter des Kühlkreislaufs, in der Kernzone im Wechsel",
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
    """Zeichnet die Gegner aus den Pixelkarten in Bolt Buddies (ui/pix.gd) als PNG. Ohne den Ordner bleiben die vorhandenen."""
    src = os.path.join(OUT, "..", "Bolt-Buddies", "ui", "pix.gd")
    if not os.path.isfile(src):
        return
    try:
        from PIL import Image
    except ImportError:
        return
    import re
    text = open(src, encoding="utf-8").read()
    pal = dict(re.findall(r'"(\w)": "([0-9A-Fa-f]{6})"', text[:text.index("const MAPS")]))
    dst = os.path.join(OUT, "archiv", "stoerungen", "foes")
    os.makedirs(dst, exist_ok=True)
    for key, *_ in FOES:
        block = re.search(r'"%s": \[(.*?)\]' % key, text[text.index("const MAPS"):], re.S).group(1)
        rows = re.findall(r'"([^"]*)"', block)
        img = Image.new("RGBA", (len(rows[0]), len(rows)), (0, 0, 0, 0))
        for y, row in enumerate(rows):
            for x, ch in enumerate(row):
                if ch in pal:
                    img.putpixel((x, y), tuple(int(pal[ch][i:i + 2], 16) for i in (0, 2, 4)) + (255,))
        img.save(os.path.join(dst, key + ".png"))


def foe_card(f):
    key, name, kind, col, hp, atk, speed, bolts, xp, when, where, does, new, invaders = f
    tag = f'<span class="foe-kind">{kind}</span>' + ('<span class="badge badge-plan">neu in 1.0</span>' if new else "")
    stats = "".join(f'<div><dt>{a}</dt><dd>{v}</dd></div>' for a, v in [("Leben", hp), ("Schaden", atk), ("Tempo", speed)])
    inv = f"""
  <section class="bot-game bot-game-plan">
    <h4>Block Invaders<span class="bot-role">geplant</span></h4>
    <p>{html.escape(invaders)}</p>
  </section>""" if invaders else ""
    return f"""<li class="bot-card" id="{key}" style="--bot:#{col}">
  <div class="bot-head">
    <div class="bot-screen"><img src="foes/{key}.png" width="96" height="96" alt="{name}" loading="lazy"></div>
    <div class="bot-name"><h3>{name}</h3><div class="foe-tags">{tag}</div></div>
  </div>
  <section class="bot-game bot-game-fight">
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


foe_sprites()
foe_index = "".join(f'<a href="#{f[0]}" style="--bot:#{f[3]}"><img src="foes/{f[0]}.png" width="40" height="40" alt="" loading="lazy"><span>{f[1]}</span></a>' for f in FOES)
write("stoerungen", head("Archiv · Störungsprotokoll", "Störungsprotokoll",
    "Alles, was im Rechner schiefgehen kann: Gegner, die im Schrottschacht angreifen, und Ereignisse, die Rätsel im Hauptrechner schwerer machen.") + f"""
      <nav class="bot-index foe-index" aria-label="Gegner">{foe_index}</nav>
      <div class="callout wiki-note">
        <b>So liest du die Karten:</b> Leben, Schaden und Tempo sind Grundwerte. Mit jedem Kampf werden Gegner um 20 % zäher und 14 % stärker,
        und je Ebene gibt es die Hälfte mehr Schrauben. Der blaue Kasten zeigt, was in Block Invaders geplant ist.
      </div>
      <section class="wiki-sec">
        <h2>Gegner im Schrottschacht</h2>
        <ul class="bot-grid">
{chr(10).join(foe_card(f) for f in FOES)}
        </ul>
      </section>
      <section class="wiki-sec">
        <h2>Ereignisse im Hauptrechner</h2>
        <p>Aus Bits &amp; Bolts. Sie treffen Zwischenrechner, den Hauptrechner und auf hohen Stufen auch normale Rätsel. Vier davon bringen Roboter als Eigenart in jedes Rätsel mit, dafür haben sie mehr Ladung oder Tipps.</p>
        <ul class="bot-grid">
{chr(10).join(event_card(e) for e in EVENTS)}
        </ul>
      </section>
""", "Gegner und Ereignisse im Roboter-Universum: Bug, Spam-Drohne, Firewall, Rostwurm, Frostbug, die Bosse und acht Störungen.")

# Ersatzteillager
ITEMS = [("Kreissäge", "Waffe", "Leistung"), ("Laser", "Waffe", "Leistung, Logik"), ("Taser", "Waffe", "Leistung, Takt"),
         ("Blechpanzer", "Rüstung", "Gehäuse"), ("Kühlkörper", "Rüstung", "Gehäuse, Takt"), ("Gummihülle", "Rüstung", "Gehäuse, Logik"),
         ("RAM-Riegel", "Chip", "Logik"), ("Taktquarz", "Chip", "Takt"), ("Turbolader", "Chip", "Leistung, Takt"), ("Zusatzakku", "Chip", "Gehäuse, Logik")]
MODS = [("Übertakter", "+15 % Tempo"), ("Schleifstein", "+20 % Schaden"), ("Panzerplatten", "+25 % Leben"),
        ("Zielhilfe", "+15 % Volltreffer"), ("Tarnlack", "+10 % Ausweichen"), ("Stacheln", "2 Schaden an Angreifern"),
        ("Stromdieb", "heilt sich um 15 % des Schadens"), ("Rostspray", "Getroffene rosten: 2 Schaden je Zug"),
        ("Dickes Blech", "1 Panzerung"), ("Nanobots", "heilt 2 Leben je Zug")]
write("ersatzteile", head("Archiv · Ersatzteillager", "Ersatzteillager",
    "Was einen Roboter in Bolt Buddies stark macht: vier Attribute, drei Ausrüstungsplätze, Module für eine Expedition und gute Pflege.") + f"""
      <section class="wiki-sec">
        <h2>Attribute</h2>
        {table(["Attribut", "Wirkt auf", "Soll später kommen aus"], [
            ["<b>Leistung</b>", "mehr Schaden", "Block Invaders"],
            ["<b>Takt</b>", "öfter dran, weicht aus", "Loop Runner"],
            ["<b>Logik</b>", "mehr Volltreffer", "Bits &amp; Bolts"],
            ["<b>Gehäuse</b>", "mehr Leben", "Kippwelt"]])}
      </section>
      <section class="wiki-sec">
        <h2>Ausrüstung</h2>
        <p>Jeder Roboter hat drei Plätze: Waffe, Rüstung und Chip. Teile gibt es im Schacht und in Schrottkisten aus dem Shop. Überzählige Teile lassen sich für Schrauben verkaufen.</p>
        {table(["Teil", "Platz", "Hebt"], [[f"<b>{a}</b>", b, c] for a, b, c in ITEMS])}
        <p>Jedes Teil hat eine von vier Seltenheiten. Je seltener, desto mehr Punkte bringt es:</p>
        <p class="rarity"><span class="r0">Schrott</span><span class="r1">solide</span><span class="r2">selten</span><span class="r3">legendär</span></p>
      </section>
      <section class="wiki-sec">
        <h2>Module</h2>
        <p>Nach jedem gewonnenen Kampf darf man eine Belohnung wählen. Ein Modul gilt für das ganze Team bis zum Ende der Expedition.</p>
        {table(["Modul", "Wirkung"], [[f"<b>{a}</b>", b] for a, b in MODS])}
      </section>
      <section class="wiki-sec">
        <h2>Pflege und Vorräte</h2>
        {table(["Wert", "sinkt", "steigt durch", "Im Kampf"], [
            ["<b>Energie</b>", "1 Punkt in 6 Minuten", "Akku (+35), Schlafen", "ab 70: +10 % Leben · unter 30: −20 % Leben"],
            ["<b>Laune</b>", "1 Punkt in 5 Minuten, rostig doppelt so schnell", "Spielen (+18), Streicheln, Expedition", "ab 70: +10 % Volltreffer · unter 30: −20 % Schaden"],
            ["<b>Pflege</b>", "1 Punkt in 8 Minuten", "Ölkanne (+40)", "ab 70: +10 % Ausweichen · unter 30: −20 % Tempo"]])}
        <p>Werte sinken auch, wenn das Spiel zu ist, höchstens für 48 Stunden. Kaputt geht dabei nichts: Ein leerer Roboter schaltet ab und lädt an der Ladeleiste.</p>
      </section>
      <section class="wiki-sec" id="ausbau">
        <h2>Werkstatt-Ausbau</h2>
        <p>Kommt mit Bolt Buddies 1.0. Jede Station wird für Schrauben in drei Stufen ausgebaut und steht dann sichtbar in der Werkstatt. Sie machen die Pflege leichter, aber nie überflüssig: Auch ganz ausgebaut braucht ein Roboter nach zwei Tagen wieder etwas.</p>
        {table(["Station", "Stufe 1 / 2 / 3", "Preis in Schrauben"], [
            ["<b>Ladeleiste</b>", "Schlafende laden 35 / 70 / 100 % schneller", "60 / 180 / 450"],
            ["<b>Ölbad</b>", "Pflege sinkt 15 / 30 / 45 % langsamer", "60 / 180 / 450"],
            ["<b>Spielecke</b>", "Laune sinkt 15 / 30 / 45 % langsamer", "60 / 180 / 450"],
            ["<b>Werkbank</b>", "zerlegen und aufwerten / 25 % günstiger / 50 % günstiger", "80 / 200 / 450"],
            ["<b>Funkantenne</b>", 'Empfängt Post aus den anderen Spielen, siehe <a href="../funk/">Funkverbindung</a>. Kommt später.', "–"]])}
        <p>Alles zusammen kostet 2830 Schrauben. Eine Expedition bringt je nach Stufe des Teams etwa 30 bis 250, für die erste Station reichen zwei frühe Expeditionen.</p>
      </section>
      <section class="wiki-sec" id="werkbank">
        <h2>Werkbank</h2>
        <p>An der Werkbank wird aus altem Kram ein Lieblingsteil. Zerlegen macht aus einem Teil im Lager Schrott. Aufwerten hebt ein Teil eine Seltenheit höher und gibt ihm 2 Punkte dazu, auch wenn es gerade ein Roboter trägt.</p>
        {table(["Seltenheit", "Schrott beim Zerlegen", "Aufwerten zur nächsten"], [
            ["<b>Schrott</b>", "1", "20 Schrauben, 3 Schrott"],
            ["<b>solide</b>", "3", "50 Schrauben, 6 Schrott"],
            ["<b>selten</b>", "5", "120 Schrauben, 12 Schrott"],
            ["<b>legendär</b>", "7", "geht nicht höher"]])}
      </section>
      <section class="wiki-sec">
        <h2>Schrauben und Schrott</h2>
        <ul class="plain-list">
          <li><b>Schrauben</b> gibt es im Schacht und für verkaufte Teile. Je tiefer die Ebene, desto mehr: Jede Ebene bringt die Hälfte mehr als die darüber. Ausgegeben werden sie im Shop für Akkus, Öl und Schrottkisten und für den Werkstatt-Ausbau.</li>
          <li><b>Schrott</b> gibt es nur an der Werkbank, aus zerlegten Teilen. Er wird zum Aufwerten gebraucht.</li>
        </ul>
      </section>
""", "Attribute, Ausrüstung, Seltenheiten, Module und Pflegewerte der Roboter in Bolt Buddies.")

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
            ["<b>Snake Jam</b>", "Akkus, Öl, Schrauben"]])}
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
