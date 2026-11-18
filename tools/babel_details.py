"""Ausführliche Abschnitte für die Seiten von Bits & Bolts und Bots & Buddies im Bereich B.A.B.E.L.

Wird von make_babel.py benutzt. Roboter, Gegner und Bilder aus Bots & Buddies liegen fest in babel/img/,
copy_images() holt nur die Bildschirmfotos aus dem Ordner Bits-and-Bolts daneben.
"""
import os

from archiv_data import ORDER, BASE, TRAIT, PUZZLE, UNLOCK, ROLE, ATTR, LAYERS, HOME, KEEPSAKE, COLORS, SAYS

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
IMG = os.path.join(OUT, "babel", "img")


## Gegner aus Bots & Buddies (früher in make_archiv.py)
FOES = [
    ("bug", "Bug", "Gegner", "FF5252", 12, 3, 14, 3, 3, "ab Kampf 1", "alle Ebenen",
     "Der häufigste Gegner. Schwach, aber oft in Gruppen. Steht vorn.", False, "Rückt in der Formation vor."),
    ("drone", "Spam-Drohne", "Gegner", "B46CFF", 9, 4, 13, 4, 3, "ab Kampf 2", "alle Ebenen",
     "Fliegt über die vorderen Reihen hinweg und zielt auf den hintersten Roboter.", False, "Fliegt mit und wirft Bomben."),
    ("turret", "Firewall", "Gegner", "FF5252", 12, 8, 8, 6, 6, "ab Kampf 3", "alle Ebenen",
     "Langsam, schießt aber wild und hart auf irgendwen im Team.", False, "Schießt auf zufällige Blöcke."),
    ("worm", "Rostwurm", "Gegner", "D9773A", 34, 7, 7, 6, 6, "ab Kampf 4", "alle Ebenen, im Kabelsalat und im Netzteil doppelt so oft",
     "Zäh und gepanzert (1 Panzerung). Hält lange durch.", False, "Braucht mehrere Treffer."),
    ("frost", "Frostbug", "Gegner", "4DE8FF", 16, 4, 11, 5, 5, "ab Kampf 21", "Lüftergrund (vor allem), Netzteil",
     "Seine Treffer kühlen ab: Wer getroffen wird, ist später wieder dran.", True, ""),
    ("spark", "Wackelkontakt", "Gegner", "FF9A3D", 11, 4, 16, 5, 5, "ab Kampf 11", "Kabelsalat (vor allem), Lüftergrund, Netzteil",
     "Schnell und geladen: Wer ihn trifft, bekommt einen Schlag zurück, der tiefer im Schacht stärker wird.", True, ""),
    ("heat", "Überhitzer", "Gegner", "FF5252", 18, 6, 9, 7, 7, "ab Kampf 31", "Netzteil (vor allem)",
     "Strahlt Hitze ab und trifft das ganze Team zugleich, jeden mit 60 % seines Schadens.", True, ""),
    ("boss", "Bluescreen", "Boss", "3B6BFF", 80, 8, 9, 25, 25, "Kampf 5, 10, 15",
     "Mitte von Schraubenhalde und Kabelsalat (dort mit Wackelkontakten), Wächter der Schraubenhalde, im Netzteil im Wechsel",
     "Trifft das ganze Team zugleich. Hinterlässt ein seltenes Teil und einen Akku.", False, "Boss-Welle alle 5 Wellen."),
    ("short", "Kurzschluss", "Wächter", "FFB000", 75, 9, 14, 30, 30, "Kampf 20, 25",
     "Wächter des Kabelsalats, Boss in der Mitte des Lüftergrunds, im Netzteil im Wechsel",
     "Schnell, schlägt wild um sich und landet viele Volltreffer (25 %). Kommt mit Wackelkontakt und Spam-Drohne.", True, ""),
    ("chiller", "Kältekern", "Wächter", "4DE8FF", 95, 7, 8, 35, 35, "Kampf 30, 35",
     "Wächter des Lüftergrunds, Boss in der Mitte des Netzteils, dort auch im Wechsel",
     "Trifft das ganze Team und kühlt alle zugleich ab. Kommt mit Frostbug und Bug.", True, ""),
    ("trafo", "Brummtrafo", "Wächter", "FF7A45", 110, 7, 7, 40, 40, "Kampf 40, danach im Wechsel",
     "Wächter des Netzteils, dort im Wechsel mit den anderen drei",
     "Brummt so laut, dass er das ganze Team zugleich trifft. Wer ihn trifft, verbrennt sich: 3 Schaden zurück. Kommt mit Überhitzer und Frostbug.", True, ""),
]

SHOTS = [("01", "22 Roboter, jeder mit eigener Regel"), ("02", "Nur Nullen und Einsen"), ("03", "Tipps erklären statt verraten"),
         ("04", "Spiegel, Hex, Pixel und mehr"), ("05", "Ereignisse wie der Nebel"), ("06", "10 Etagen bis zum Hauptrechner"),
         ("07", "Der Hauptrechner"), ("08", "Roboter wählen")]


def copy_images():
    os.makedirs(os.path.join(IMG, "bots"), exist_ok=True)
    os.makedirs(os.path.join(IMG, "foes"), exist_ok=True)
    # Roboter, Gegner und Bilder aus Bots & Buddies liegen fest in babel/img (bots/, foes/, bb_*.png)
    # Bildschirmfotos aus dem Store, verkleinert
    src = os.path.join(OUT, "..", "Bits-and-Bolts", "store", "de", "screenshots")
    if os.path.isdir(src):
        from PIL import Image
        for key, _ in SHOTS:
            p = os.path.join(src, key + ".png")
            if os.path.exists(p):
                Image.open(p).convert("RGB").resize((360, 720), Image.LANCZOS).save(os.path.join(IMG, "bnb_" + key + ".jpg"), quality=82)


def table(head, rows, cls=""):
    th = "".join(f"<th>{h}</th>" for h in head)
    tr = "\n".join("        <tr>" + "".join(f"<td>{c}</td>" for c in r) + "</tr>" for r in rows)
    return f'<div class="babel-table-wrap"><table class="babel-table{cls}">\n        <thead><tr>{th}</tr></thead>\n        <tbody>\n{tr}\n        </tbody>\n      </table></div>'


def bot_img(b, size=40):
    return f'<img class="pix" src="../img/bots/{b.lower()}.png" alt="" width="{size}" height="{int(size * 1.2)}" loading="lazy">'


# ── Bits & Bolts ─────────────────────────────────────────────────────────────
def bits_and_bolts():
    shots = "\n".join(f'        <figure><img src="../img/bnb_{k}.jpg" alt="{t}" width="180" height="360" loading="lazy"><figcaption>{t}</figcaption></figure>'
                      for k, t in SHOTS)
    bots = "\n".join(
        f'        <li class="babel-bot" style="--bc:#{COLORS[b]}">{bot_img(b)}<div><b>{b}</b> <span class="babel-tag">{ROLE[b]}</span>'
        f'<p>{PUZZLE[b]}</p><small>{"Von Anfang an dabei" if b == "BYTE" else "Frei " + UNLOCK[b]}</small></div></li>'
        for b in ORDER)
    return f"""
    <h2>Bilder</h2>
    <div class="babel-shots">
{shots}
    </div>

    <h2>Die Regeln</h2>
    <p>Immer gilt:</p>
    <ol class="babel-list">
      <li>Jede Zelle bekommt eine 0 oder eine 1.</li>
      <li>Nie drei gleiche Ziffern direkt nebeneinander oder untereinander.</li>
      <li>Jede Zeile und jede Spalte hat gleich viele Nullen und Einsen.</li>
    </ol>
    <p>Nur wenn ein Rätsel es anzeigt: Keine zwei Zeilen und keine zwei Spalten sind gleich (Einzigartig), und Zeichen zwischen Zellen: <code>=</code> heißt gleich, <code>×</code> heißt verschieden. Jedes Rätsel hat genau eine Lösung und lässt sich ohne Raten lösen.</p>
    <p><b>Zahlensysteme:</b> Zeigt ein Rätsel Oktal-, Hex- oder ASCII-Hinweise, stehen über den Spalten die Stellenwerte (4 2 1, 8 4 2 1 oder alle Zweierpotenzen). Umrechnen im Kopf ist nicht nötig.</p>
    <p><b>Bedienung:</b> nach oben wischen setzt eine 1, nach unten eine 0, Tippen setzt eine Notiz. Erst das Loslassen trägt ein, Zurückziehen bricht ab.</p>

    <h2>Ein Run</h2>
    <ul class="babel-list">
      <li><b>Kurzschluss:</b> Eine falsche Ziffer wird nicht eingetragen, sie kostet eine Ladung, und BYTE sagt, warum sie falsch war. Ist der Akku leer, ist der Run vorbei.</li>
      <li><b>Ladung und Tipps</b> hängen am Roboter, BYTE hat 5 Ladungen und 3 Tipps. Tipps erklären den nächsten Schritt, statt die Lösung zu verraten.</li>
      <li><b>10 Etagen:</b> 7 Rätsel, 2 Zwischenrechner (Etage 4 und 7, schwerer, mit Ereignis, danach +2 Ladung oder +1 Tipp) und oben der Hauptrechner mit 1 bis 4 Sektoren.</li>
      <li><b>Gastroboter:</b> Die ersten zwei Etagen kommen vom gewählten Roboter, danach mischen andere freigeschaltete Roboter mit ihren Regeln mit.</li>
      <li>Ein unterbrochener Run geht genau so weiter, mit derselben Karte und denselben Rätseln.</li>
    </ul>

    <h2>Der Weg nach oben</h2>
    {table(["Etage", "Gegend", "Wetter dort"], [
        ["1–2", "Steckkarten", "Wackelkontakt: Immer wieder wackelt eine deiner Ziffern. Tippst du sie schnell an, sitzt sie wieder fest, sonst erlischt sie."],
        ["3–4", "Knopfzelle", "Stromausfall: Nach einem Countdown erlöschen die Vorgaben. Wer vorher eine Ziffer daneben setzt, hält sie an."],
        ["5–7", "Chipsatz", "Überspannung: Ein Kurzschluss kostet 2 Ladungen statt 1."],
        ["8–9", "Arbeitsspeicher", "Störsignal: Immer wieder rauscht ein Feld aus vier Zellen ein paar Sekunden lang. Dort siehst du nichts und kannst nichts eintragen."],
        ["10", "Hauptrechner", "Alles kommt zusammen. Jeder Sektor bringt eine Erinnerung zurück."],
    ])}
    <p>Dazu bringen vier Roboter ihre eigenen Ereignisse mit: <b>Falsche Vorgabe</b> (ERROR, Suchen kostet nichts), <b>Ansteckung</b> (VIRUS), <b>Zeitdruck</b> (DAEMON) und <b>Nebel</b> (MORSE).</p>

    <h2>Sechs Stufen</h2>
    <p>Jeder Sieg öffnet die nächste Stufe. Die Stufe ändert nicht Ladung und Tipps, sie macht die Rätsel schwerer.</p>
    {table(["Stufe", "Was dazukommt"], [
        ["0", "nur 6×6, leichtere Rätsel, 1 Regel je Rätsel, keine Ereignisse"],
        ["1", "bis 2 Regeln je Rätsel, 1 Ereignis bei den Rechnern"],
        ["2", "Rätsel ohne Erleichterung, Sensoren"],
        ["3", "Ereignisse und schwerere Rätsel ab Etage 4, bis 3 Regeln, Einzigartig, 2 Ereignisse im Hauptrechner"],
        ["4", "schwerere Rätsel ab Etage 5, 8×8 ab Etage 6, Hauptrechner in 8×8"],
        ["5", "schwerere Rätsel, 8×8 ab Etage 4, Ereignisse ab Etage 3, bis 2 Ereignisse je Rätsel, bis 4 Regeln, stärkerer Hauptrechner"],
    ])}

    <h2>Die 22 Roboter</h2>
    <p>Jeder Roboter bringt einen Hinweis, eine Zusatzregel, ein Ereignis oder eine Fähigkeit mit. Die ersten sechs kommen mit den Siegen, alle anderen schaltet frei, was man gespielt hat.</p>
    <ul class="babel-bots">
{bots}
    </ul>

    <h2>Erinnerungen und Archiv</h2>
    <ul class="babel-list">
      <li><b>66 Erinnerungen:</b> Der Hauptrechner ist das Gedächtnis des PCs. Jeder gelöste Sektor bringt eine Erinnerung des Roboters zurück, von dem er stammt, drei je Roboter.</li>
      <li><b>24 Errungenschaften</b> im Spiel, ohne Konto. Wer mag, meldet sie zusätzlich bei Google Play Games.</li>
      <li><b>Üben</b> in 6×6 und 8×8, auch mit mehreren Robotern zugleich, und ein Verlauf aller Runs.</li>
      <li>Deutsch und Englisch, Töne und Musik im 8-Bit-Stil, alles abschaltbar. Keine Werbung, kein Konto, kein Internet nötig.</li>
    </ul>
"""


# ── Bots & Buddies ───────────────────────────────────────────────────────────
def bots_and_buddies():
    layers = [("Schraubenhalde", "1–10", "die vier ersten Gegner gleich oft", "Bluescreen", "Bluescreen"),
              ("Kabelsalat", "11–20", "vor allem Wackelkontakte, Rostwürmer doppelt", "Bluescreen mit Wackelkontakten", "Kurzschluss"),
              ("Lüftergrund", "21–30", "vor allem Frostbugs", "Kurzschluss", "Kältekern"),
              ("Netzteil", "ab 31", "vor allem Überhitzer, dazu alles gemischt", "Kältekern", "Brummtrafo")]
    layer_figs = "\n".join(
        f'        <figure><img class="pix" src="../img/bb_layer_{i}.png" alt="{n}" width="320" height="180" loading="lazy">'
        f'<figcaption><b>{n}</b> · Kampf {k}</figcaption></figure>' for i, (n, k, *_) in enumerate(layers))
    foes = "\n".join(
        f'        <li class="babel-foe" style="--bc:#{f[3]}"><img class="pix" src="../img/foes/{f[0]}.png" alt="" width="48" height="48" loading="lazy">'
        f'<div><b>{f[1]}</b> <span class="babel-tag">{f[2]}</span><p>{f[11]}</p><small>{f[9]} · {f[10]}</small></div></li>'
        for f in FOES)
    stations = [("dock", "Ladeleiste", "Schlafende laden 35 / 70 / 100 % schneller", "60 / 180 / 450"),
                ("bath", "Ölbad", "Pflege sinkt 15 / 30 / 45 % langsamer", "60 / 180 / 450"),
                ("play", "Spielecke", "Laune sinkt 15 / 30 / 45 % langsamer", "60 / 180 / 450"),
                ("bench", "Werkbank", "zerlegen und aufwerten, dann 25 und 50 % günstiger", "80 / 200 / 450"),
                ("lift", "Aufzug", "2 und 3 Aufträge gleichzeitig", "250 / 600"),
                ("radio", "Funkantenne", "kommt mit der Verbindung zu den anderen Spielen", "–")]
    st = "\n".join(f'        <li><img class="pix" src="../img/bb_station_{k}.png" alt="" width="180" height="69" loading="lazy">'
                   f'<div><b>{n}</b><p>{d}</p><small>{p + " Schrauben" if p != "–" else "noch nicht zu bauen"}</small></div></li>' for k, n, d, p in stations)
    bots = "\n".join(
        f'        <li class="babel-bot" style="--bc:#{COLORS[b]}">{bot_img(b)}<div><b>{b}</b> <span class="babel-tag">„{SAYS[b]}“</span>'
        f'<p>{TRAIT[b][0].upper() + TRAIT[b][1:]}.</p>'
        f'<small>{" · ".join(f"{a[:3]} {v}" for a, v in zip(ATTR, BASE[b]))}<br>'
        f'{"Von Anfang an dabei" if b == "BYTE" else "Wartet in: " + LAYERS[HOME[b]][0]} · Bringt mit: {KEEPSAKE[b]}</small></div></li>'
        for b in ORDER)
    return f"""
    <figure class="babel-hero-img"><img class="pix" src="../img/bb_workshop.png" alt="Die Werkstatt mit Robotern" width="900" height="600" loading="lazy">
      <figcaption>Die Werkstatt: Lochwand, Aufzugstür, Teileregal und die Ladeleiste.</figcaption></figure>

    <h2>Die Werkstatt</h2>
    <p>Alle geretteten Roboter laufen frei in der Werkstatt herum. Jeder bringt ein persönliches Teil mit, das danach an seinem festen Platz steht: OKTA ein Aquarium, HEXA einen Snackautomaten, DAEMON eine Kaffeemaschine. So füllt sich die Werkstatt mit jedem Roboter. Antippen wählt einen aus, nochmal antippen streichelt ihn.</p>
    {table(["Wert", "sinkt", "steigt durch"], [
        ["Energie", "1 Punkt in 6 Minuten", "Akku (+35), Schlafen an der Ladeleiste"],
        ["Laune", "1 Punkt in 5 Minuten, rostig doppelt so schnell", "Spielen, Streicheln, Expeditionen"],
        ["Pflege", "1 Punkt in 8 Minuten", "Ölkanne (+40)"],
    ])}
    <p>Die Werte sinken auch, wenn das Spiel zu ist, höchstens für 48 Stunden. Ist der Akku leer, schaltet der Roboter ab und lädt. Kaputt geht nichts.</p>

    <h2>Ausbau</h2>
    <p>Stationen kosten Schrauben, stehen sichtbar im Raum und machen die Pflege leichter, aber nie überflüssig. Alles zusammen kostet 3650 Schrauben, das reicht für etwa ein bis zwei Wochen Spielen.</p>
    <ul class="babel-stations">
{st}
    </ul>

    <h2>Ausrüstung</h2>
    {table(["Attribut", "wirkt auf"], [["Leistung", "Schaden"], ["Takt", "Tempo und Ausweichen"], ["Logik", "Volltreffer"], ["Gehäuse", "Leben"]])}
    <ul class="babel-list">
      <li>Drei Plätze: <b>Waffe</b>, <b>Rüstung</b>, <b>Chip</b>, in vier Seltenheiten: Schrott, solide, selten, legendär.</li>
      <li>An der Werkbank lassen sich Teile zerlegen oder eine Seltenheit höher aufwerten.</li>
      <li>Im Shop gibt es Akkus, Öl, Schrottkisten, Tresorkisten und Trainingsdaten.</li>
      <li>Der Zustand zählt im Kampf: Gut gepflegte Roboter haben mehr Leben, mehr Volltreffer und weichen öfter aus.</li>
    </ul>

    <h2>Expeditionen</h2>
    <ul class="babel-list">
      <li>Ein Team aus bis zu drei Robotern kämpft sich Kampf für Kampf tiefer. Die Kämpfe laufen von selbst, entschieden wird davor und dazwischen.</li>
      <li><b>Nach jedem Sieg</b> eine von drei Belohnungen: ein Modul fürs Team, ein Teil für zuhause, oder Reparatur und Vorräte.</li>
      <li><b>Rettung:</b> Nach Kampf 2, 5, 8 und so weiter wird ein Roboter gerettet, jeder wartet in seiner Ebene.</li>
      <li><b>Aufzug:</b> weiter oder mit der ganzen Beute heim. Der nächste Kampf ist schon zu sehen, dazu gibt es einen Nebenschacht mit zäheren Gegnern und mehr Schrauben.</li>
      <li><b>Haltestellen:</b> Wer den Wächter einer Ebene besiegt, kann später direkt in der nächsten einsteigen.</li>
      <li>Fällt das ganze Team aus, bleibt die halbe Beute liegen. Gerettete Roboter und Erfahrung bleiben immer.</li>
    </ul>

    <h2>Die vier Ebenen</h2>
    <div class="babel-layers">
{layer_figs}
    </div>
    {table(["Ebene", "Kämpfe", "Gegner", "Boss in der Mitte", "Wächter"], [list(l) for l in layers])}

    <h2>Gegner</h2>
    <p>Keine Feinde mit Absicht, sondern Getier, das im Schacht wuchert, wo kein Roboter wohnt.</p>
    <ul class="babel-bots babel-foes">
{foes}
    </ul>

    <h2>Teams, Aufträge und Tagesschacht</h2>
    <ul class="babel-list">
      <li><b>Teams:</b> Bis zu sechs Teams aus je drei Robotern. Genau eins ist aktiv und lebt in der Werkstatt, die anderen ruhen bei ihren persönlichen Teilen.</li>
      <li><b>Aufträge:</b> Ein ruhendes Team geht für 1, 4, 8 oder 12 Stunden allein los und kommt mit Beute und Erfahrung zurück.</li>
      <li><b>Tagesschacht:</b> Einmal am Tag eine Expedition mit fester Vorgabe: keine Reparatur, allein, Glaskanonen oder Schatzsuche. Danach gibt es immer ein Teil.</li>
      <li><b>Erinnerungen:</b> Auf Wunsch meldet sich das Spiel, wenn ein Roboter etwas braucht oder ein Team zurück ist. Standardmäßig aus, höchstens eine am Tag.</li>
    </ul>

    <h2>Die 22 Roboter</h2>
    <p>Jeder verteilt 12 Punkte anders auf Leistung, Takt, Logik und Gehäuse und hat eine Eigenheit im Kampf. Gerettet wird jeder in seiner Ebene.</p>
    <ul class="babel-bots">
{bots}
    </ul>
"""


# ── Amps & Arcs ──────────────────────────────────────────────────────────────
AA_SHOTS = [("01", "Der Gang hinter dem Roboter"), ("02", "Torwächter Wackelstecker"), ("03", "Einbauen: Schaltung und Überladung"),
            ("04", "Ausgebaut: Laser und Salve"), ("05", "Roboter wählen"), ("06", "VIRUS in der Soundkarte"),
            ("07", "Errungenschaften"), ("08", "Ergebnis eines Runs")]
AA_FAMILIES = [
    ("Prozesse", "3DFF7A", "Takt", "Nach jedem entstörten Rauschen feuern die Waffen eine Sekunde lang schneller.",
     [("BYTE", "Blaster", "Fernkampf", "Einzelschüsse auf das nächste Rauschen."),
      ("LOOP", "Schleife", "Nahkampf", "Kugeln kreisen um ihn und schwingen hinaus."),
      ("MORSE", "Funkspruch", "Fernkampf", "Punkt, Punkt, Strich, der Strich schlägt durch alles."),
      ("SHIFT", "Bitschieber", "Streuung", "Schnelle Schüsse, Bit für Bit über die ganze Breite geschoben."),
      ("DAEMON", "Hintergrunddienst", "Fernkampf", "Drohnen schweben vor ihm und schießen selbst."),
      ("ROOT", "Wurzelbeben", "Nahkampf", "Eine breite Welle läuft vor ihm durch die Leitung.")]),
    ("Zahlensysteme", "FF9E2C", "Präzision", "Mehr Volltreffer, und jeder Volltreffer sprüht Funken auf ein Rauschen daneben.",
     [("OKTA", "Oktett", "Streuung", "Acht Schüsse im Ring um ihn herum."),
      ("PIXA", "Pixelstreuung", "Streuung", "Ein Fächer aus Pixeln mit kurzer Reichweite."),
      ("HEXA", "Hexschuss", "Fernkampf", "Ein sehr starker Schuss auf das zäheste Rauschen."),
      ("ASKI", "Zeilenumbruch", "Fernkampf", "Ein Zeichen fliegt hinaus und trifft auf dem Rückweg noch einmal."),
      ("CHROMA", "Prisma", "Streuung", "Farbige Strahlen im Fächer."),
      ("NIBBLE", "Knabbern", "Nahkampf", "Beißt schnell in das nächste Rauschen.")]),
    ("Logikgatter", "FFD34D", "Panzerung", "Jeder Treffer gegen dich wird kleiner, Funken der Torwächter noch mehr.",
     [("GATE", "Schlagbaum", "Nahkampf", "Schwingt vorn einen Balken durch alles."),
      ("XOR", "Kreuzfeuer", "Fernkampf", "Schüsse schräg nach vorn, die sich kreuzen."),
      ("NULL", "Nullfeld", "Nahkampf", "Ein Feld um ihn trifft alles, was hineinkommt."),
      ("PARI", "Paritätsbogen", "Fernkampf", "Ein Blitz springt durch mehrere Rauschen."),
      ("QUBIT", "Überlagerung", "Streuung", "Schüsse tauchen direkt vor dem Rauschen auf."),
      ("MIRA", "Spiegelschuss", "Fernkampf", "Schüsse prallen von den Wänden ab.")]),
    ("Störenfriede", "FF5252", "Rost", "Jeder Treffer rostet nach, ein Viertel des Schadens kommt noch dazu.",
     [("VIRUS", "Ansteckung", "Fernkampf", "Sporen rosten stark nach, der Rost springt beim Entstören weiter."),
      ("ERROR", "Absturz", "Nahkampf", "Regelmäßig eine Explosion um ihn herum."),
      ("GLITCH", "Bildfehler", "Streuung", "Sehr schnelle Schüsse in zufällige Richtungen."),
      ("PATCH", "Flicken", "Fernkampf", "Langsame Flicken, die im Ring explodieren.")]),
]
AA_NOISE = [
    ("Anschlüsse", "FF5252", ["flea", "dust", "crack"], "boss", "Wackelstecker"),
    ("Netzwerkkarte", "4DA8FF", ["louse", "ping"], "storm", "Paketsturm"),
    ("Soundkarte", "FF5CF0", ["hummer"], "feedback", "Rückkopplung"),
    ("Grafikkarte", "4DE8FF", ["pixel", "stripe"], "artifact", "Artefakt"),
]
AA_NOISE_NAMES = {"flea": "Funkenfloh", "dust": "Staubflocke", "crack": "Knackser", "louse": "Paketlaus", "ping": "Ping",
                  "hummer": "Brummer", "pixel": "Pixelfehler", "stripe": "Streifen"}


def copy_amps_images():
    """Bildschirmfotos und Rauschen aus dem Ordner Amps-and-Arcs daneben."""
    from PIL import Image
    src = os.path.join(OUT, "..", "Amps-and-Arcs")
    shots = os.environ.get("AA_SHOTS", "")
    if shots and os.path.isdir(shots):
        for key, _ in AA_SHOTS:
            p = os.path.join(shots, "aa_" + key + ".png")
            if os.path.exists(p):
                Image.open(p).convert("RGB").resize((360, 780), Image.LANCZOS).save(os.path.join(IMG, "aa_" + key + ".jpg"), quality=82)
    noise = os.path.join(src, "assets", "noise")
    os.makedirs(os.path.join(IMG, "aa_noise"), exist_ok=True)
    for sec in AA_NOISE:
        for kind in sec[2] + [sec[3]]:
            p = os.path.join(noise, kind + ".png")
            if os.path.exists(p):
                im = Image.open(p).convert("RGBA")
                im.resize((im.width * 3, im.height * 3), Image.NEAREST).save(os.path.join(IMG, "aa_noise", kind + ".png"))


def amps_and_arcs():
    shots = "\n".join(f'        <figure><img src="../img/aa_{k}.jpg" alt="{t}" width="180" height="390" loading="lazy"><figcaption>{t}</figcaption></figure>'
                       for k, t in AA_SHOTS)
    fams = ""
    for name, col, trait, text, bots in AA_FAMILIES:
        items = "\n".join(
            f'        <li class="babel-bot" style="--bc:#{col}">{bot_img(b)}<div><b>{b}</b> <span class="babel-tag">{w} · {k}</span>'
            f'<p>{t}</p></div></li>' for b, w, k, t in bots)
        fams += f"""
    <h3 style="color:#{col}">{name} · {trait}</h3>
    <p>{text}</p>
    <ul class="babel-bots">
{items}
    </ul>
"""
    noise = ""
    for name, col, kinds, boss, boss_name in AA_NOISE:
        items = "".join(
            f'<li class="babel-foe" style="--bc:#{col}"><img class="pix" src="../img/aa_noise/{k}.png" alt="" loading="lazy"><div><b>{AA_NOISE_NAMES[k]}</b></div></li>'
            for k in kinds)
        items += f'<li class="babel-foe" style="--bc:#{col}"><img class="pix" src="../img/aa_noise/{boss}.png" alt="" loading="lazy"><div><b>{boss_name}</b> <span class="babel-tag">Torwächter</span></div></li>'
        noise += f"""
    <h3 style="color:#{col}">{name}</h3>
    <ul class="babel-bots">{items}</ul>
"""
    return f"""
    <h2>Bilder</h2>
    <div class="babel-shots">
{shots}
    </div>

    <h2>Ein Run im Detail</h2>
    <ul class="babel-list">
      <li><b>Hinter dem Roboter:</b> Er läuft von selbst durch einen Gang aus Leiterbahnen, der Daumen steuert nur nach links und rechts. Gefeuert wird von selbst.</li>
      <li><b>Ein Run</b> führt durch vier Abschnitte, je etwa zwei Minuten. Am Ende jedes Abschnitts wartet ein Torwächter, danach lädt der Akku etwas auf.</li>
      <li><b>Schrott</b> aus entstörtem Rauschen füllt eine Leiste. Ist sie voll, wird eins aus drei Angeboten eingebaut.</li>
      <li><b>Ausgefallen</b> ist der Roboter, wenn sein Akku leer ist. Die Rüstung macht jeden Treffer schwächer.</li>
    </ul>

    <h2>Die vier Abschnitte</h2>
    <p>Jeder Abschnitt hat eigenes Rauschen, spätere mischen das ältere mit.</p>
{noise}

    <h2>Einbauen</h2>
    <ul class="babel-list">
      <li><b>Bauteile</b> wachsen von Stufe I bis V, höchstens fünf verschiedene pro Run: Kondensator, Spule, Lüfter, Widerstand, Diode, Quarz, Sicherung, Kühlkörper.</li>
      <li><b>Familienbauteile</b> nur für die eigene Familie: Taktgeber, Rechenwerk, Schutzschaltung, Säure.</li>
      <li><b>Schaltungen:</b> Zwei Bauteile auf höchster Stufe verschmelzen. Blitzring, Laser, Kühlkreislauf, Schmelzsicherung.</li>
      <li><b>Überladungen:</b> Jede Waffe hat eine Endform, wenn sie auf Mk III ist und ihr Partner-Bauteil auf Stufe III, zum Beispiel die Salve des Blasters oder die Seuche von VIRUS.</li>
      <li><b>Schrott ausgeben:</b> neu würfeln oder eine Karte für später sperren. Einmal pro Run kommt die Waffe eines anderen Roboters als Zweitwaffe dazu.</li>
    </ul>

    <h2>Sechs Stufen</h2>
    <p>Wie in Bits &amp; Bolts: Ein Sieg auf einer Stufe öffnet die nächste, mit jedem Roboter.</p>
    {table(["Stufe", "Was dazukommt"], [
        ["0", "Weniger und schwächeres Rauschen"],
        ["1", "Normal"],
        ["2", "Rauschen ist zäher"],
        ["3", "Goldenes Elite-Rauschen: dreimal so zäh, dreimal so viel Schrott"],
        ["4", "Dichter, und die Torwächter halten mehr aus"],
        ["5", "Alles schneller, Berührungen schmerzen mehr"],
    ])}

    <h2>Die 22 Roboter in vier Familien</h2>
    <p>Die Familien kommen aus Bots &amp; Buddies, jede bringt eine Eigenschaft mit. Jeder Roboter hat seine eigene Waffe, die Art (Nahkampf, Fernkampf oder Streuung) zeigt, wie sie trifft. BYTE ist von Anfang an da, alle anderen schaltet frei, was man spielt.</p>
{fams}
    <h2>Dazu</h2>
    <ul class="babel-list">
      <li><b>19 Errungenschaften</b> und eine Statistik über alle Runs, ohne Konto.</li>
      <li><b>Üben</b> einzelner Abschnitte, ein Archiv mit Robotern, Rauschen und allem, was man gebaut hat, und ein Verlauf.</li>
      <li>Eine kurze Einführung im ersten Run, Töne im 8-Bit-Stil, Vibration, alles abschaltbar.</li>
    </ul>
"""


EXTRA = {"bits-and-bolts": bits_and_bolts, "bots-and-buddies": bots_and_buddies, "amps-and-arcs": amps_and_arcs}


def extra(slug):
    return EXTRA[slug]() if slug in EXTRA else ""
