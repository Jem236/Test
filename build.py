#!/usr/bin/env python3
"""
Baut die Website scharzfeld-harz.de aus den Inhaltsdateien.

    inhalte/*.yml   ->  _site/*.html      (eine YAML-Datei = eine Seite)
    vorlagen/       ->  Aussehen der Seiten (HTML-Vorlagen)
    css/, bilder/   ->  werden unverändert nach _site/ kopiert

Aufruf:  python3 build.py            (baut nach _site/)
         python3 build.py --pruefen  (baut und listet offene Platzhalter)

Bricht mit verständlicher Fehlermeldung ab, wenn etwas nicht stimmt
(z. B. Bild fehlt, Pflichtfeld fehlt, Tippfehler in der YAML-Datei).
Auf GitHub bleibt dann die alte, funktionierende Version online.
"""
import html
import re
import shutil
import sys
import time
from pathlib import Path

import markdown
import yaml
from jinja2 import Environment, FileSystemLoader, StrictUndefined, ChainableUndefined
from markupsafe import Markup

BASIS = Path(__file__).parent
INHALT = BASIS / "inhalte"
ZIEL = BASIS / "_site"

ABSCHNITT_TYPEN = {"einleitung", "text", "kacheln", "galerie", "karten", "kasten", "links", "sprungmarken"}
PLATZHALTER = re.compile(r"\[\[\s*bitte ergänzen:\s*(.+?)\]\]", re.S)

fehler: list[str] = []
offen: list[str] = []
benutzte_bilder: set[str] = set()
aktuelle_datei = ""


def fehl(text):
    fehler.append(f"{aktuelle_datei}: {text}")


# ---------------------------------------------------------------- Filter
def platzhalter(text: str) -> str:
    def ersetze(m):
        offen.append(f"{aktuelle_datei}: {m.group(1).strip()}")
        return f'<mark class="todo">[bitte ergänzen: {html.escape(m.group(1).strip())}]</mark>'
    return PLATZHALTER.sub(ersetze, text)


def extern_attr(url: str) -> str:
    return ' target="_blank" rel="noopener"' if re.match(r"https?://", str(url)) else ""


def links_extern(htm: str) -> str:
    return re.sub(r'<a href="(https?://[^"]+)"', r'<a href="\1" target="_blank" rel="noopener"', htm)


MD = markdown.Markdown(extensions=["sane_lists", "attr_list", "nl2br"])


def f_md(text) -> Markup:
    if not text:
        return Markup("")
    MD.reset()
    return Markup(links_extern(MD.convert(platzhalter(str(text)))))


def f_mdi(text) -> Markup:
    """Markdown für eine Zeile, ohne umschließendes <p>."""
    h = str(f_md(text))
    return Markup(re.sub(r"^<p>(.*)</p>$", r"\1", h.strip(), flags=re.S))


def f_bild(datei, alt="") -> Markup:
    if not datei:
        return Markup("")
    if not (BASIS / "bilder" / datei).is_file():
        fehl(f'Bild "{datei}" gibt es nicht im Ordner bilder/ (Groß-/Kleinschreibung beachten!)')
    benutzte_bilder.add(datei)
    return Markup(f'<img src="bilder/{html.escape(datei)}" alt="{html.escape(str(alt or ""))}" loading="lazy">')


def f_telefon(nummern) -> Markup:
    if isinstance(nummern, (list, tuple)):
        return Markup(" oder ").join(f_telefon(n) for n in nummern)
    n = str(nummern)
    if "[[" in n:
        return Markup(platzhalter(n))
    ziffern = re.sub(r"\D", "", n)
    if not ziffern.startswith("0"):
        return Markup(html.escape(n))
    return Markup(f'<a href="tel:+49{ziffern[1:]}">{html.escape(n)}</a>')


def f_link(url, text=None) -> Markup:
    url = str(url)
    if not text:
        text = re.sub(r"^https?://|/$", "", url)
    return Markup(f'<a href="{html.escape(url)}"{extern_attr(url)}>{html.escape(str(text))}</a>')


def f_extern(url) -> Markup:
    return Markup(extern_attr(url))


# ---------------------------------------------------------------- Prüfung
def pruefe_seite(datei: str, s: dict):
    if not isinstance(s, dict):
        fehl("Datei ist leer oder kein gültiges YAML")
        return
    if not s.get("titel"):
        fehl('Pflichtfeld "titel" fehlt')
    if s.get("banner"):
        f_bild(s["banner"])
    for i, a in enumerate(s.get("abschnitte") or [], 1):
        typ = (a or {}).get("typ")
        if typ not in ABSCHNITT_TYPEN:
            fehl(f'Abschnitt {i}: unbekannter typ "{typ}" (erlaubt: {", ".join(sorted(ABSCHNITT_TYPEN))})')
            continue
        if typ == "karten":
            for e in a.get("eintraege") or []:
                if not e.get("name"):
                    fehl(f"Abschnitt {i}: Eintrag ohne \"name\"")
        if typ in ("text", "kasten") and not a.get("text"):
            fehl(f'Abschnitt {i} ({typ}): "text" fehlt')


# ---------------------------------------------------------------- Bauen
def main():
    global aktuelle_datei
    pruefen = "--pruefen" in sys.argv

    aktuelle_datei = "_website.yml"
    web = yaml.safe_load((INHALT / "_website.yml").read_text(encoding="utf-8"))

    seiten = {}
    for p in sorted(INHALT.glob("*.yml")):
        if p.name.startswith("_"):
            continue
        aktuelle_datei = p.name
        try:
            s = yaml.safe_load(p.read_text(encoding="utf-8"))
        except yaml.YAMLError as e:
            fehl(f"YAML-Fehler (meist Einrückung oder ein fehlendes Anführungszeichen):\n    {e}")
            continue
        pruefe_seite(p.name, s)
        seiten[p.stem + ".html"] = s

    menu = sorted(
        ({"datei": d, "name": s["menu"], "rf": s.get("reihenfolge", 99)} for d, s in seiten.items() if isinstance(s, dict) and s.get("menu")),
        key=lambda m: m["rf"],
    )

    env = Environment(loader=FileSystemLoader(BASIS / "vorlagen"), autoescape=True,
                      undefined=ChainableUndefined, trim_blocks=True, lstrip_blocks=True)
    env.filters.update(md=f_md, mdi=f_mdi, bild=f_bild, telefon=f_telefon, link=f_link, extern=f_extern)

    if ZIEL.exists():
        shutil.rmtree(ZIEL)
    ZIEL.mkdir()

    version = time.strftime("%Y%m%d%H%M")
    for datei, s in seiten.items():
        aktuelle_datei = datei.replace(".html", ".yml")
        if not isinstance(s, dict):
            continue
        try:
            htm = env.get_template("seite.html").render(seite=s, web=web, menu=menu, datei=datei, version=version)
        except Exception as e:  # noqa: BLE001
            fehl(f"Vorlagenfehler: {e}")
            continue
        (ZIEL / datei).write_text(htm, encoding="utf-8")

    # Weiterleitungen alter Adressen
    for alt, neu in (web.get("weiterleitungen") or {}).items():
        (ZIEL / alt).write_text(env.get_template("weiterleitung.html").render(ziel=neu), encoding="utf-8")

    # 404-Seite
    s404 = {"titel": "Seite nicht gefunden", "banner": "banner-sonnenuntergang.jpg",
            "abschnitte": [{"typ": "text", "text": "Diese Seite gibt es leider nicht (mehr). [Zur Startseite](index.html)"}]}
    (ZIEL / "404.html").write_text(env.get_template("seite.html").render(seite=s404, web=web, menu=menu, datei="404.html", version=version), encoding="utf-8")

    # statische Dateien
    shutil.copytree(BASIS / "css", ZIEL / "css")
    (ZIEL / "bilder").mkdir()
    benutzte_bilder.update({web.get("logo", ""), "favicon.ico"})
    for b in (BASIS / "bilder").iterdir():
        if b.is_file() and not b.name.startswith("."):
            shutil.copy2(b, ZIEL / "bilder" / b.name)
            if b.stat().st_size > 600_000:
                print(f"Hinweis: Bild {b.name} ist {b.stat().st_size // 1024} KB groß – bitte auf ca. 1600 px Breite verkleinern.")
    (ZIEL / ".nojekyll").write_text("")

    # Domain, Sitemap, robots.txt
    if web.get("domain"):
        (ZIEL / "CNAME").write_text(web["domain"].strip() + "\n")
        urls = "\n".join(f"  <url><loc>https://{web['domain']}/{'' if d == 'index.html' else d}</loc></url>" for d in seiten)
        (ZIEL / "sitemap.xml").write_text(f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{urls}\n</urlset>\n')
        (ZIEL / "robots.txt").write_text(f"User-agent: *\nAllow: /\nSitemap: https://{web['domain']}/sitemap.xml\n")

    ungenutzt = sorted(b.name for b in (BASIS / "bilder").iterdir() if b.is_file() and b.name not in benutzte_bilder and not b.name.startswith("."))

    if fehler:
        print("\n❌ FEHLER – die Website wurde NICHT veröffentlicht:\n")
        for f in fehler:
            print("  •", f)
        sys.exit(1)

    print(f"✅ {len(seiten)} Seiten gebaut nach {ZIEL.name}/")
    if offen:
        print(f"\n⚠️  {len(offen)} offene Platzhalter [[bitte ergänzen: …]] (gelb markiert auf der Seite):")
        for o in offen:
            print("  •", o)
    if pruefen and ungenutzt:
        print("\nℹ️  Bilder, die nirgends verwendet werden:", ", ".join(ungenutzt))


if __name__ == "__main__":
    main()
