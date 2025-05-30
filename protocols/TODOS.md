
==================
# ✅ NEXT STEPS #
==================
# Bekannte Bugss
- Beim Send werden die system-hook teilweise doppelt aufgerufen. 
  - Rufen wir alle System-Hook immer auf?
  - Rufen wir Systemhooks überhaupt nicht auf, dann können wir die Sessions nicht steuern.

# Realm


- Texte speichern wir wo? Markdown-Files wäre irgendwie auch cool
    - Dann könnten wir solche Dateien einfach per Drag&Drop ins System ziehen!

- Konzept Namespaces 
  - User_1, User_2 -> NS1
  - User_2 -> NS2
- Realmsettings: wirklich von Setings ableiten? eher nicht
- realm.models.room -> template + field attachment.
- realm.commands.general - IC, OOC
- realm.commands.character - * 

- Ersten Commands aus Evennia abziehen 
  - Account, Session 

# Platform
- Erstelle neues Projekt ....
- Konzept: Engabe -> Verarbeitung - > Ausgabe
  - Antwort was getan wird; Antwort was getan wurde? 

# A.M.E.E 
- Alles Dokumentieren im Code auf Englisch (Docstrings)
- Unittests (oder besseres - Yukoon-Style)

# Open AI
- Yakoon-06 (AI-key) -> comment_all_public_methods
  -> Was bedeutet das? -> Neuer Chat. 
      CmdGPTSession 

# Drag & Drop am Webclient
- Daten können hier dann verarbeitet werden. 
- Request kann auch BINDATA / Chunks?

# Docker
- Alles muss in einem Docker laufen

# MUD
- Templates für die Räume (Jinja2)
- Konzept: Namespaces 
  - Modelle sind verwenden Namensberreiche
- Und jede Menge Commands (die habe ich schon für Evennia entwickelt. Sind aber
  alle noch anzupassen.
- Persistieren aller Objekte
- Commands:
  - CmdInventory
  - CmdGet, CmdPut -> Legen in Boxen / Inventar....

# WETTER: CHAT: Yakoon-04
get_weather(): Er genügt, das erstmal auf Abruf zu tun.
1. Die Wetter-Phasen 
2. Die Wetter-Events (Ereignisse pro Zone)


---
# GIT Konvention:
git commit -m "feat(cli): add project init command"


# Start RestService
- uvicorn yakoon.app.webapi.app:app --reload

# Install Yakon as component
- Im ProjektRoot: pip install -e .
- C:\Bibliothek\yakoon>  python -m yakoon --init smurf

# Zusammenfassung -> Chatgpt
Mach uns mal eine Zusammenfassung, was wir alles geschafft haben, damit wir konzentriert unsere Zusammenarbeit fortsezen können.

# Später
- Alles Dockern


# Application Plan
yakoon/               ← die Engine (pip install yakoon)
minddojo/             ← ein Spielprojekt, erzeugt mit `yakoon --init`
├── realm/             ← Lokale Basisschicht (wenn überschrieben)
├── worlds/
│   └── dojo1/
│       ├── rooms/
│       └── templates/
├── requirements.txt  ← eigene Abhängigkeiten
├── yakoon.conf.py    ← Konfiguration (tickrate, hooks, etc.)


# GIT-CONVENTIONS:
<type>(<scope>): <description>
- https://www.conventionalcommits.org/

**Beispiele:**
- feat(cli): add project init command
- fix(auth): reject empty passwords
- refactor(realm): move phase logic to store
- test: add coverage for CmdLook
- docs(readme): update getting started

**Häufige type-Werte**
- feat	    neues Feature
- fix	    Bugfix
- refactor	Code-Umbau (kein neues Verhalten)
- docs	    Doku-Änderungen
- style	    Formatierung, keine Logik
- test	    Tests ergänzt/geändert
- chore	    Wartung (z. B. CI, Tooling)