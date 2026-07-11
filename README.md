# B31G3L.github.io

Datenschutzerklärungen für meine Android-Apps, gehostet über GitHub Pages.

## Einrichtung

1. Auf GitHub ein Repository namens **`B31G3L.github.io`** anlegen (exakter Name = dein Username + `.github.io`, wichtig für User-Pages).
2. Diese Dateien in das Repo kopieren und pushen:

```bash
cd pfad/zu/entpackten/dateien
git init
git add .
git commit -m "Initial commit: Datenschutzseiten"
git branch -M main
git remote add origin https://github.com/B31G3L/B31G3L.github.io.git
git push -u origin main
```

3. Im Repo unter **Settings → Pages** prüfen, dass als Quelle der `main`-Branch (Root) ausgewählt ist. Bei User-Pages-Repos ist das meist automatisch aktiv.
4. Nach ein paar Minuten ist die Seite erreichbar unter:
   - Übersicht: `https://b31g3l.github.io/`
   - Dotlist: `https://b31g3l.github.io/dotlist/`
   - NexTime: `https://b31g3l.github.io/nextime/`
   - Leetspeak Generator: `https://b31g3l.github.io/leetspeak-generator/`

## Vor dem Veröffentlichen

- In jeder `index.html` unter `dotlist/`, `nextime/` und `leetspeak-generator/` die Platzhalter `[Vor- und Nachname]`, `[Anschrift, falls erforderlich]`, `[E-Mail-Adresse]` und `[Datum einfügen]` ausfüllen.
- Texte sind Entwürfe auf Basis der bekannten Funktionen/Dienste jeder App (Firebase, FCM, Google Sign-In, Spracheingabe, In-App-Review). Bitte prüfen, ob sich seither etwas geändert hat (z. B. neue SDKs, Werbe- oder Analyse-Dienste), und im Zweifel rechtlich absichern lassen – dies ersetzt keine Rechtsberatung.
- Die fertigen Links (`.../dotlist/`, `.../nextime/`, `.../leetspeak-generator/`) kannst du direkt im Play Console Eintrag jeder App als "Link zur Datenschutzerklärung" hinterlegen.

## Neue App hinzufügen

1. Neuen Ordner anlegen, z. B. `genea/`.
2. `index.html` einer bestehenden App als Vorlage kopieren und Inhalt anpassen.
3. Karte in der Haupt-`index.html` (`app-list`) ergänzen.
