# Website scharzfeld-harz.de – Arbeitsanweisung für Claude

Website des Verkehrsvereins Scharzfeld-Südharz e.V. (Ort Scharzfeld, 37412 Herzberg am Harz).
Gepflegt von Ehrenamtlichen ohne Programmierkenntnisse – Änderungen kommen meist als
formlose Bitte („Haus Bohne hat eine neue Telefonnummer“, „neuer Verein“, „Foto tauschen“).

## Aufbau

- `inhalte/*.yml` – **eine Datei = eine Seite**. Dateiname = Seitenadresse
  (`vereine.yml` → `vereine.html`). Fast alle Änderungen passieren hier.
- `inhalte/_website.yml` – Kopf, Fuß, Vereinsadresse, Domain, Weiterleitungen alter Adressen.
- `bilder/` – alle Bilder, flach, Dateinamen klein, ohne Leerzeichen/Umlaute (`uk-haus-bohne.jpg`).
- `vorlagen/` – Jinja2-HTML-Vorlagen, je Abschnittstyp eine Datei `abschnitt-<typ>.html`.
- `css/style.css` – Gestaltung (Farben aus dem Ortswappen: Rot `#a3201c`, Gold `#d9a521`).
- `build.py` – baut `_site/`. Lokal testen: `pip install -r requirements.txt && python3 build.py --pruefen`
- `.github/workflows/website.yml` – baut und veröffentlicht bei jedem Push auf `main` (GitHub Pages).

## Seitenfelder

`titel` (Pflicht), `seitentitel` (optional, für Google), `beschreibung` (Meta-Description),
`menu` (Name im Hauptmenü; fehlt → nicht im Menü), `reihenfolge` (Menüposition),
`banner` (Titelbild), `untertitel`, `ort` (wird bei Karten an die Adresse gehängt), `abschnitte`.

## Abschnittstypen (`typ:`)

| typ | Felder |
|---|---|
| `einleitung` | `titel`, `text` (Markdown), `knoepfe: [{name, url}]`, `kasten: {titel, text}` |
| `text` | `titel`, `anker`, `text` (Markdown), optional `bild` + `bild_alt` (links daneben), `einleitung: true` (größer), `schmal: true` (Rechtstexte) |
| `kacheln` | `titel`, `eintraege: [{titel, bild, bild_alt, text, link}]` |
| `galerie` | `titel`, `stil: historisch` (Bild nicht beschneiden), `bilder: [{datei, text, alt}]` |
| `karten` | `titel`, `anker`, `eintraege: [{kategorie, name, bild, text, ausstattung: [..], person, adresse, telefon (Text oder Liste), web, web_text, email, kontakt}]` – mit Bild: Unterkunfts-Layout, ohne Bild: kompakte Karten |
| `kasten` | `titel`, `text` (Markdown) |
| `links` | `titel`, `text`, `eintraege: [{name, url}]` |
| `sprungmarken` | keine – listet alle Abschnitte der Seite mit `anker` + `titel` |

Markdown: Zeilenumbruch im Text = Zeilenumbruch auf der Seite. Absatz = Leerzeile.
Platzhalter für fehlende Angaben: `[[bitte ergänzen: was fehlt]]` → erscheint gelb markiert,
`build.py` listet alle offenen Platzhalter.

## Regeln

1. **Nichts erfinden.** Keine Telefonnummern, Öffnungszeiten, Jahreszahlen, Namen oder Fakten
   zur Ortsgeschichte ergänzen, die nicht vom Verein kommen. Fehlt etwas → Platzhalter setzen
   und im Antworttext nachfragen.
2. **Datenschutz:** Keine externen Ressourcen einbinden – keine Google Fonts, keine
   CDN-Skripte, kein Google Maps/YouTube-Embed, kein Analytics, keine Social-Media-Widgets,
   keine Formulare. Alles wird aus diesem Repository ausgeliefert. Wenn so etwas ausdrücklich
   gewünscht wird: vorher auf die nötige Änderung der `inhalte/Datenschutz.yml` hinweisen
   und sie mitliefern.
3. **Impressum/Datenschutz** nur ändern, wenn darum gebeten wird oder eine Änderung (z. B.
   neuer Hoster, neues Postfach) es erfordert. Hinweis geben, dass Claude keine Rechtsberatung ist.
4. **Bilder:** vor dem Einchecken auf max. 1600 px Breite (Titelbilder) bzw. 800 px (Karten)
   verkleinern, JPEG Qualität ~82. Dateiname klein, ohne Leerzeichen/Umlaute.
   Fotografin/Fotograf im Bildnachweis (`Impressum.yml`) ergänzen, wenn neu.
5. **Dateinamen der Seiten nicht umbenennen** (Links, Google). Falls doch nötig: alte Adresse
   in `_website.yml → weiterleitungen` eintragen. `Impressum.html` und `Datenschutz.html`
   bleiben großgeschrieben (Kompatibilität mit der alten Website).
6. Vor dem Abschluss immer `python3 build.py --pruefen` ausführen; es muss ✅ melden.
   Ist ein Browser verfügbar, betroffene Seite in Desktop- und Handybreite ansehen.
7. Sprache: Deutsch, Sie-Form gegenüber Gästen, freundlich-sachlich, keine Werbefloskeln.
8. Commit-Nachrichten auf Deutsch und konkret („Haus Bohne: neue Telefonnummer“).

## Offene Punkte (Stand Oktober 2026)

- Impressum: Vorstand, Amtsgericht, Verantwortliche/r nach MStV, Name Überarbeitung
- Datenschutz: Anbieter des Postfachs info@scharzfeld-harz.de
- Vereine: Ansprechpartner; Liste und Kurzbeschreibungen vom Verein bestätigen lassen
- Dorfläden: Telefonnummer Seniorenzentrum Diedrich
- Unterkunftsverzeichnis stammt inhaltlich von ca. 2015 – Gastgeber einzeln bestätigen lassen
- Zwei Fotos nur als „Impression aus Scharzfeld“ beschriftet (sehenswert-eingang.jpg, turm.jpg)
- Domain scharzfeld-harz.de: noch nicht verbunden (`_website.yml → domain`)
- Geplant: Dorfrundgang (Seite + Faltblatt), Stationen/Fotos kommen vom Verein
