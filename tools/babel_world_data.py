"""Die Welt BABEL: Orte im alten Tower-PC, ihre Formen in der Seitenansicht und die Heimat jedes Roboters.

Diese Datei ist die Quelle für die Welt (früher in make_archiv2.py). Sie wird gelesen von
Bits-and-Bolts/tools/babel_world.py, das daraus core/babel.gd für die Spiele schreibt.
"""

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
        name="Flachbandkabel", part="zwischen Platine und Laufwerken", game="Lines &amp; Loads · die Förderbänder",
        short="Brücken quer durchs Gehäuse.",
        look="Breite graue Bänder, die von der Platine hinüber zu den Laufwerken gespannt sind.",
        sound="Sie schwingen leise im Luftzug.",
        special="Wer mutig ist, balanciert darüber, statt den langen Weg zu nehmen. In den Laufwerken sind sie die Förderbänder der Fabrik: Was man darauflegt, wandert von selbst zur nächsten Maschine. PATCH verlegt sie."),
    "cd": dict(
        name="CD-Laufwerk", part="vorne oben, Nachbar der Werkstatt", game="Lines &amp; Loads · das zweite Laufwerk",
        short="Eine Schublade, die manchmal von selbst aufgeht.",
        look="Ein flacher Kasten mit Schublade. Drinnen liegt noch eine Scheibe, die im Licht in allen Regenbogenfarben schimmert.",
        sound="Still, bis die Scheibe anläuft. Dann heult es auf und vibriert durch die Wand bis in die Werkstatt.",
        special="Manchmal geht die Schublade von selbst auf und wieder zu, und keiner weiß, warum. Was auf der Scheibe ist, hat noch niemand herausgefunden. Seine Schublade ist die große Presse der Fabrik: Nur hier werden aus sehr guten Teilen Meisterstücke."),
    "werkstatt": dict(
        name="Werkstatt", part="vorne oben, leerer Laufwerksschacht", game="Bots &amp; Buddies · Zuhause",
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
        name="Festplatte", part="vorne im Laufwerkskäfig", game="Lines &amp; Loads · das erste Laufwerk",
        short="Eine alte Scheibe, die sich dreht.",
        look="Ein schwerer Kasten, darin eine spiegelnde Scheibe, über die ein Lesearm schwingt.",
        sound="Ruhig, bis die Scheibe anläuft. Dann surrt und klackert es.",
        special="Alles, was je gespeichert wurde, liegt hier in endlosen Spuren, wie in einer Bibliothek. Anders als der Hauptrechner bewahrt sie Dinge auf, keine Erinnerungen. Beim Neustart ist sie nur halb erwacht. Die Fabrik liefert ihr Teil für Teil, was sie braucht, bis sie wieder läuft. Dann kehren ASKI und MIRA nach Hause zurück."),
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
        name="Schraubenhalde", part="Schacht · gleich unter der Werkstatt", game="Bots &amp; Buddies",
        short="Hier liegt, was zuletzt gefallen ist.", img="layer_0.png",
        look="Ein Hang aus Schrauben, Klammern und Krümeln, der sich zwischen Platine und Laufwerken gesammelt hat.",
        sound="Von oben fällt noch etwas Licht. Bei jedem Schritt klimpern Schrauben.",
        special="Hier liegen die meisten Verlorenen, weil sie nicht tief gefallen sind."),
    "kabelsalat": dict(
        name="Kabelsalat", part="Schacht · unter der Platine", game="Bots &amp; Buddies",
        short="Ein Dschungel aus alten Kabeln.", img="layer_1.png",
        look="Dicke Kabelstränge hängen kreuz und quer, verknotet und mit Kabelbindern zusammengezurrt. Dazwischen hängen Staubfäden wie Lianen.",
        sound="Dämmrig, ab und zu blitzen Funken. Es knistert überall.",
        special="Man verläuft sich leicht. Die Kabel führen überallhin, auch dorthin, wo seit Jahren keiner mehr war."),
    "lueftergrund": dict(
        name="Lüftergrund", part="Schacht · vor dem Frontlüfter", game="Bots &amp; Buddies",
        short="Kalt und windig, Staubflusen treiben wie Schnee.", img="layer_2.png",
        look="Der Boden vor dem Gehäuselüfter. Staubflusen treiben wie Schnee, die Wände sind mit grauem Flaum bedeckt.",
        sound="Kühles, blasses Licht. Der Lüfter rauscht gleichmäßig wie Wind.",
        special="Es ist immer windig und kalt. Wer zu lange bleibt, wird langsam."),
    "netzteil": dict(
        name="Netzteil", part="Schacht · ganz unten", game="Bots &amp; Buddies",
        short="Ganz unten brummt und glüht es.", img="layer_3.png",
        look="Ein Blechkasten ganz unten, durch die Lüftungsschlitze glüht es orange. Drinnen stehen Spulen und Kondensatoren wie Türme.",
        sound="Rot und warm. Ein tiefes Brummen, das man im Bauch spürt.",
        special="Von hier kommt der ganze Strom. Die ältesten und eigenwilligsten Roboter wohnen hier und mögen die Hitze, für Besucher ist es anstrengend."),
}


## Form jedes Orts in der Seitenansicht (672x922): ("r", x, y, w, h), ("c", x, y, r) oder ("p", "x,y x,y ..."),
## dazu die Zeilen der Beschriftung, ihr Mittelpunkt und ob sie gedreht ist.
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
assert sorted(SHAPES) == sorted(PLACES), "jeder Ort braucht eine Form"


## Heimat jedes Roboters. Gefunden wird er trotzdem im Schacht (Bots & Buddies).
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

## Welches Spiel an welchem Ort spielt (bnb Bits & Bolts, aa Amps & Arcs, bb Bots & Buddies, ll Lines & Loads,
## ee Echoes & Encores). Orte ohne Eintrag sind noch in keinem Spiel.
GAME = {
    "steckkarten": "bnb", "knopfzelle": "bnb", "chipsatz": "bnb", "arbeitsspeicher": "bnb", "hauptrechner": "bnb",
    "anschluesse": "aa", "netzwerkkarte": "aa", "soundkarte": "aa", "grafikkarte": "aa",
    "werkstatt": "bb", "schicht1": "bb", "kabelsalat": "bb", "lueftergrund": "bb", "netzteil": "bb",
    "flachband": "ll", "cd": "ll", "festplatte": "ll",
    "lautsprecher": "ee",
}
