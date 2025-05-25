## Reicht ein Commit-Kommentar – oder gehört das in DECISIONS.md?
> Faustregel: Wenn du es jemand anderem erklären müsstest → rein damit.
> Dokumentiert wird: Was? Und Warum?

## [2025-05-25]
**Session Data**
Wir unterscheiden zwischen RuntimeSessionData und StorageSessionData. RuntimeData nimmt ein Objekt auf, welches im Domain Hook für die Domain angehängt wird. Es enthält Daten wie Character oder Document.
StorageSessionData beinhaltet die Daten welche durch den SessionService persistiert und geladen werden.  
> Idee: Trennung der Daten zwischen Storage und Laufzeit.

## [2025-05-25]
**Template-Splitting**
Template-Splitting nach Format
Jedes logische Template besteht aus drei eigenständigen Dateien: .md, .plain, .ansi. Je nach Client wird automatisch das passende Format gerendert.
> Der Versuch, ein einziges Template dynamisch umzuwandeln (per Policy oder String-Strip) führte wiederholt zu inkonsistenten Ausgaben, 
> erschwerter Wartung und unklarer Formatlogik. Die Trennung nach Format schafft Klarheit, bessere Testbarkeit und eine stabile Render-Pipeline.

## [2025-05-25]
**Template-Rendering mit Markdown**
Alle Ausgaben erfolgen über Jinja2-Templates mit Markdown-Syntax.
> Grund: maximale Flexibilität, anpassbares Layout (auch für Kundenlösungen), markdown-kompatibel (z. B. Webclient, Chat-Ausgabe); Struktur: gemeinsamer `templates/`-Ordner, unterteilt nach Domain (`templates/mud/`, `templates/system/`, etc.)
> Endung: .j2.md -> jinja2 + markdown -> (Syntax-Highlighting)
> Zeilenumbrüche: zwei Leerzeichen am Ende / dreifaches Backtick

## [2025-05-25]
**Yakoon als Lösungseinheit (Solution)**
Yakoon-Plattform ist nun nur noch Infrastruktur – Einstieg erfolgt über Solution/
> Architektur: Platform → Solution → Entry-Points (console, webapi, telnet, webclient)
> Jeder App-Start erfolgt über Solution/run_*.py
> Vorbereitung für: `yakoon init`, `yakoon dev`, `yakoon deploy --docker`

## [2025-05-24]
**Webclient mit React + Vite**
Yakoon-Weboberfläche läuft unter React (Vite + Tailwind).
> Vorteile: ultraschneller Dev-Cycle, modernes Build-System, Hot-Reload
> Styling: Dark-Mode, Markdown-kompatibel
> Start: `npm run dev` im webclient-Verzeichnis

## [2025-05-24]
**Versionierung über Git-Tags + Fallback-Datei**
Plattformversion wird über `git describe --tags` ermittelt; Fallback über `version.txt`.
> Bei Docker-Build: Version via `echo "..." > version.txt` setzen
> Annotated Git-Tags erforderlich: `git tag -a v0.3.1 -m "Yakoon version 0.3.1"`