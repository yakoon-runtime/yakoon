## Reicht ein Commit-Kommentar – oder gehört das in DECISIONS.md?
> Faustregel: Wenn du es jemand anderem erklären müsstest → rein damit.
> Dokumentiert wird: Was? Und Warum?

## [2025-06-07]
**Vergabeprozess für numerische IDs über Shards**
Beim Vergabeprozess für numerische IDs über Shards stellt sich die Frage, wann ein neuer Shard erzeugt werden muss. Ziel ist es, Ressourcen effizient zu nutzen und unnötige Ranges zu vermeiden. Ein neuer Shard wird nur erzeugt, wenn ein bestehender Shard entweder vollständig ausgeschöpft ist oder beim Speichern ein Konflikt (z.B. Parallelzugriff) auftritt.
Solange ein Shard noch Schreibkapazität hat und gespeichert werden kann, wird er weiterverwendet.
Vorteil: 
- minimale Anzahl von Shards
- saubere ID-Räume
- effiziente Nutzung der Datenbank
- keine unnötige Parallelisierung oder Leerlauf-Shards
Nachtrag: "Redis wurde bewusst vermieden – zugunsten eines nachvollziehbaren, speicherbasierten Shard-Counters.“

## [2025-06-06]
# Services dürfen andere Services konsumieren
Innerhalb der Domänenschicht ist es erlaubt, dass Services einander aufrufen und verwenden. Das ermöglicht saubere Kapselung von Logik und Wiederverwendung, ohne Layer-Grenzen zu verletzen. Ein Service darf jedoch keine Controller, IO-Schichten oder externe Systeme direkt verwenden – diese Verantwortung bleibt klar getrennt.

## [2025-06-06]
**Der SharedCounter liefert nur IDs, keine Keys**
Die Struktur eines Keys (domain, bucket, scope) ist domänenspezifisch und lebt im aktuellen Kontext – meist in der Session. Der CounterService hat keine Kenntnis darüber und liefert ausschließlich fortlaufende IDs. Services kombinieren diese ID gezielt mit bestehenden Kontextinformationen, z. B.: → `session.key.with_id(...)`
So bleibt die Verantwortung klar getrennt:
- Session = Kontext
- Service = Entscheidung
- Counter = technische ID-Vergabe

## [2025-06-06]
**Kein Leaken von Technik**
Infrastruktur-Komponenten wie der SharedCounterService, Row-Zugriff oder Key-Generierung dürfen ausschließlich im ServiceLayer verwendet werden. Weder Controller noch Engine sehen technische Hilfsmittel oder Detailzustände. Nur die Bedeutung („ein Raum wird erstellt“) darf durchgereicht werden – alles andere bleibt gekapselt.

## [2025-06-06]
**CounterService gerhört in interne Infrastruktur**
Der CounterService ist eine interne Infrastruktur – und wird ausschließlich durch die Domain-Services verwendet, niemals direkt durch Fassade, Controller oder Engine. Warum das richtig ist:
- IDs sind domänenspezifisch - Fassade kennt keine Objektdetails.
- Sie reicht Intention weiter, keine Strukturverantwortung - Kein Leaken von Technik	
- Counter bleibt reine Infrastruktur – kein globales Werkzeug - Erzwingt saubere Objekt-Konstruktion	
- Alles entsteht durch service.create(...), nie „halb von außen“

## [2025-06-06]
**Services sind für gültige Objekte verantwortlich**
Nur der jeweilige Service darf Objekte wie Session, Room oder Account in einen validen Zustand überführen. Das bedeutet: `.validate()` muss innerhalb des Services immer erfolgreich durchführbar sein. Weder Controller noch Engine dürfen IDs erzeugen, Felder ergänzen oder Validierung auslösen. Nur der Service kennt Kontext und Regeln – er trägt die alleinige Verantwortung. Somit erfolgt auch die Erzeugung gültiger Schlüssel über den Coutner-Service nur innerhalb der Services.

## [2025-06-06]
**Session.key darf niemals None sein**
Wir initialisieren jede Session mit einem vollständigen Key-Rahmen
(Domain, Bucket, Scope), aber lassen die ID bewusst leer (None).
Damit bleibt die Session eindeutig typisiert (z. B. "session/anon/live"),
aber erzeugt keine persistente ID, bis klar ist, dass sie gespeichert werden muss.
Ein `None`-Key wurde verworfen, weil:
- spätere Finalisierung unmöglich wäre (kein Kontext vorhanden)
- der Code zusätzliche Prüfungen auf `None` erfordert hätte
- Debugging, Logging und Namespacing unnötig erschwert würden
Stattdessen gilt: 
→ `session.key` ist **immer gesetzt**, aber `session.key.id` kann `None` sein.

## [2025-06-04]
**Services bauen Objekte, Stores liefern dicts**
Wir haben festgelegt, dass alle Stores ausschließlich mit dict arbeiten und keine Domainobjekte instanziieren.
Das Erzeugen, Validieren und Interpretieren von Objekten erfolgt ausschließlich im Service-Layer.
So bleibt der Speicher generisch, leicht austauschbar und testbar. Domainlogik gehört nicht in die Infrastruktur.
Das verhindert unnötige Duplikation und hält die Trennung klar.

## [2025-06-03]
**Setup-Funktionen & Registry-Struktur**
Jede Domain besitzt ein eigenes `setup.py`, das eine ServiceRegistry erzeugt.  
Die Stores werden über `create_store_registry()` zentral verwaltet und beim Setup übergeben.  
Alle Registry-Klassen sind explizit typisiert, enthalten aber keine Logik.  
Service- und Store-Registries sind getrennt, werden aber über `from_store_registry()` verbunden.

## [2025-06-02]
**003 – Kein ORM / Kein SQL-Mapper**
Wir verzichten bewusst auf ORMs wie SQLAlchemy oder Tortoise.  
Sie erzeugen versteckte Abhängigkeiten, Magie im Speicherzugriff und hohes Memory-Footprint.  
Stattdessen verwenden wir `asyncpg` + `PyPika` + explizite `StoreBase`-Klassen.  
Alle Datenzugriffe bleiben sichtbar, testbar und frei von Metaprogrammierung.

## [2025-06-01]
**StoreRegistry & ServiceRegistry**
Wir trennen Infrastruktur (StoreRegistry) von Anwendungslogik (ServiceRegistry).  
Jede Domain kapselt ihre eigene ServiceRegistry und bindet nur die Stores, die sie benötigt.  
Bootstrap entscheidet, welche Domains aktiv sind – nicht, wie sie intern aufgebaut sind.  
Das System bleibt testbar, erweiterbar und backend-agnostisch

## [2025-05-31]
**Kontextbasierte Architektur eingeführt**
Jede Domain besitzt ihre eigene ServiceRegistry, die alle Services kapselt (z. B. room, session, account).
Über einen ServiceRouter erfolgt die Auflösung pro Bucket.
Die Plattform kann so flexible, testbare und parallele Umgebungen betreiben.
Das System ist damit voll modular, multi-bucket-fähig und vorbereitet auf Persistenz, Testumgebungen und Paketinstallationen.

## [2025-05-30]
**Markdown bleibt als Importformat denkbar**
Markdown bleibt als Importformat denkbar – z. B. per Drag&Drop mit automatischer DB-Befüllung.

## [2025-05-30]
**Kein Markdown als Speicherformat**
Wir verwerfen Markdown als Speicherformat für Räume zugunsten einer SQL-basierten Lösung. Gründe: fehlende Zustandsfähigkeit, kein Multiuser-Support, keine Queries. Ziel ist eine skalierbare, persistente Welt mit dynamischer Erweiterbarkeit.

## [2025-05-29]
**Commands & Presenter**
Alle Commands verwenden das Presenter-System mit klarer template_key-Definition pro Command. Die Darstellung erfolgt vollständig über sprachfähige Jinja2-Templates, getrennt vom Code. Die Struktur verbessert Lesbarkeit, Mehrsprachigkeit und Konsistenz. Ausgabe-Logik ist vollständig kapselbar, testbar und flexibel. Der Presenter ersetzt direkte Ausgaben (session.emit, session.fail) durch eine semantische Schicht. Pfadangaben erfolgen explizit über get_template_path() – kein Hidden-Routing.

## [2025-05-29]
**Umgang mit KI (Intent Mapping)**
Entscheidung: Die KI fungiert ausschließlich als Berater zur Bedeutungserschließung von Benutzereingaben (Intent Mapping). Sie wählt mögliche Commands und Domains aus – führt aber nichts aus. Begründung: Die Plattform bleibt alleinige ausführende Instanz (Akteur). Die KI ist rein unterstützend (Berater) tätig. Damit wird verhindert, dass das Modell außerhalb der gültigen Systemlogik halluziniert – z. B. ungültige Commands erfindet oder nicht vorhandene Domains vorschlägt. Leitsatz: "Wer ist Akteur, wer ist Berater?" Nur die Plattform darf handeln. Die KI darf vorschlagen.

intent = ai_chat_prompt("Bring mich ins Ritterschloss")
if intent.is_valid():
    if session.auto_confirm and intent.command.safe:
        engine.dispatch(intent.to_command_string())  # z. B. "teleport #343"
    else:
        await ask(session, f"Willst du ausführen: {intent.command.key} {intent.command.args}?")

## [2025-05-29]
**Umgang mit KI (Intent Mapping)**
Entscheidung: Die KI wird nicht direkt zur Steuerung der Plattform genutzt, sondern dient ausschließlich der Interpretation von Benutzereingaben. Aus diesen ermittelt sie das passende Command, die zugehörige Domain und mögliche Argumente. Begründung: Die Plattform bleibt ausführende Instanz mit vollständiger Kontrolle. Die KI agiert als Intent-Resolver, nicht als Logikträger – das verhindert Automatisierungsfehler, Halluzinationen und wahrt Systemintegrität.

## [2025-05-29]
**Presenter**
Ein Presenter wurde eingeführt, um die gesamte Template-Struktur zu kapseln. Dieser Presenter arbeitet mit der Session ist so somit in der Lage direkt Templates an Clients zu versenden. Grund: Die Verwendung von Templates reduziert sich auf eine Erstellung des Presenters + pres.emit("key", **data). Zudem wurden die Prompts angebunden. pres.prompts.emit("key")

## [2025-05-28]
**Templates vs. Translater**
Entscheidung: Alle Benutzerausgaben werden über Jinja2-Templates pro Command und Sprache geregelt. Dies ermöglicht konsistente, übersetzbare Ausgaben mit klarer Struktur, einfacher Sprachumschaltung und vollständiger Trennung von Logik und Darstellung – ohne redundante Translator-Systeme.

## [2025-05-28]
**Memory Manager**
MemoryManager zur zyklischen Überwachung von Speicherveränderungen. Anzeige von Objekt-Trends mit Pfeilen und Delta-Werten. safe_input() ersetzt ainput() zur Vermeidung wachsender Closures. Keine Anzeichen für Memory-Leaks mehr bei Commands und Prompts.

## [2025-05-28]
**Timeout - offene Future**
Wenn der Aufrufer keinen Timeout setzt, wird automatisch ein Standardwert verwendet (z. B. 30 Sekunden). So wird jede Prompt-Blockade vermieden, auch wenn man’s vergiss

## [2025-05-27]
**Einführung IOAdpater**
Einführung eines `Output`, um Ausgaben (`out`, `err`) in einer gemeinsamen Struktur zu kapseln. Die Übergabe einzelner Callback-Funktionen wurde durch ein objektbasiertes Modell ersetzt, das klarer, testbarer und flexibler ist – insbesondere für Console, WebSocket und zukünftige Frontends. Der IO-Kontext wird nun konsistent per `Output` an Engine- und Session-Methoden übergeben.

## [2025-05-27]
**Prompt & Batch**
Clients, die kontinuierlich Requests verarbeiten (z. B. Console, Telnet, WebSocket), unterstützen interaktive Prompts (Benutzereingaben) während der Command-Ausführung. 
Diese Clients besitzen einen stabilen, zustandsbehafteten Kanal, über den Prompts korrekt empfangen und beantwortet werden können. Bei stateless Clients (z. B. REST-Services) kann hingegen nicht garantiert werden, dass ein gestarteter Prompt-Future überhaupt aufgelöst wird. Stateless-Clients dürfen keine interaktiven Prompts verwenden. Stattdessen müssen sie vollständige Abläufe als batch:-Kommandos ausführen, bei denen alle Eingaben im Voraus definiert sind. Daher: REST macht nur vollständige Abläufe und ist per Design zustandslos (auch wenn technisch machbar).

## [2025-05-27]
**Prompt-aware Batch Execution**
Introduce prompt-aware batch execution with internal input resolution. Reason: Avoid blocking the engine on ask() during batch processing while preserving execution order and prompt flow.

## [2025-05-26]
**Dynamische Commands per Domain-Hooks**
Zur Unterstützung kontextsensitiver Commands (z. B. Raum-Exits) führt jede Domain zwei Lifecycle-Hooks:
- on_before_resolve(session) → registriert dynamische Commands
- on_cleanup(session) → entfernt sie wieder
Dadurch wird dynamisches Routing pro Session möglich, ohne den Resolver oder die Registry zu verändern.Zudem werden nun Commands nur innerhalb eines Lifecycles angelegt und wieder entfernt.

## [2025-05-26]
**Festlegung von Ausführungsbedingungen für Commands**
Commands können festlegen, ob ein geladener Charakter erforderlich ist: requires_character = False
> Fehlt das Attribut oder ist es True, prüft der Domain-Hook on_before_run_command(...), ob session.data_runtime.character gesetzt ist – sonst wird die Ausführung blockiert.
> Damit steuert das Command selbst die Anforderungen an den Session-Zustand.n

## [2025-05-26]
**Klickbare Links**
Unterstützung von internen & externen Hyperlinks wurde wie folgt umgesetzt:
> externe Links -> markdown: [Open Docs](https://example.com)
> interne Links -> werden zu Commands: 
> [Show version](# "version"); [Show help version](# "help version")

## [2025-05-25]
**Session Data**
Wir unterscheiden zwischen RuntimeSessionData und StorageSessionData. RuntimeData nimmt ein Objekt auf, welches im Domain Hook für die Domain angehängt wird. Es enthält Daten wie Character oder Document. StorageSessionData beinhaltet die Daten welche durch den SessionService persistiert und geladen werden. Idee: Trennung der Daten zwischen Storage und Laufzeit.

## [2025-05-25]
**Template-Splitting**
Template-Splitting nach Format Jedes logische Template besteht aus drei eigenständigen Dateien: .md, .plain, .ansi. 
Je nach Client wird automatisch das passende Format gerendert.
> Der Versuch, ein einziges Template dynamisch umzuwandeln (per Policy oder String-Strip) führte wiederholt zu inkonsistenten Ausgaben, 
> erschwerter Wartung und unklarer Formatlogik. Die Trennung nach Format schafft Klarheit, bessere Testbarkeit und eine stabile Render-Pipeline.

## [2025-05-25]
**Template-Rendering mit Markdown**
Alle Ausgaben erfolgen über Jinja2-Templates mit Markdown-Syntax.
> Grund: maximale Flexibilität, anpassbares Layout (auch für Kundenlösungen), markdown-kompatibel (z. B. Webclient, Chat-Ausgabe); 
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