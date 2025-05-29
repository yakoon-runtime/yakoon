## Reicht ein Commit-Kommentar – oder gehört das in DECISIONS.md?
> Faustregel: Wenn du es jemand anderem erklären müsstest → rein damit.
> Dokumentiert wird: Was? Und Warum?

## [2025-05-29]
**Umgang mit KI (Intent Mapping)**
Entscheidung: Die KI fungiert ausschließlich als Berater zur Bedeutungserschließung von Benutzereingaben
(Intent Mapping). Sie wählt mögliche Commands und Domains aus – führt aber nichts aus.
Begründung: Die Plattform bleibt alleinige ausführende Instanz (Akteur). 
Die KI ist rein unterstützend (Berater) tätig. Damit wird verhindert, dass das Modell außerhalb 
der gültigen Systemlogik halluziniert – z. B. ungültige Commands erfindet oder nicht vorhandene Domains vorschlägt.
Leitsatz: "Wer ist Akteur, wer ist Berater?" – Nur die Plattform darf handeln. Die KI darf vorschlagen.

´´´
intent = ai_chat_prompt("Bring mich ins Ritterschloss")
if intent.is_valid():
    if session.auto_confirm and intent.command.safe:
        engine.send(intent.to_command_string())  # z. B. "teleport #343"
    else:
        await ask(session, f"Willst du ausführen: {intent.command.key} {intent.command.args}?")
´´´

## [2025-05-29]
**Umgang mit KI (Intent Mapping)**
Entscheidung: Die KI wird nicht direkt zur Steuerung der Plattform genutzt, sondern dient 
ausschließlich der Interpretation von Benutzereingaben. 
Aus diesen ermittelt sie das passende Command, die zugehörige Domain und mögliche Argumente.
Begründung: Die Plattform bleibt ausführende Instanz mit vollständiger Kontrolle. 
Die KI agiert als Intent-Resolver, nicht als Logikträger – das verhindert Automatisierungsfehler, 
Halluzinationen und wahrt Systemintegrität.

## [2025-05-29]
**Presenter**
Ein Presenter wurde eingeführt, um die gesamte Template-Struktur zu kapseln.
Dieser Presenter arbeitet mit der Session ist so somit in der Lage direkt
Templates an Clients zu versenden. Grund: Die Verwendung von Templates reduziert
sich auf eine Erstellung des Presenters + pres.emit("key", **data). Zudem wurden
die Prompts angebunden. pres.prompts.emit("key")

## [2025-05-28]
**Templates vs. Translater**
Entscheidung: Alle Benutzerausgaben werden über Jinja2-Templates pro Command und Sprache geregelt. 
Dies ermöglicht konsistente, übersetzbare Ausgaben mit klarer Struktur, einfacher 
Sprachumschaltung und vollständiger Trennung von Logik und Darstellung – ohne redundante Translator-Systeme.

## [2025-05-28]
**Memory Manager**
MemoryManager zur zyklischen Überwachung von Speicherveränderungen.
Anzeige von Objekt-Trends mit Pfeilen und Delta-Werten.
safe_input() ersetzt ainput() zur Vermeidung wachsender Closures.
Keine Anzeichen für Memory-Leaks mehr bei Commands und Prompts.

## [2025-05-28]
**Timeout - offene Future**
Wenn der Aufrufer keinen Timeout setzt, wird automatisch ein Standardwert verwendet 
(z. B. 30 Sekunden). So wird jede Prompt-Blockade vermieden, auch wenn man’s vergiss

## [2025-05-27]
**Einführung IOAdpater**
Einführung eines `IOAdapter`, um Ausgaben (`out`, `err`) in einer gemeinsamen Struktur zu kapseln.
Die Übergabe einzelner Callback-Funktionen wurde durch ein objektbasiertes Modell ersetzt, das klarer, 
testbarer und flexibler ist – insbesondere für Console, WebSocket und zukünftige Frontends.
Der IO-Kontext wird nun konsistent per `IOAdapter` an Engine- und Session-Methoden übergeben.

## [2025-05-27]
**Prompt & Batch**
Clients, die kontinuierlich Requests verarbeiten (z. B. Console, Telnet, WebSocket),
unterstützen interaktive Prompts (Benutzereingaben) während der Command-Ausführung. 
Diese Clients besitzen einen stabilen, zustandsbehafteten Kanal, über den Prompts korrekt
empfangen und beantwortet werden können. Bei stateless Clients (z. B. REST-Services) kann 
hingegen nicht garantiert werden, dass ein gestarteter Prompt-Future überhaupt aufgelöst wird. 
Stateless-Clients dürfen keine interaktiven Prompts verwenden. Stattdessen müssen sie vollständige 
Abläufe als batch:-Kommandos ausführen, bei denen alle Eingaben im Voraus definiert sind.
Daher: REST macht nur vollständige Abläufe und ist per Design zustandslos (auch wenn technisch machbar).

## [2025-05-27]
**Prompt-aware Batch Execution**
Introduce prompt-aware batch execution with internal input resolution.
Reason: Avoid blocking the engine on ask() during batch processing while preserving 
execution order and prompt flow.

## [2025-05-26]
**Dynamische Commands per Domain-Hooks**
Zur Unterstützung kontextsensitiver Commands (z. B. Raum-Exits)
führt jede Domain zwei Lifecycle-Hooks:
- on_before_resolve(session) → registriert dynamische Commands
- on_cleanup(session) → entfernt sie wieder
Dadurch wird dynamisches Routing pro Session möglich, ohne den Resolver oder die Registry zu verändern.
Zudem werden nun Commands nur innerhalb eines Lifecycles angelegt und wieder entfernt.

## [2025-05-26]
**Festlegung von Ausführungsbedingungen für Commands**
Commands können festlegen, ob ein geladener Charakter erforderlich ist: 
requires_character = False
> Fehlt das Attribut oder ist es True, prüft der Domain-Hook on_before_run_command(...), 
ob session.data_runtime.character gesetzt ist – sonst wird die Ausführung blockiert.
> Damit steuert das Command selbst die Anforderungen an den Session-Zustand.n

## [2025-05-26]
**Klickbare Links**
Unterstützung von internen & externen Hyperlinks wurde wie folgt umgesetzt:
> externe Links -> markdown: [Open Docs](https://example.com)
> interne Links -> werden zu Commands: 
> [Show version](# "version"); [Show help version](# "help version")

## [2025-05-25]
**Session Data**
Wir unterscheiden zwischen RuntimeSessionData und StorageSessionData. RuntimeData nimmt ein Objekt auf, 
welches im Domain Hook für die Domain angehängt wird. Es enthält Daten wie Character oder Document.
StorageSessionData beinhaltet die Daten welche durch den SessionService persistiert und geladen werden.  
> Idee: Trennung der Daten zwischen Storage und Laufzeit.

## [2025-05-25]
**Template-Splitting**
Template-Splitting nach Format
Jedes logische Template besteht aus drei eigenständigen Dateien: .md, .plain, .ansi. 
Je nach Client wird automatisch das passende Format gerendert.
> Der Versuch, ein einziges Template dynamisch umzuwandeln (per Policy oder String-Strip) 
führte wiederholt zu inkonsistenten Ausgaben, 
> erschwerter Wartung und unklarer Formatlogik. Die Trennung nach Format schafft Klarheit, 
bessere Testbarkeit und eine stabile Render-Pipeline.

## [2025-05-25]
**Template-Rendering mit Markdown**
Alle Ausgaben erfolgen über Jinja2-Templates mit Markdown-Syntax.
> Grund: maximale Flexibilität, anpassbares Layout (auch für Kundenlösungen), 
markdown-kompatibel (z. B. Webclient, Chat-Ausgabe); 
Struktur: gemeinsamer `templates/`-Ordner, unterteilt nach Domain (`templates/realm/`, `templates/system/`, etc.)
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