# Auftrag für Claude Code: Website scharzfeld-harz.de auf GitHub veröffentlichen

Dieses Verzeichnis enthält die fertige Website des Verkehrsvereins Scharzfeld-Südharz e.V.
(Seitengenerator: `build.py`, Inhalte in `inhalte/`, Regeln in `CLAUDE.md`).
Bitte veröffentliche sie über GitHub Pages. Die Person, mit der du sprichst, ist keine
Entwicklerin – erkläre jeden Schritt, bei dem sie etwas tun muss, kurz auf Deutsch.

## Schritte

1. **Prüfen, ob alles da ist**
   - `python3 -m pip install -r requirements.txt` (falls nötig mit `--user` oder in einer venv)
   - `python3 build.py --pruefen` muss ✅ melden. Offene Platzhalter sind okay, nur auflisten.

2. **GitHub-Zugang**
   - `gh auth status` prüfen. Ist `gh` nicht installiert, Installation anbieten
     (macOS: `brew install gh`). Ist niemand angemeldet: die Nutzerin bitten, `gh auth login`
     selbst auszuführen (Browser-Anmeldung) – keine Passwörter oder Tokens im Chat abfragen.
   - Fragen, unter welchem Konto bzw. welcher Organisation das Repository liegen soll
     (empfohlen: ein eigenes Vereinskonto, nicht privat) und wie es heißen soll
     (Vorschlag: `scharzfeld-harz`).

3. **Repository anlegen und hochladen**
   ```bash
   git init -b main
   git add .
   git commit -m "Website scharzfeld-harz.de: erste Version"
   gh repo create <konto>/<name> --public --source . --remote origin --push
   ```
   Vorher kurz bestätigen lassen: Das Repository ist **öffentlich**, alle Dateien sind für
   jeden einsehbar (kostenloses GitHub Pages setzt das voraus).

4. **GitHub Pages auf „GitHub Actions“ stellen**
   ```bash
   gh api -X POST repos/<konto>/<name>/pages -f build_type=workflow \
     || gh api -X PUT repos/<konto>/<name>/pages -f build_type=workflow
   ```

5. **Ersten Bau abwarten**
   ```bash
   gh workflow run website.yml   # falls der Push ihn nicht schon gestartet hat
   gh run watch
   ```
   Bei Fehlern das Log lesen (`gh run view --log-failed`), Ursache beheben, neu pushen.

6. **Ergebnis melden**
   - Adresse der Website nennen (`gh api repos/<konto>/<name>/pages --jq .html_url`).
   - Die offenen Platzhalter aus `build.py --pruefen` auflisten und darauf hinweisen,
     dass Impressum und Datenschutz vor dem Bekanntmachen vervollständigt sein müssen.
   - Hinweis: Eigene Domain später über `inhalte/_website.yml → domain` und
     Settings → Pages → Custom domain (siehe README.md).

7. **Aufräumen**
   Diese Datei (`AUFTRAG-CLAUDE-CODE.md`) danach aus dem Repository löschen
   (`git rm AUFTRAG-CLAUDE-CODE.md && git commit -m "Einrichtungsanleitung entfernt" && git push`).

## Wichtig

- Nichts an Inhalten oder Rechtstexten ändern, nur veröffentlichen.
- Für alle späteren Änderungen gelten die Regeln in `CLAUDE.md`.
