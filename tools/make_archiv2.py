# Erzeugt das Archiv 2.0 (die Welt, neu gedacht) für B31G3L.github.io.
# Aufruf aus dem Repo: python tools/make_archiv2.py [Zielordner]
# Alles hier ist ein Entwurf auf dem Papier, nichts davon ist schon in den Spielen umgesetzt.
import os, sys, html
from archiv_data import ORDER, COLORS, SAYS, KEEPSAKE, PUZZLE, TRAIT, HOME

OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
STAND = "14.11.2026"
BOTS = "../../archiv/roboter/bots/"   # Die Sprites liegen schon im alten Archiv
FOES = "../../archiv/stoerungen/foes/"
ART = "../../archiv/weltkarte/img/"

PAGES = [("", "Übersicht", "Was hier entsteht"), ("welt", "Die Welt", "Der alte PC und seine Orte"),
         ("stoerungen", "Störungen", "Wetter und Getier"), ("roboter", "Roboter", "Alle 22 und ihre Heimat")]
DRAFT = '<span class="badge badge-plan">Entwurf</span>'
IDEA = '<span class="badge badge-plan">Idee</span>'
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
## Jeder Ort: Name, Lage, Spiel, kurz, Aussehen, Licht und Klang, Besonderes, Bild aus dem alten Archiv.
## NONE: Orte, die noch in keinem Spiel vorkommen.
NONE = "noch in keinem Spiel"
PLACES = {
    "hauptrechner": dict(
        name="Hauptrechner", part="Prozessor, oben auf der Platine", game="Bits &amp; Bolts · Ziel jedes Aufstiegs",
        short="Der höchste Punkt der Welt und ihr Gedächtnis.",
        look="Ein flacher, quadratischer Block unter dem riesigen Kühlkörper. Zwischen den Kühlrippen geht man wie durch einen Wald aus Metall, in der Mitte führt ein stilles Tor nach innen. Drinnen liegen die Sektoren.",
        sound="Warmes Licht und ein leises, gleichmäßiges Summen. Über allem dreht sich der CPU-Lüfter.",
        special="Hier liegt alles, was der PC je erlebt hat, und jeder Roboter hat hier eine Spur hinterlassen. Jeder Sektor gehört zu einem Roboter: Wer ihn wiederherstellt, sieht ein Stück von früher. Der Hauptrechner ist ein Ort, keine Figur. Er spricht nicht, aber er erinnert sich."),
    "cpu_luefter": dict(
        name="CPU-Lüfter", part="auf dem Prozessor", game=NONE,
        short="Die Windmühle über dem Hauptrechner.",
        look="Ein großes Windrad auf dem Kühlkörper, die Flügel grau vor Staub.",
        sound="Ein gleichmäßiges Surren. Wenn der Hauptrechner nachdenkt, dreht er schneller.",
        special="Von seinem Rand hat man den weitesten Blick über die ganze Platine."),
    "spannungswandler": dict(
        name="Spannungswandler", part="neben dem Prozessor", game=NONE,
        short="Das Tor zum Hauptrechner.",
        look="Eine Reihe Kondensatoren wie Säulen, dazwischen kleine Spulen. Zusammen sehen sie aus wie ein Tor.",
        sound="Ein feines Pfeifen, wenn viel Strom fließt.",
        special="Hier wird der Strom aus dem Netzteil fein gemacht für den Prozessor. Wer hier durchgeht, ist fast am Ziel."),
    "arbeitsspeicher": dict(
        name="Arbeitsspeicher", part="Platine · Etage 8–9, direkt neben dem Prozessor", game="Bits &amp; Bolts",
        short="Speicherriegel wie Hochhäuser, immer Betrieb.",
        look="Die Riegel stehen in Reihen wie Hochhäuser, ihre kleinen Chips sind die Fenster. Dazwischen enge Gassen.",
        sound="Überall blinken Lämpchen, es wuselt und flüstert. Wenn der PC nachdenkt, wird es laut.",
        special="Hier ist alles nur vorübergehend: Was nicht gespeichert wird, ist beim Ausschalten weg. Die Bewohner sind gesellig, schnell und ein bisschen vergesslich."),
    "chipsatz": dict(
        name="Chipsatz", part="Platine · Etage 5–7", game="Bits &amp; Bolts",
        short="Die Kreuzung, an der alle Leiterbahnen zusammenlaufen.",
        look="Ein flacher Chip mitten auf der Platine. Von allen Seiten laufen Leiterbahnen auf ihn zu wie Straßen auf einen Marktplatz.",
        sound="Hell und geschäftig. Ständig fließt etwas vorbei, es klickt und schaltet.",
        special="Wer irgendwohin will, kommt hier vorbei. Hier wird getauscht: Teile, Nachrichten, Gerüchte. Die Begegnungen aus Bits &amp; Bolts passen genau hierher."),
    "bios": dict(
        name="BIOS-Chip", part="auf der Platine", game=NONE,
        short="Hier hat der Neustart begonnen.",
        look="Ein kleiner, unscheinbarer Chip mit einem verblassten Aufkleber.",
        sound="Meistens ganz still. Nur beim Einschalten leuchtet er kurz auf.",
        special="Der BIOS-Chip weckt den PC als Allererstes. Vielleicht ist BYTE genau hier aufgewacht. Er kennt die Grundregeln, nach denen im PC alles funktioniert."),
    "knopfzelle": dict(
        name="Knopfzelle", part="Platine · Etage 3–4", game="Bits &amp; Bolts",
        short="Die kleine Batterie, die nie aufgehört hat.",
        look="Eine silberne Münze, flach in ihrer Halterung und groß wie ein Platz. Darauf sind Zahlen eingeprägt, die keiner mehr lesen kann.",
        sound="Still. Nur ein ganz leises Ticken.",
        special="Sie hat die Uhr am Laufen gehalten, auch in all den Jahren, in denen alles aus war. Die Roboter kommen her, um nachzudenken. Hier weiß man, wie spät es ist und wie lange alles geschlafen hat."),
    "steckkarten": dict(
        name="Steckkarten", part="Platine · Etage 1–2, ganz unten", game="Bits &amp; Bolts",
        short="Wände und Klippen, hier beginnt der Aufstieg.",
        look="Hohe Karten stehen in ihren Steckplätzen, dazwischen liegen enge Schluchten. Die goldenen Kontakte an den Kanten sind wie Treppenstufen.",
        sound="Schattig, nur von oben fällt Licht. Ab und zu knackt es, wenn eine Karte wackelt.",
        special="Ein Durchgangsort zwischen Grafikkarte, Soundkarte und Netzwerkkarte. Wer hier hochklettert, lernt die Grundregeln."),
    "grafikkarte": dict(
        name="Grafikkarte", part="oberster Steckplatz", game=NONE,
        short="Bunt, laut und voller Licht.",
        look="Eine breite Karte mit eigenem Lüfter, rundherum bunt beleuchtet.",
        sound="Es flackert in allen Farben. Wenn sie arbeitet, heult ihr Lüfter auf.",
        special="Hier entstehen alle Bilder. Die Bewohner sind Künstler und streiten gern über Farben."),
    "soundkarte": dict(
        name="Soundkarte", part="Steckplatz", game=NONE,
        short="Hier entstehen alle Töne.",
        look="Eine schmale Steckkarte mit runden Buchsen am Ende.",
        sound="Hier ist es nie ganz still. Töne werden geübt, Echos hallen.",
        special="Wer genau hinhört, hört alte Melodien, die der PC früher gespielt hat."),
    "netzwerkkarte": dict(
        name="Netzwerkkarte", part="Steckplatz", game=NONE,
        short="Sie lauscht nach draußen.",
        look="Eine Steckkarte mit einer Buchse nach draußen und zwei kleinen Lämpchen.",
        sound="Meistens still. Manchmal blinkt ein Lämpchen, als käme von draußen eine Nachricht.",
        special="Ob draußen noch jemand ist, weiß keiner. MORSE ist oft hier und horcht."),
    "anschluesse": dict(
        name="Anschlüsse", part="Rückwand des Gehäuses", game=NONE,
        short="Der Rand der Welt.",
        look="Die Rückwand mit vielen Öffnungen: Buchsen, Steckplätze, Schlitze. Hinter manchen schimmert Licht.",
        sound="Zugig. Durch manche Buchsen dringen fremde Signale.",
        special="Dahinter ist das Draußen, und keiner weiß, was dort ist. Von hier kommen die Spam-Drohnen herein."),
    "flachband": dict(
        name="Flachbandkabel", part="zwischen Platine und Laufwerken", game=NONE,
        short="Brücken quer durchs Gehäuse.",
        look="Breite graue Bänder, die von der Platine hinüber zu den Laufwerken gespannt sind.",
        sound="Sie schwingen leise im Luftzug.",
        special="Wer mutig ist, balanciert darüber, statt den langen Weg zu nehmen."),
    "cd": dict(
        name="CD-Laufwerk", part="vorne oben, Nachbar der Werkstatt", game=NONE,
        short="Eine Schublade, die manchmal von selbst aufgeht.",
        look="Ein flacher Kasten mit Schublade. Drinnen liegt noch eine Scheibe, die im Licht in allen Regenbogenfarben schimmert.",
        sound="Still, bis die Scheibe anläuft. Dann heult es auf und vibriert durch die Wand bis in die Werkstatt.",
        special="Manchmal geht die Schublade von selbst auf und wieder zu, und keiner weiß, warum. Was auf der Scheibe ist, hat noch niemand herausgefunden."),
    "werkstatt": dict(
        name="Werkstatt", part="vorne oben, leerer Laufwerksschacht", game="Bolt Buddies · Zuhause",
        short="Das Zuhause aller Geretteten.", img="workshop.png",
        look="Ein Blechkasten vorne im Gehäuse, in dem früher ein Laufwerk steckte. Durch den Schlitz in der alten Blende fällt Licht. Drinnen: Lochwand mit Werkzeug, Regal mit Teilekisten, Ladeleiste und die Andenken.",
        sound="Gemütliches Licht. Werkzeug klappert, jemand schnarcht an der Ladeleiste.",
        special="Der einzige Ort, der wirklich den Robotern gehört. Mit jedem Geretteten wird sie voller, weil jeder ein Andenken an seine Heimat aufstellt. Hinter der Werkstatt führt der Aufzug zwischen Platine und Laufwerken hinunter in den Schacht. Hier gibt es keine Störungen."),
    "diskette": dict(
        name="Diskettenlaufwerk", part="vorne, unter der Werkstatt", game=NONE,
        short="Der älteste Teil des PCs.",
        look="Ein schmaler Schlitz mit Klappe. Dahinter wartet ein Lesekopf seit Jahren auf eine Diskette.",
        sound="Wenn es anläuft, rattert und klackert es wie eine alte Maschine.",
        special="Hier liegen vergessene Disketten, und auf manchen steht noch mit der Hand geschrieben, was einmal darauf war."),
    "festplatte": dict(
        name="Festplatte", part="vorne im Laufwerkskäfig", game=NONE,
        short="Eine alte Scheibe, die sich dreht.",
        look="Ein schwerer Kasten, darin eine spiegelnde Scheibe, über die ein Lesearm schwingt.",
        sound="Ruhig, bis die Scheibe anläuft. Dann surrt und klackert es.",
        special="Alles, was je gespeichert wurde, liegt hier in endlosen Spuren, wie in einer Bibliothek. Anders als der Hauptrechner bewahrt sie Dinge auf, keine Erinnerungen."),
    "lautsprecher": dict(
        name="PC-Lautsprecher", part="vorne unten", game=NONE,
        short="Die Stimme des PCs.",
        look="Ein kleiner runder Lautsprecher, kaum größer als eine Münze.",
        sound="Er piepst. Einmal kurz beim Start heißt: alles gut.",
        special="Mehr als Piepsen kann er nicht, aber jeder versteht ihn."),
    "frontblende": dict(
        name="Frontblende", part="Vorderseite des Gehäuses", game=NONE,
        short="Das Einzige, was man von außen sieht.",
        look="Die Vorderseite mit dem Einschaltknopf und zwei kleinen Lämpchen, grün und orange.",
        sound="Von innen scheinen die Lämpchen wie zwei kleine Sonnen durch die Wand.",
        special="Der Einschaltknopf ist der Grund, warum alle wach sind. Aber keiner war je draußen und hat ihn gesehen."),
    "schicht1": dict(
        name="Schraubenhalde", part="Schacht · gleich unter der Werkstatt", game="Bolt Buddies",
        short="Hier liegt, was zuletzt gefallen ist.", img="layer_0.png",
        look="Ein Hang aus Schrauben, Klammern und Krümeln, der sich zwischen Platine und Laufwerken gesammelt hat.",
        sound="Von oben fällt noch etwas Licht. Bei jedem Schritt klimpern Schrauben.",
        special="Hier liegen die meisten Verlorenen, weil sie nicht tief gefallen sind."),
    "kabelsalat": dict(
        name="Kabelsalat", part="Schacht · unter der Platine", game="Bolt Buddies",
        short="Ein Dschungel aus alten Kabeln.", img="layer_1.png",
        look="Dicke Kabelstränge hängen kreuz und quer, verknotet und mit Kabelbindern zusammengezurrt. Dazwischen hängen Staubfäden wie Lianen.",
        sound="Dämmrig, ab und zu blitzen Funken. Es knistert überall.",
        special="Man verläuft sich leicht. Die Kabel führen überallhin, auch dorthin, wo seit Jahren keiner mehr war."),
    "lueftergrund": dict(
        name="Lüftergrund", part="Schacht · vor dem Frontlüfter", game="Bolt Buddies",
        short="Kalt und windig, Staubflusen treiben wie Schnee.", img="layer_2.png",
        look="Der Boden vor dem Gehäuselüfter. Staubflusen treiben wie Schnee, die Wände sind mit grauem Flaum bedeckt.",
        sound="Kühles, blasses Licht. Der Lüfter rauscht gleichmäßig wie Wind.",
        special="Es ist immer windig und kalt. Wer zu lange bleibt, wird langsam."),
    "netzteil": dict(
        name="Netzteil", part="Schacht · ganz unten", game="Bolt Buddies",
        short="Ganz unten brummt und glüht es.", img="layer_3.png",
        look="Ein Blechkasten ganz unten, durch die Lüftungsschlitze glüht es orange. Drinnen stehen Spulen und Kondensatoren wie Türme.",
        sound="Rot und warm. Ein tiefes Brummen, das man im Bauch spürt.",
        special="Von hier kommt der ganze Strom. Die ältesten und eigenwilligsten Roboter wohnen hier und mögen die Hitze, für Besucher ist es anstrengend."),
}
GROUPS = [  # Abschnitt der Weltseite: Schlüssel, Titel, Orte
    ("bnb", "Bits &amp; Bolts: der Aufstieg", ["hauptrechner", "arbeitsspeicher", "chipsatz", "knopfzelle", "steckkarten"]),
    ("bb", "Bolt Buddies: Werkstatt und Schacht", ["werkstatt", "schicht1", "kabelsalat", "lueftergrund", "netzteil"]),
    ("frei", "Noch in keinem Spiel", ["cpu_luefter", "spannungswandler", "bios", "grafikkarte", "soundkarte", "netzwerkkarte",
                                      "anschluesse", "flachband", "cd", "diskette", "festplatte", "lautsprecher", "frontblende"]),
]
assert sorted(k for g_ in GROUPS for k in g_[2]) == sorted(PLACES), "jeder Ort gehört in genau einen Abschnitt"
GAME_OF = {k: g_[0] for g_ in GROUPS for k in g_[2]}

## Der Querschnitt: ein offener Tower von der Seite, hinten links, vorne rechts.
## Form je Ort: ("r", x, y, b, h) oder ("c", x, y, Radius) oder ("p", Punkte); Beschriftung: Zeilen, Mitte x/y, gedreht
SHAPES = {
    "anschluesse": (("r", 20, 40, 40, 500), ["Anschlüsse"], (40, 290), True),
    "spannungswandler": (("r", 78, 40, 26, 200), ["Spannungswandler"], (91, 140), True),
    "cpu_luefter": (("r", 112, 40, 160, 54), ["CPU-Lüfter"], (192, 67), False),
    "hauptrechner": (("r", 112, 102, 160, 130), ["Hauptrechner"], (192, 167), False),
    "arbeitsspeicher": (("r", 284, 40, 96, 200), ["Arbeits-", "speicher"], (332, 140), False),
    "chipsatz": (("r", 150, 262, 110, 70), ["Chipsatz"], (205, 297), False),
    "bios": (("r", 84, 350, 92, 40), ["BIOS-Chip"], (130, 370), False),
    "knopfzelle": (("c", 322, 352, 36), ["Knopf-", "zelle"], (322, 352), False),
    "steckkarten": (("r", 78, 410, 304, 174), ["Steck-", "karten"], (346, 546), False),
    "grafikkarte": (("r", 90, 422, 280, 46), ["Grafikkarte"], (230, 445), False),
    "soundkarte": (("r", 90, 482, 220, 40), ["Soundkarte"], (200, 502), False),
    "netzwerkkarte": (("r", 90, 536, 220, 40), ["Netzwerkkarte"], (200, 556), False),
    "flachband": (("p", "382,300 482,256 482,276 382,320"), ["Flachband"], (432, 287), "slant"),
    "cd": (("r", 482, 40, 138, 54), ["CD-Laufwerk"], (551, 67), False),
    "werkstatt": (("r", 482, 100, 138, 82), ["Werkstatt"], (551, 141), False),
    "diskette": (("r", 482, 188, 138, 44), ["Diskettenlaufwerk"], (551, 210), False),
    "festplatte": (("r", 482, 240, 138, 72), ["Festplatte"], (551, 276), False),
    "lautsprecher": (("c", 551, 500, 34), ["PC-Laut-", "sprecher"], (551, 500), False),
    "frontblende": (("r", 630, 40, 22, 700), ["Frontblende"], (641, 390), True),
    "schicht1": (("r", 398, 190, 74, 200), ["Schrau-", "ben-", "halde"], (435, 345), False),
    "kabelsalat": (("p", "398,396 472,396 472,740 20,740 20,610 398,610"), ["Kabelsalat"], (210, 675), False),
    "lueftergrund": (("r", 482, 610, 138, 130), ["Lüftergrund"], (551, 722), False),
    "netzteil": (("r", 20, 752, 300, 126), ["Netzteil"], (170, 815), False),
}
assert sorted(SHAPES) == sorted(PLACES), "jeder Ort braucht eine Form im Querschnitt"


def pc_svg():
    """Der Querschnitt als SVG. Farbe nach Spiel, gestrichelt: noch in keinem Spiel. Jeder Ort springt zu seiner Karte."""
    parts = ['<rect class="pc-case" x="10" y="10" width="652" height="880" rx="14"/>',
             '<rect class="pc-board" x="70" y="30" width="320" height="570" rx="6"/>',
             '<text class="pc-hint" x="80" y="596" dominant-baseline="middle">Platine</text>',
             '<text class="pc-hint" x="476" y="866" text-anchor="middle">Gehäuseboden</text>',
             '<text class="pc-hint" x="20" y="912">← hinten</text>',
             '<text class="pc-hint" x="652" y="912" text-anchor="end">vorne →</text>']
    # Die großen Flächen zuerst, damit die Karten und der Lüfter darauf liegen
    order = ["steckkarten", "kabelsalat"] + [k for k in SHAPES if k not in ("steckkarten", "kabelsalat", "flachband")] + ["flachband"]
    for key in order:
        shape, lines, (lx, ly), turn = SHAPES[key]
        if shape[0] == "r":
            el = f'<rect class="pc-shape" x="{shape[1]}" y="{shape[2]}" width="{shape[3]}" height="{shape[4]}" rx="5"/>'
        elif shape[0] == "c":
            el = f'<circle class="pc-shape" cx="{shape[1]}" cy="{shape[2]}" r="{shape[3]}"/>'
        else:
            el = f'<polygon class="pc-shape" points="{shape[1]}"/>'
        if key == "lueftergrund":   # Lüfterrad
            el += '<circle class="pc-deco" cx="551" cy="662" r="38"/><path class="pc-deco" d="M551 624v76M513 662h76M524 635l54 54M578 635l-54 54"/>'
        if key == "arbeitsspeicher":   # vier Riegel
            el += "".join(f'<rect class="pc-deco" x="{x}" y="48" width="10" height="184"/>' for x in (292, 312, 352, 362))
        rot = f' transform="rotate(-90 {lx} {ly})"' if turn is True else (f' transform="rotate(-24 {lx} {ly})"' if turn == "slant" else "")
        small = " pc-small" if turn or key in ("bios", "diskette", "knopfzelle", "lautsprecher") else ""
        h0 = ly - (len(lines) - 1) * 7.5
        text = "".join(f'<tspan x="{lx}" y="{h0 + i * 15}">{t}</tspan>' for i, t in enumerate(lines))
        parts.append(f'<a class="pc-place pc-{GAME_OF[key]}" href="#{key}"><title>{PLACES[key]["name"]}</title>{el}'
                     f'<text class="pc-label{small}"{rot}>{text}</text></a>')
    parts.append('<line class="pc-lift" x1="466" y1="182" x2="466" y2="745"/>')
    parts.append('<text class="pc-hint pc-lift-label" x="461" y="208" text-anchor="end">Aufzug</text>')
    svg = "\n".join("            " + p for p in parts)
    return f"""        <div class="pc-wrap">
          <svg class="pc-svg" viewBox="0 0 672 922" role="img" aria-label="Der PC im Querschnitt: links hinten die Platine, rechts vorne die Laufwerke, unten der Schacht">
{svg}
          </svg>
        </div>
        <p class="pc-legend"><span class="pc-key pc-bnb">Bits &amp; Bolts</span><span class="pc-key pc-bb">Bolt Buddies</span><span class="pc-key pc-frei">noch in keinem Spiel</span></p>
"""


## Heimat jedes Roboters. Gefunden wird er trotzdem im Schacht, siehe SHAFT.
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


# ── Störungen ────────────────────────────────────────────────────────────────
## Art, Name, Bild (Sprite in FOES) oder Code, Farbe, Orte, wie sie in der Welt sind, was sie im Spiel tun
## Oben auf der Platine sind Störungen wie Wetter, unten im Schacht wie Getier.
STOER = {
    # Wetter auf der Platine (Ereignisse aus Bits & Bolts)
    "wackel_w": ("wetter", "Wackelkontakt", "~ ~", "FF9A3D", ["steckkarten", "hauptrechner"],
                 "Die Karten sitzen locker in ihren Steckplätzen, und zwischen ihnen springen Wackelkontakte hin und her. Immer wieder geht irgendwo ein Licht aus.",
                 "Immer wieder erlischt eine deiner Ziffern und muss neu eingetragen werden."),
    "signal": ("wetter", "Störsignal", "? !", "4DE8FF", ["arbeitsspeicher", "hauptrechner"],
               "Im Gedränge der Speicherriegel rauscht es. Gedanken der anderen schwirren durch die Gassen, und manchmal bleibt einer hängen.",
               "Immer wieder taucht eine falsche Notiz auf."),
    "strom": ("wetter", "Stromausfall", "0 V", "B4BECC", ["knopfzelle", "hauptrechner"],
              "Die Knopfzelle ist alt. Ab und zu flackert es, und dann wird es für einen Moment dunkel und still.",
              "Nach einem Countdown erlöschen die Vorgaben. Richtige Ziffern direkt daneben holen sie zurück."),
    "spannung": ("wetter", "Überspannung", "!! V", "FFD34D", ["chipsatz", "hauptrechner"],
                 "Wo alle Leitungen zusammenlaufen, staut sich manchmal zu viel Strom. Dann knistert die Luft, und jeder Fehler tut doppelt weh.",
                 "Ein Kurzschluss kostet 2 Ladungen statt 1."),
    # Getier im Schacht (Gegner aus Bolt Buddies)
    "bug": ("getier", "Bug", "bug", "FF5252", ["schicht1", "kabelsalat", "lueftergrund", "netzteil"],
            "Kleine Käfer, die sich in alten Daten einnisten. Einzeln harmlos, aber selten allein.",
            "Der häufigste Gegner. Schwach, aber oft in Gruppen."),
    "drone": ("getier", "Spam-Drohne", "drone", "B46CFF", ["schicht1", "kabelsalat", "lueftergrund", "netzteil", "anschluesse"],
              "Schwirrt summend herum und lässt Werbemüll fallen. Kommt ursprünglich durch die Anschlüsse herein.",
              "Fliegt über die vorderen Reihen hinweg und zielt auf den hintersten Roboter."),
    "turret": ("getier", "Firewall", "turret", "FF5252", ["schicht1", "kabelsalat", "lueftergrund", "netzteil"],
               "Eine sture Wand, die niemanden durchlassen will, auch die eigenen Leute nicht. Sie meint es eigentlich gut.",
               "Langsam, schießt aber wild und hart auf irgendwen im Team."),
    "worm": ("getier", "Rostwurm", "worm", "D9773A", ["schicht1", "kabelsalat", "netzteil"],
             "Frisst sich langsam durch altes Metall. Wo er war, bleibt Rost.",
             "Zäh und gepanzert. Im Kabelsalat und im Netzteil doppelt so oft."),
    "spark": ("getier", "Wackelkontakt", "spark", "FF9A3D", ["kabelsalat"],
              "Ein zappelndes Funkenwesen, das zwischen losen Steckern hin und her springt. Wer es anfasst, bekommt einen Schlag. Dieselben Wesen lassen oben auf der Platine die Lichter flackern.",
              "Schnell und geladen: Wer ihn trifft, bekommt einen Schlag zurück."),
    "frost": ("getier", "Frostbug", "frost", "4DE8FF", ["lueftergrund"],
              "Lebt im kalten Luftzug des Lüfters. Wo er hinbeißt, wird es klamm und langsam.",
              "Seine Treffer kühlen ab: Wer getroffen wird, ist später wieder dran."),
    "heat": ("getier", "Überhitzer", "heat", "FF5252", ["netzteil"],
             "Glüht still vor sich hin und strahlt Hitze in alle Richtungen ab.",
             "Trifft das ganze Team zugleich."),
    # Wächter der Schichten
    "boss": ("waechter", "Bluescreen", "boss", "3B6BFF", ["schicht1"],
             "Ein großer blauer Bildschirm, der alles anhält, was ihm zu nahe kommt. Danach ist er selbst ganz verwirrt.",
             "Wächter der ersten Schicht. Trifft das ganze Team zugleich."),
    "short": ("waechter", "Kurzschluss", "short", "FFB000", ["kabelsalat"],
              "Ein wildes Knäuel aus Funken, entstanden, wo sich zwei blanke Kabel berühren.",
              "Wächter des Kabelsalats. Schnell, schlägt wild um sich und landet viele Volltreffer."),
    "chiller": ("waechter", "Kältekern", "chiller", "4DE8FF", ["lueftergrund"],
                "Ein Klumpen aus Eis und Staub, der sich genau vor dem Lüfter festgesetzt hat.",
                "Wächter des Lüftergrunds. Trifft das ganze Team und kühlt alle zugleich ab."),
    "trafo": ("waechter", "Brummtrafo", "trafo", "FF7A45", ["netzteil"],
              "Ein dicker Transformator mit Kupferspulen, der seit Jahren vor sich hin brummt. Er ist nicht böse, nur grantig, weil ihn das eigene Brummen nicht schlafen lässt.",
              "Wächter des Netzteils, zuerst in Kampf 40. Trifft das ganze Team zugleich, und wer ihn trifft, verbrennt sich."),
    # Ideen für Orte, die noch keine Störung haben
    "fluse": ("idee", "Staubfluse", "≋", "B4BECC", ["lueftergrund"],
              "Treibt im Luftzug, bleibt überall hängen und verstopft die Wege. Völlig harmlos, nur lästig.", ""),
    "kratzer": ("idee", "Kratzer", "/ /", "C9A8FF", ["festplatte"],
                "Die Scheibe hat Kratzer. Wo der Lesearm darüberfährt, springt alles, und ein Stück Gespeichertes fehlt.", ""),
    "pixel": ("idee", "Pixelfehler", "▪ ▫", "FF5CF0", ["grafikkarte"],
              "Ein bunter Fleck, der einfach nicht weggeht. Manchmal wandert er.", ""),
}
## Eigenarten, die Roboter aus ihrer Heimat mitbringen (Ereignisse aus Bits & Bolts)
QUIRKS = [
    ("Falsche Vorgabe", "ERROR", "Eine Vorgabe zeigt die falsche Ziffer. Wer eine richtige anzweifelt, bekommt einen Kurzschluss."),
    ("Ansteckung", "VIRUS", "Bei einem Kurzschluss erlischt auch eine eingetragene Ziffer daneben."),
    ("Zeitdruck", "DAEMON", "Wer zu lange nichts Richtiges einträgt, verliert eine Ladung."),
    ("Nebel", "MORSE", "Klar zu sehen ist nur die Umgebung der zuletzt berührten Zelle."),
]
assert all(p in PLACES for s in STOER.values() for p in s[4])


# ── Bausteine ────────────────────────────────────────────────────────────────
def mini(b):
    return (f'<a class="mini-bot" href="../roboter/#{b.lower()}" style="--bot:#{COLORS[b]}">'
            f'<img src="{BOTS}{b.lower()}.png" width="16" height="19" alt="">{b}</a>')


def chip(key):
    kind, name, pic, col = STOER[key][:4]
    img = (f'<img src="{FOES}{pic}.png" width="16" height="16" alt="">' if kind in ("getier", "waechter")
           else f'<span class="chip-code">{html.escape(pic)}</span>')
    return f'<a class="mini-bot" href="../stoerungen/#{key}" style="--bot:#{col}">{img}{name}</a>'


def found_here(key):
    return [b for b in ORDER if b != "BYTE" and SHAFT[HOME[b]] == key]


def place_card(key):
    p = PLACES[key]
    pic = f'<img class="place-img" src="{ART}{p["img"]}" alt="{p["name"]}" loading="lazy">' if p.get("img") else ""
    rows = [("Aussehen", p["look"]), ("Licht und Klang", p["sound"]), ("Besonderes", p["special"])]
    stoer = [k for k, s in STOER.items() if key in s[4]]
    if stoer:
        rows.append(("Störungen", " ".join(chip(k) for k in stoer)))
    if HEIMAT.get(key):
        rows.append(("Wohnen hier", " ".join(mini(b) for b in HEIMAT[key])))
    if found_here(key):
        rows.append(("Hier gefunden", " ".join(mini(b) for b in found_here(key))))
    if key == "werkstatt":
        rows.append(("Schon da", f'{mini("BYTE")} war als Erster wach.'))
    dl = "".join(f"<div><dt>{a}</dt><dd>{b}</dd></div>" for a, b in rows)
    return f"""          <li class="place place-detail" id="{key}">{pic}<div class="place-head"><h3>{p["name"]}</h3></div><p class="game-genre">{p["part"]} · {p["game"]}</p><p>{p["short"]}</p><dl class="place-facts">{dl}</dl></li>"""


# ── Übersicht ────────────────────────────────────────────────────────────────
cards = "\n".join(
    f'<li class="app-card"><a class="wiki-card-link" href="{s}/"><h3 class="app-title">{t}</h3><p class="app-desc">{d}</p></a></li>'
    for s, t, d in [
        ("welt", "Die Welt", "Ein alter Tower-PC, der wieder läuft. Der Querschnitt und alle Orte im Detail: wie sie aussehen, wie sie klingen, wer dort wohnt."),
        ("stoerungen", "Störungen", "Oben auf der Platine wie Wetter, unten im Schacht wie Getier. Keine Feinde, nur Ärgernisse eines alten PCs."),
        ("roboter", "Roboter", "Alle 22 Roboter mit ihrer Heimat im PC, ihrem Fundort im Schacht und ihrem Andenken."),
    ])
write("", "Übersicht", "Archiv 2.0: Die Welt der Roboter wird neu gedacht. Entwurf zu Welt, Störungen und Robotern von Bits & Bolts und Bolt Buddies.",
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
            ["Neu offen", "alles andere"],
        ], " wiki-table-plain")}
      </section>
""")


# ── Die Welt ─────────────────────────────────────────────────────────────────
def group_section(key, title, keys):
    intro = {
        "bnb": "<p>In Bits &amp; Bolts klettert ein Roboter Etage für Etage über das Mainboard nach oben. Die Etagen gehören zu vier Gegenden mit eigener Stimmung und eigenem Wetter: Steckkarten (1–2), Knopfzelle (3–4), Chipsatz (5–7) und Arbeitsspeicher (8–9). Die Karte im Spiel zeigt, wo eine neue Gegend beginnt. Kleinere Chips auf dem Weg sind die Zwischenrechner, Etappenziele vor dem Hauptrechner. Die Binärrätsel sind dabei wörtlich das, was die Roboter tun: alte Daten wieder zusammensetzen.</p>\n"
               "        <p class=\"muted-small\">Die Reihenfolge folgt der echten Platine: unten die Steckkarten, oben neben dem Prozessor der Arbeitsspeicher.</p>",
        "bb": "<p>Die Werkstatt ist das Zuhause. Darunter liegt der Boden des Gehäuses, wo alles landet, was in all den Jahren heruntergefallen ist: Staub, verlorene Schrauben, abgebrochene Teile und die Roboter selbst. "
              "In Bolt Buddies steigt ein Team Schicht für Schicht hinab und holt sie zurück. Dass Schrauben die Währung sind, passt: In einem alten PC fallen genau die nach unten.</p>\n"
              "        <p class=\"muted-small\">Bilder: die heutigen Kulissen aus Bolt Buddies.</p>",
        "frei": "<p>Diese Orte gibt es im PC, manche davon sind die Heimat von Robotern. In einem Spiel kommen sie noch nicht vor.</p>",
    }[key]
    return f"""      <section class="wiki-sec" id="{key}">
        <h2>{title}</h2>
        {intro}
        <ul class="place-list place-list-wide">
{chr(10).join(place_card(k) for k in keys)}
        </ul>
      </section>
"""

write("welt", "Die Welt", "Die Welt der Roboter ist ein alter Tower-PC: oben der Hauptrechner als Gedächtnis, in der Mitte die Werkstatt, unten der Schrottschacht. Alle Orte im Detail.",
      head('<a href="../">Archiv 2.0</a> · Die Welt', "Die Welt",
           "Die ganze Welt ist ein alter Tower-PC. Er stand jahrelang ausgeschaltet herum, jetzt läuft er wieder. "
           "Für die Roboter ist er riesig: hinten die Platine mit dem Hauptrechner ganz oben, vorne die Werkstatt zwischen den Laufwerken, unten der Schrottschacht.") + f"""
      <section class="wiki-sec">
        <h2>Grundsätze</h2>
        {table(["", ""], [
            ["Schauplatz", "ein alter Tower-PC, sonst nichts"],
            ["Anfang", "Der PC wird wieder eingeschaltet. Mit dem Strom wachen die Roboter auf, BYTE als Erster."],
            ["Menschen", "spielen keine Rolle. Wer den PC eingeschaltet hat, ist egal."],
            ["Bedrohung", "gibt es nicht. Kein Zeitdruck, kein Feind, der alles zerstören will."],
            ["Antrieb", "Neugier und Gemeinschaft: Freunde finden, den PC erkunden, ihn Stück für Stück herrichten."],
            ["Störungen", 'gehören zum PC wie Wetter oder Ungeziefer. Eher lästig als böse, siehe <a href="../stoerungen/">Störungen</a>.'],
            ["Ton", "gemütlich"],
        ], " wiki-table-plain")}
      </section>

      <section class="wiki-sec">
        <h2>Der PC im Querschnitt</h2>
        <p>Der Tower offen von der Seite: hinten links die Platine, über die es in Bits &amp; Bolts hinauf zum Hauptrechner geht. Vorne rechts die Laufwerke mit der Werkstatt. Dazwischen fährt der Aufzug hinunter in den Schacht von Bolt Buddies.</p>
{pc_svg()}        <p class="muted-small">Antippen führt zum Ort weiter unten. Farbig: Orte, die schon in einem Spiel vorkommen. Gestrichelt: noch in keinem Spiel.</p>
      </section>

      <section class="wiki-sec" id="warum">
        <h2>Warum alle unten liegen</h2>
        <p>Jeder Roboter hat eine Heimat irgendwo im PC. Als der PC ausging, sind aber alle heruntergefallen und liegen jetzt verstreut im Schrottschacht. Je tiefer jemand gefallen ist, desto schwerer ist er zu finden.</p>
        <p>So greifen die beiden Spiele ineinander: <b>Unten im Schacht findet man verlorene Roboter, oben im Hauptrechner verlorene Erinnerungen.</b> Das Andenken, das jeder Gerettete in die Werkstatt mitbringt, erinnert an seine Heimat.</p>
      </section>

{"".join(group_section(*g_) for g_ in GROUPS)}
      <section class="wiki-sec">
        <h2>Noch offen</h2>
        <ul class="plain-list">
          <li>Ob und wie die Orte, die noch in keinem Spiel vorkommen, einmal ins Spiel kommen.</li>
        </ul>
      </section>
""")


# ── Störungen ────────────────────────────────────────────────────────────────
def stoer_card(key):
    kind, name, pic, col, where, world, game_ = STOER[key]
    if kind in ("getier", "waechter"):
        big = kind == "waechter"
        screen = f'<div class="bot-screen"><img class="{"foe-l" if big else "foe-s"}" src="{FOES}{pic}.png" width="{96 if big else 80}" height="{96 if big else 80}" alt="{name}" loading="lazy"></div>'
    else:
        screen = f'<div class="bot-screen event-code"><span style="color:#{col};text-shadow:0 0 8px #{col}80">{html.escape(pic)}</span></div>'
    label = {"wetter": "Wetter", "getier": "Getier", "waechter": "Wächter", "idee": "Idee"}[kind]
    places = " · ".join(f'<a href="../welt/#{p}">{PLACES[p]["name"]}</a>' for p in where)
    play = ""
    if game_:
        icon, gname = ("bits-and-bolts", "Bits &amp; Bolts") if kind == "wetter" else ("bolt-buddies", "Bolt Buddies")
        cls = "bot-game-puzzle" if kind == "wetter" else "bot-game-fight"
        play = f"""
  <section class="bot-game {cls}">
    <h4><img src="../../icons/{icon}.png" alt="" width="20" height="20">{gname}<span class="bot-role">heute im Spiel</span></h4>
    <p>{html.escape(game_)}</p>
  </section>"""
    return f"""<li class="bot-card" id="{key}" style="--bot:#{col}">
  <div class="bot-head">
    {screen}
    <div class="bot-name"><h3>{name}</h3><div class="foe-tags"><span class="foe-kind">{label}</span></div></div>
  </div>
  <p>{world}</p>
  <p class="bot-unlock"><b>Wo:</b> {places}</p>{play}
</li>"""


def quirk_card(q):
    name, bot, does = q
    return f"""<li class="bot-card" style="--bot:#{COLORS[bot]}">
  <div class="bot-head">
    <div class="bot-screen"><img src="{BOTS}{bot.lower()}.png" width="80" height="96" alt="{bot}" loading="lazy"></div>
    <div class="bot-name"><h3>{name}</h3><a class="bot-family" href="../roboter/#{bot.lower()}">bringt {bot} mit</a></div>
  </div>
  <p class="bot-unlock"><b>Aus:</b> <a href="../welt/#{HOME_OF[bot]}">{PLACES[HOME_OF[bot]]["name"]}</a></p>
  <section class="bot-game bot-game-puzzle">
    <h4><img src="../../icons/bits-and-bolts.png" alt="" width="20" height="20">Bits &amp; Bolts<span class="bot-role">heute im Spiel</span></h4>
    <p>{html.escape(does)}</p>
  </section>
</li>"""


def stoer_grid(kind):
    return '        <ul class="bot-grid">\n' + "\n".join(stoer_card(k) for k, s in STOER.items() if s[0] == kind) + "\n        </ul>\n"

write("stoerungen", "Störungen", "Störungen im alten PC: oben auf der Platine wie Wetter, unten im Schrottschacht wie Getier. Keine Feinde, nur Ärgernisse.",
      head('<a href="../">Archiv 2.0</a> · Störungen', "Störungen",
           "In dieser Welt gibt es keine Feinde. Störungen gehören zu einem alten PC wie Wetter oder Ungeziefer: Sie sind lästig, manchmal anstrengend, aber nicht böse. "
           "Man vertreibt sie, man wartet sie ab, man räumt hinter ihnen auf.") + f"""
      <div class="callout wiki-note"><b>Oben Wetter, unten Getier.</b> Auf der Platine sind Störungen Zustände, die über eine Gegend ziehen: Flackern, Rauschen, Stromstöße. Das sind die Ereignisse aus Bits &amp; Bolts. Unten im Schacht sind es Wesen, die dort leben. Das sind die Gegner aus Bolt Buddies. Jede Schicht hat außerdem einen Wächter.</div>

      <section class="wiki-sec" id="wetter">
        <h2>Wetter auf der Platine</h2>
        <p>Jede Gegend hat ihr eigenes Wetter. Im Spiel ist ein Fluch dort in der Hälfte der Fälle ihr Wetter, sonst ein zufälliges Ereignis. Im Hauptrechner kommt alles zusammen.</p>
{stoer_grid("wetter")}      </section>

      <section class="wiki-sec" id="getier">
        <h2>Getier im Schacht</h2>
        <p>Bug, Spam-Drohne und Firewall gibt es überall im Schacht. Die anderen leben nur in ihrer Schicht.</p>
{stoer_grid("getier")}      </section>

      <section class="wiki-sec" id="waechter">
        <h2>Wächter</h2>
        <p>Jede Schicht hat einen Wächter, der sich dort breitgemacht hat. Wer ihn vertreibt, kommt künftig direkt bis zur nächsten Schicht.</p>
{stoer_grid("waechter")}      </section>

      <section class="wiki-sec" id="mitgebracht">
        <h2>Von Robotern mitgebracht</h2>
        <p>Manche Roboter bringen ihre eigene kleine Störung mit, je nachdem, wo sie herkommen. Das sind keine Störungen eines Ortes, sondern Eigenarten.</p>
        <ul class="bot-grid">
{chr(10).join(quirk_card(q) for q in QUIRKS)}
        </ul>
      </section>

      <section class="wiki-sec" id="ideen">
        <h2>Ideen {IDEA}</h2>
        <p>Für Orte, die noch keine eigene Störung haben. Noch in keinem Spiel.</p>
{stoer_grid("idee")}      </section>
""")


# ── Roboter ──────────────────────────────────────────────────────────────────
def bot_card(b):
    home = PLACES[HOME_OF[b]]["name"]
    if b == "BYTE":
        found = "war als Erster wach und wartet in der Werkstatt"
    else:
        found = f'<a href="../welt/#{SHAFT[HOME[b]]}">{PLACES[SHAFT[HOME[b]]]["name"]}</a>'
    return f"""<li class="bot-card" id="{b.lower()}" style="--bot:#{COLORS[b]}">
  <div class="bot-head">
    <div class="bot-screen"><img src="{BOTS}{b.lower()}.png" width="80" height="96" alt="{b}" loading="lazy"></div>
    <div class="bot-name"><h3>{b}</h3><span class="bot-say">„{html.escape(SAYS[b])}“</span></div>
  </div>
  <dl class="app-meta bot-world">
    <div><dt>Heimat</dt><dd><a href="../welt/#{HOME_OF[b]}">{home}</a></dd></div>
    <div><dt>Gefunden</dt><dd>{found}</dd></div>
    <div><dt>Andenken</dt><dd>{html.escape(KEEPSAKE[b])}</dd></div>
  </dl>
  <details class="bot-more"><summary>In den Spielen</summary>
    <p><b>Bits &amp; Bolts:</b> {html.escape(PUZZLE[b])}</p>
    <p><b>Bolt Buddies:</b> {html.escape(TRAIT[b][0].upper() + TRAIT[b][1:])}.</p>
  </details>
</li>"""

groups = []
for key, p in PLACES.items():
    if key not in HEIMAT:
        continue
    groups.append(f"""      <section class="wiki-sec">
        <h2>{p["name"]} <span class="muted-small">{p["part"]}</span></h2>
        <ul class="bot-grid">
{chr(10).join(bot_card(b) for b in HEIMAT[key])}
        </ul>
      </section>
""")
index = "".join(f'<a href="#{b.lower()}" style="--bot:#{COLORS[b]}"><img src="{BOTS}{b.lower()}.png" width="40" height="48" alt="" loading="lazy"><span>{b}</span></a>'
                for k in PLACES if k in HEIMAT for b in HEIMAT[k])
write("roboter", "Roboter", "Alle 22 Roboter in der Welt des alten PCs: Heimat, Fundort im Schrottschacht und Andenken.",
      head('<a href="../">Archiv 2.0</a> · Roboter', "Roboter",
           "Alle 22 Roboter, sortiert nach ihrer Heimat im PC, von oben nach unten. Ihre Namen kommen aus der Computersprache, und meist verraten sie schon, wo sie zu Hause sind.") + f"""
      <nav class="bot-index" aria-label="Roboter">{index}</nav>
      <div class="callout wiki-note">
        <b>Heimat und Fundort:</b> Jeder Roboter wohnt eigentlich irgendwo im PC. Als der PC ausging, sind aber alle in den Schrottschacht gefallen. Dort findet man sie in Bolt Buddies, je tiefer, desto später. Ihr Andenken stellen sie in der Werkstatt auf. <a href="../welt/#warum">Mehr dazu →</a>
      </div>
{"".join(groups)}""")
print("ok")
