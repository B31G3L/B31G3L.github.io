# B31G3L.github.io

Homepage und Datenschutzerklärungen für meine Android-Apps, gehostet über GitHub Pages:
<https://b31g3l.github.io/>

Reines HTML und CSS, kein Build-Schritt. Die Seite lädt bewusst nichts von Dritten nach
(keine Web-Fonts, keine Skripte, keine Cookies) – das steht so auch in `impressum/`.

## Seiten

| Pfad | Inhalt | Sprache |
|---|---|---|
| `/` | Startseite mit allen Apps und Spielen | DE |
| `/nextime/` | Datenschutz NexTime | DE |
| `/leetspeak-generator/` | Datenschutz Leetspeak Generator | DE |
| `/binary-clock/` | Datenschutz Binary-Clock | DE |
| `/housepot/` | Datenschutz Housepot, mit Löschanleitung unter `#konto-loeschen` | DE + EN |
| `/list2share/` | Datenschutz List2Share (App wird eingestellt; nicht mehr auf der Startseite verlinkt) | DE |
| `/dotlist/` | Weiterleitung auf `/list2share/` (alter App-Name) | – |
| `/reboot-byte/` | Datenschutz Reboot BYTE (nicht mehr auf der Startseite verlinkt) | EN + DE |
| `/bits-and-bolts/` | Datenschutz Bits & Bolts | DE + EN |
| `/impressum/` | Impressum und Datenschutz der Website | DE |

Die Links trägst du in der Play Console als „Link zur Datenschutzerklärung“ ein.
Für Housepot eignet sich `https://b31g3l.github.io/housepot/#konto-loeschen` als URL für Löschanträge.

## Neue App hinzufügen

1. Neuen Ordner anlegen, z. B. `meine-app/`.
2. `index.html` einer bestehenden App als Vorlage kopieren:
   `binary-clock/` für eine App ohne Datenübertragung, `housepot/` für eine App mit Konto und Cloud,
   `bits-and-bolts/` für eine zweisprachige Seite.
3. Inhalt gegen den Code der App prüfen: Berechtigungen im Manifest, eingebundene SDKs in `build.gradle`,
   externe Links, Android-Sicherung (`allowBackup`).
4. Karte in der Haupt-`index.html` ergänzen (`<li class="app-card">`) und die Zahlen im Kopfbereich anpassen.
5. Zeile in der Tabelle oben ergänzen.

## Aufbau

- `style.css` – ein Stylesheet für alle Seiten, helles und dunkles Farbschema über `prefers-color-scheme`.
- Bausteine der Datenschutzseiten: `.summary` (Kurzfassung), `.callout` (Hinweis), `article.policy` (Text),
  `.lang-switch` und `.lang-divider` für zweisprachige Seiten.

## Hinweis

Die Texte beschreiben den Stand der Apps beim jeweils angegebenen Datum und sind keine Rechtsberatung.
Ändert sich an einer App etwas (neue Berechtigung, neues SDK, neuer Dienst), muss die Erklärung mit angepasst werden.

## Logos (`brand/`)

Pixel-Schrift auf dunklem Grund, Ziffern in Terminal-Grün – passend zur Seite. Alle Dateien erzeugt `brand/make-brand.js`
(`node brand/make-brand.js brand`), die PNGs sind daraus gerendert.

| Datei | Größe | Wofür |
|---|---|---|
| `play-icon-512.png` | 512 × 512 | Google Play: Entwicklerseite, Symbol |
| `play-header-4096x2304.png` | 4096 × 2304 | Google Play: Entwicklerseite, Header-Bild (mit Schlagworten in Leet) |
| `play-feature-1024x500.png` | 1024 × 500 | Google Play: Vorstellungsgrafik (neutral, ohne App-Bezug) |
| `avatar-1024.png` | 1024 × 1024 | Profilbild (GitHub, Ko-fi, Google-Konto) – wird dort rund zugeschnitten |
| `logo-512.png`, `logo.svg` | 512 × 512 | Logo mit runden Ecken, `logo-light.svg` für helle Flächen |
| `github-banner-1280x640.png` | 1280 × 640 | GitHub „Social preview“ eines Repos |
| `social-1200x630.png` | 1200 × 630 | Vorschaubild beim Teilen der Website (`og:image`) |
| `wordmark-dark.*`, `wordmark-light.*` | 1312 × 224 | Schriftzug `B31G3L_` ohne Hintergrund (dark = für dunkle Flächen) |
| `mark.svg`, `mark-192.png` | – | Kurzform „31“ für kleine Größen; liegt auch als `favicon.svg` im Wurzelordner |
