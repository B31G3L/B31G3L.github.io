# Erzeugt die Archiv-Seiten (Wiki zum Roboter-Universum) für B31G3L.github.io.
# Aufruf aus dem Repo: python tools/make_archiv.py
import os, sys, html

OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
STAND = "13.11.2026"

PAGES = [  # slug, Titel im Menü, Untertitel
    ("", "Das Archiv", "Übersicht"),
    ("roboter", "Roboter-Register", "Alle 22 Roboter"),
    ("einsaetze", "Einsatzorte", "Die Spiele"),
    ("weltkarte", "Weltkarte", "Orte der Welt"),
    ("regelwerk", "Regelwerk", "Binär-Rätsel"),
    ("stoerungen", "Störungsprotokoll", "Gegner und Ereignisse"),
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

def bar(v):
    return f'<span class="pips" aria-label="{v} von 6">' + "".join(
        f'<i class="{"on" if i < v else ""}"></i>' for i in range(6)) + "</span>"

def bot_card(b):
    u = UNLOCK.get(b)
    unlock = "von Anfang an" if not u else f"nach {u[0]} {'Sieg' if u[0] == 1 else 'Siegen'}, Stufe {u[1]} geschafft"
    stats = "".join(f"<div><dt>{a}</dt><dd>{bar(v)}<span class=\"num\">{v}</span></dd></div>"
                    for a, v in zip(ATTR, BASE[b]))
    hero = f'<div><dt>Held in</dt><dd>{html.escape(HERO[b])}</dd></div>' if b in HERO else ""
    return f"""<li class="bot-card" id="{b.lower()}">
  <div class="bot-head"><h3>{b}</h3><span class="bot-say">„{html.escape(SAYS[b])}“</span></div>
  <p class="bot-section">Bits &amp; Bolts · <span>{ROLE[b]}</span></p>
  <p>{html.escape(PUZZLE[b])}</p>
  <p class="bot-unlock">Freigeschaltet {unlock}</p>
  <p class="bot-section">Bolt Buddies · <span>Eigenheit</span></p>
  <p>{html.escape(TRAIT[b])}</p>
  <dl class="bot-stats">{stats}</dl>
  {f'<dl class="bot-stats bot-hero">{hero}</dl>' if hero else ''}
</li>"""

# ── Seiten ───────────────────────────────────────────────────────────────────

# Übersicht
links = "\n".join(
    f'<li class="app-card"><a class="wiki-card-link" href="{s}/"><h3 class="app-title">{t}</h3><p class="app-desc">{d}</p></a></li>'
    for s, t, d in [
        ("roboter", "Roboter-Register", "Alle 22 Roboter mit Rätselfähigkeit, Kampfwerten, Eigenheit und Spruch."),
        ("einsaetze", "Einsatzorte", "Die Spiele des Universums: was man dort tut und was es den Robotern bringt."),
        ("weltkarte", "Weltkarte", "Hauptrechner, Werkstatt, Schrottschacht und die Orte, die noch kommen."),
        ("regelwerk", "Regelwerk", "Die Binär-Regeln aus Bits & Bolts, alle Zusatzregeln und die Schwierigkeitsstufen."),
        ("stoerungen", "Störungsprotokoll", "Bugs, Spam-Drohnen, Firewalls, Rostwürmer, der Bluescreen und alle Ereignisse."),
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
            ["Währung", "Schrauben in der Werkstatt"],
        ], " wiki-table-plain")}
      </section>
""", "Das Archiv der Roboter: Wiki zu Bits & Bolts, Bolt Buddies und allen Spielen im Roboter-Universum von B31G3L.")

# Roboter
cards = "\n".join(bot_card(b) for b in ORDER)
index = " · ".join(f'<a href="#{b.lower()}">{b}</a>' for b in ORDER)
write("roboter", head("Archiv · Roboter-Register", "Roboter-Register",
    "Alle 22 Roboter in der Reihenfolge, in der man sie in Bits &amp; Bolts freischaltet. Jeder bringt ins Rätsel eine eigene Fähigkeit mit und hat in Bolt Buddies eigene Kampfwerte.") + f"""
      <p class="bot-index">{index}</p>
      <div class="callout wiki-note">
        <b>So liest du die Karten:</b> Die Punkte zeigen die Grundwerte auf Stufe 1, zusammen immer 12. Je Stufe wächst jedes Attribut um 12 % seines Grundwerts, höchstens bis Stufe 20.
        In Bolt Buddies findet man neue Roboter im Schrottschacht, nach Kampf 2, 5, 8 und so weiter.
      </div>
      <ul class="bot-grid">
{cards}
      </ul>
      <section class="wiki-sec" id="familien" style="margin-top:40px">
        <h2>Familien <span class="badge badge-plan">Geplant</span></h2>
        <p>Geplant für Bolt Buddies 1.1: Zwei Roboter derselben Familie im Team geben einen kleinen Bonus, drei einen größeren.</p>
        {table(["Familie", "Roboter", "Bonus"], [
            ["<b>Zahlensysteme</b>", "OKTA, HEXA, ASKI, CHROMA, PIXA, NIBBLE", "mehr Volltreffer"],
            ["<b>Logikgatter</b>", "GATE, XOR, NULL, PARI, QUBIT, MIRA", "mehr Panzerung"],
            ["<b>Prozesse</b>", "BYTE, LOOP, SHIFT, DAEMON, ROOT, MORSE", "mehr Tempo"],
            ["<b>Störenfriede</b>", "VIRUS, ERROR, GLITCH, PATCH", "mehr Schaden, mehr Rost"]])}
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
             ["<b>Werkstatt-Ausbau</b>", 'Ladeleiste, Ölbad, Spielecke, Werkbank und Funkantenne für Schrauben ausbauen. Siehe <a href="../ersatzteile/#ausbau">Ersatzteillager</a>.', "1.0"],
             ["<b>Werkbank</b>", "Teile zu Schrott zerlegen und damit andere Teile aufwerten.", "1.0"],
             ["<b>Tagesschacht</b>", "Einmal am Tag eine Expedition mit festem Seed und kleiner Vorgabe. Eine Serie zählt mit, ein verpasster Tag pausiert sie nur.", "1.0"],
             ["<b>Erinnerungen</b>", "Höchstens eine freundliche Meldung am Tag, etwa „BYTE ist ausgeschlafen“. Abschaltbar.", "1.0"],
             ["<b>Vertrauen</b>", "Jeder Roboter sammelt Vertrauen durch Pflege und Expeditionen. Es schaltet Sprüche, Lackierungen und eine stärkere Eigenheit frei.", "1.1"],
             ["<b>Team-Familien</b>", 'Zwei oder drei Roboter derselben Familie im Team geben einen Bonus. Siehe <a href="../roboter/#familien">Roboter-Register</a>.', "1.1"],
             ["<b>Funk</b>", 'Post aus den anderen Spielen. Siehe <a href="../funk/">Funkverbindung</a>.', "1.2"],
         ])
         + '        <p><a href="../ersatzteile/">Zum Ersatzteillager →</a></p>\n') +
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
ENEMIES = [
    ("Bug", "ab Kampf 1", "12", "3", "Der häufigste Gegner. Schwach, aber oft in Gruppen."),
    ("Spam-Drohne", "ab Kampf 2", "9", "4", "Fliegt über die vorderen Reihen hinweg und zielt auf den hintersten Roboter."),
    ("Firewall", "ab Kampf 3", "12", "8", "Langsam, schießt aber wild und hart auf irgendwen im Team."),
    ("Rostwurm", "ab Kampf 4", "34", "7", "Zäh und gepanzert. Hält lange durch."),
    ("Bluescreen", "Kampf 5, 10, 15 …", "80", "8", "Der Boss. Trifft das ganze Team zugleich und hinterlässt ein seltenes Teil und einen Akku. Wächter des Speicherkellers."),
    ("Frostbug", "ab Kampf 21 · 1.0", "16", "4", "Lebt im Kühlkreislauf. Seine Treffer kühlen ab: Wer getroffen wird, ist später wieder dran."),
    ("Kurzschluss", "Kampf 20 · 1.0", "75", "9", "Wächter des Kabelschachts. Schnell, schlägt wild um sich und landet viele Volltreffer."),
    ("Kältekern", "Kampf 30 · 1.0", "95", "7", "Wächter des Kühlkreislaufs. Trifft das ganze Team und kühlt alle zugleich ab."),
]
EVENTS = [
    ("Stromausfall", "", "Nach einem Countdown erlöschen die Vorgaben. Richtige Ziffern direkt daneben holen sie zurück."),
    ("Überspannung", "", "Ein Kurzschluss kostet 2 Ladungen statt 1."),
    ("Wackelkontakt", "", "Immer wieder erlischt eine deiner Ziffern und muss neu eingetragen werden."),
    ("Störsignal", "", "Immer wieder taucht eine falsche Notiz auf."),
    ("Falsche Vorgabe", "ERROR", "Eine Vorgabe zeigt die falsche Ziffer. Wische die andere Ziffer darauf. Wer eine richtige Vorgabe anzweifelt, bekommt einen Kurzschluss."),
    ("Ansteckung", "VIRUS", "Bei einem Kurzschluss erlischt auch eine eingetragene Ziffer daneben."),
    ("Zeitdruck", "DAEMON", "Wer zu lange nichts Richtiges einträgt, verliert eine Ladung. Jede richtige Ziffer setzt die Uhr zurück."),
    ("Nebel", "MORSE", "Klar zu sehen ist nur die Umgebung der zuletzt berührten Zelle."),
]
write("stoerungen", head("Archiv · Störungsprotokoll", "Störungsprotokoll",
    "Alles, was im Rechner schiefgehen kann: Gegner, die im Schrottschacht angreifen, und Ereignisse, die Rätsel im Hauptrechner schwerer machen.") + f"""
      <section class="wiki-sec">
        <h2>Gegner im Schrottschacht</h2>
        <p>Aus Bolt Buddies. Das sind die Grundwerte, mit jedem Kampf werden Gegner zäher und stärker. Frostbug, Kurzschluss und Kältekern kommen mit Bolt Buddies 1.0. In Block Invaders sollen dieselben Gegner die Werkstatt angreifen.</p>
        {table(["Gegner", "Taucht auf", "Leben", "Schaden", "Verhalten"], [[f"<b>{a}</b>", b, c, d, e] for a, b, c, d, e in ENEMIES], " wiki-table-num")}
      </section>
      <section class="wiki-sec">
        <h2>Ereignisse im Hauptrechner</h2>
        <p>Aus Bits &amp; Bolts. Sie treffen Zwischenrechner, den Hauptrechner und auf hohen Stufen auch normale Rätsel. Vier davon bringen Roboter als Eigenart in jedes Rätsel mit, dafür haben sie mehr Ladung oder Tipps.</p>
        {table(["Ereignis", "Bringt mit", "Wirkung"], [[f"<b>{a}</b>", (f'<a href="../roboter/#{b.lower()}">{b}</a>' if b else "–"), c] for a, b, c in EVENTS])}
      </section>
""", "Gegner und Ereignisse im Roboter-Universum: Bug, Spam-Drohne, Firewall, Rostwurm, Bluescreen und acht Störungen.")

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
        <h2>Werkstatt-Ausbau <span class="badge badge-plan">Geplant</span></h2>
        <p>Geplant für Bolt Buddies 1.0. Jede Station lässt sich für Schrauben in drei Stufen ausbauen und ist in der Werkstatt zu sehen.</p>
        {table(["Station", "Wirkung"], [
            ["<b>Ladeleiste</b>", "Schlafende Roboter laden schneller."],
            ["<b>Ölbad</b>", "Pflege sinkt langsamer."],
            ["<b>Spielecke</b>", "Laune sinkt langsamer, Roboter spielen auch miteinander."],
            ["<b>Werkbank</b>", "Teile zu Schrott zerlegen und mit Schrott andere Teile eine Seltenheit höher bringen, bis legendär."],
            ["<b>Funkantenne</b>", 'Empfängt Post aus den anderen Spielen, siehe <a href="../funk/">Funkverbindung</a>.']])}
      </section>
      <section class="wiki-sec">
        <h2>Schrauben</h2>
        <p>Die Währung der Werkstatt. Es gibt sie im Schacht und für verkaufte Teile, ausgegeben werden sie im Shop für Akkus, Öl und Schrottkisten, später auch für den Werkstatt-Ausbau.</p>
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
