# scharzfeld-harz.de

Website des Verkehrsvereins Scharzfeld-Südharz e.V.

Die Seiten werden **nicht** als HTML bearbeitet, sondern als einfache Textdateien im Ordner
[`inhalte/`](inhalte/). Nach jeder Änderung baut GitHub die Website automatisch neu und
veröffentlicht sie – nach ca. 1–2 Minuten ist sie online.

## Etwas ändern – drei Wege

**1. Claude fragen (am einfachsten)**
Claude mit Zugriff auf dieses Repository einfach schreiben, was sich ändern soll, z. B.
„Ferienwohnung An der Bremke hat kein WLAN mehr“ oder „Bitte den Harzklub-Ansprechpartner
Max Muster, Tel. 05521 1234 eintragen“. Claude hält sich an die Regeln in [`CLAUDE.md`](CLAUDE.md).

**2. Direkt auf github.com**
Datei in `inhalte/` öffnen → Stift-Symbol („Edit“) → ändern → unten „Commit changes“.
Wichtig: Die **Einrückung** (Leerzeichen am Zeilenanfang) muss stimmen. Am sichersten ist es,
einen vorhandenen Eintrag zu kopieren und anzupassen.

**3. Foto hinzufügen**
Ordner `bilder/` → „Add file“ → „Upload files“. Vorher auf ca. 1600 px Breite verkleinern,
Dateiname klein und ohne Leerzeichen/Umlaute (z. B. `fewo-sonnenblick.jpg`).
Dann in der passenden Datei in `inhalte/` mit `bild: fewo-sonnenblick.jpg` eintragen.

## Was passiert bei einem Fehler?

Hat sich ein Tippfehler eingeschlichen (z. B. falsche Einrückung, Bildname falsch geschrieben),
bricht der automatische Bau ab und **die alte Version bleibt online**. Unter dem Reiter
„Actions“ erscheint dann ein rotes ✗ – dort steht auf Deutsch, was nicht stimmt.

Gelb markierte Stellen `[[bitte ergänzen: …]]` sind fehlende Angaben, die noch nachgetragen werden müssen.

## Einmalige Einrichtung

1. Neues Repository auf github.com anlegen (öffentlich) und alle Dateien dieses Ordners hochladen
   (einschließlich `.github/workflows/website.yml`).
2. Settings → Pages → „Build and deployment“ → Source: **GitHub Actions**.
3. Reiter „Actions“ → „Website bauen und veröffentlichen“ → „Run workflow“.
4. Eigene Domain: in `inhalte/_website.yml` bei `domain:` eintragen und bei Settings → Pages
   „Custom domain“ setzen; beim Domain-Anbieter die DNS-Einträge laut GitHub-Anleitung setzen.

## Technik (für Interessierte)

`build.py` (Python, Jinja2, Markdown, PyYAML) liest `inhalte/*.yml`, setzt sie in die
Vorlagen aus `vorlagen/` ein und schreibt die fertige Website nach `_site/`.
Lokal testen: `pip install -r requirements.txt && python3 build.py --pruefen`, dann
`_site/index.html` im Browser öffnen.
Die fertigen Dateien in `_site/` laufen auf jedem Webspace – ein späterer Umzug
(z. B. zu einem deutschen Hoster) ist jederzeit möglich.
