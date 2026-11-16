"""Ausführliche Abschnitte für die Seiten von Bits & Bolts und Bots & Buddies im Bereich B.A.B.E.L.

Wird von make_babel.py benutzt. Bilder kopiert copy_images() nach babel/img/: Roboter, Gegner und Werkstatt aus den alten
Archiv-Ordnern (die Dateien liegen dort weiter), Bildschirmfotos aus dem Ordner Bits-and-Bolts daneben.
"""
import ast
import os
import shutil

from archiv_data import ORDER, BASE, TRAIT, PUZZLE, UNLOCK, ROLE, ATTR, LAYERS, HOME, KEEPSAKE, COLORS, SAYS

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
IMG = os.path.join(OUT, "babel", "img")


def _foes():
    """Liest FOES aus make_archiv.py, ohne es auszuführen (das würde die Archive wiederherstellen)."""
    src = open(os.path.join(os.path.dirname(__file__), "make_archiv.py"), encoding="utf-8").read()
    for node in ast.parse(src).body:
        if isinstance(node, ast.Assign) and getattr(node.targets[0], "id", "") == "FOES":
            return ast.literal_eval(node.value)
    return []


FOES = _foes()

SHOTS = [("01", "22 Roboter, jeder mit eigener Regel"), ("02", "Nur Nullen und Einsen"), ("03", "Tipps erklären statt verraten"),
         ("04", "Spiegel, Hex, Pixel und mehr"), ("05", "Ereignisse wie der Nebel"), ("06", "10 Etagen bis zum Hauptrechner"),
         ("07", "Der Hauptrechner"), ("08", "Roboter wählen")]


def copy_images():
    os.makedirs(os.path.join(IMG, "bots"), exist_ok=True)
    os.makedirs(os.path.join(IMG, "foes"), exist_ok=True)
    pairs = [(os.path.join(OUT, "archiv", "roboter", "bots", b.lower() + ".png"), os.path.join(IMG, "bots", b.lower() + ".png")) for b in ORDER]
    pairs += [(os.path.join(OUT, "archiv", "stoerungen", "foes", f[0] + ".png"), os.path.join(IMG, "foes", f[0] + ".png")) for f in FOES]
    for name in ("workshop.png", "layer_0.png", "layer_1.png", "layer_2.png", "layer_3.png", "lift.png"):
        pairs.append((os.path.join(OUT, "archiv", "weltkarte", "img", name), os.path.join(IMG, "bb_" + name)))
    for name in ("station_dock.png", "station_bath.png", "station_play.png", "station_bench.png", "station_lift.png", "station_radio.png"):
        pairs.append((os.path.join(OUT, "archiv", "ersatzteile", "img", name), os.path.join(IMG, "bb_" + name)))
    for a, b in pairs:
        if os.path.exists(a):
            shutil.copyfile(a, b)
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
        ["1–2", "Steckkarten", "Wackelkontakt: Immer wieder erlischt eine deiner Ziffern."],
        ["3–4", "Knopfzelle", "Stromausfall: Nach einem Countdown erlöschen die Vorgaben. Wer vorher eine Ziffer daneben setzt, hält sie an."],
        ["5–7", "Chipsatz", "Überspannung: Ein Kurzschluss kostet 2 Ladungen statt 1."],
        ["8–9", "Arbeitsspeicher", "Störsignal: Immer wieder taucht eine falsche Notiz auf."],
        ["10", "Hauptrechner", "Alles kommt zusammen. Jeder Sektor bringt eine Erinnerung zurück."],
    ])}
    <p>Dazu bringen vier Roboter ihre eigenen Ereignisse mit: <b>Falsche Vorgabe</b> (ERROR), <b>Ansteckung</b> (VIRUS), <b>Zeitdruck</b> (DAEMON) und <b>Nebel</b> (MORSE).</p>

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


EXTRA = {"bits-and-bolts": bits_and_bolts, "bots-and-buddies": bots_and_buddies}


def extra(slug):
    return EXTRA[slug]() if slug in EXTRA else ""
