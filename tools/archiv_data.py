# Daten der Roboter aus den Spielen, gemeinsam für make_archiv.py und make_archiv2.py.
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
HERO = {"BYTE": "Bits & Bolts, Bolt Buddies", "LOOP": "Loop Echo (geplant)", "GATE": "Tilt Gate (geplant)",
        "ROOT": "Tilt Gate (geplant)", "ERROR": "Surge Chain (geplant)", "GLITCH": "Surge Chain (geplant)",
        "SHIFT": "Loop Echo (geplant)", "QUBIT": "Loop Echo (geplant)"}
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
