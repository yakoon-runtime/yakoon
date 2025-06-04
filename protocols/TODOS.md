
==================
# ✅ NEXT STEPS #
==================

- Session (temp) erstellen ->
  -> Dann brauchen wir keinen store und später wieder einen remove.
  -> Dann sollten wir aber die Session nicht in der Engine erzeugen, sondern im Gateway-Controller.



# Realm
- Umstellung Services + Stores

- Konzept Namespaces 
  - User_1, User_2 -> NS1
  - User_2 -> NS2

- Ersten Commands aus Evennia übernehmen 
  - Account, Session 

# Platform
- Erstelle neues Projekt ....
- Konzept: Engabe -> Verarbeitung - > Ausgabe
  - Antwort was getan wird; Antwort was getan wurde? 

# A.M.E.E 
- Code dokumentieren (Docstrings)
- Unittests (oder pytest - Yukoon-Style)

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
- Commands:
  - CmdInventory
  - CmdGet, CmdPut -> Legen in Boxen / Inventar....

# WETTER: CHAT: Yakoon-04
get_weather(): Er genügt, das erstmal auf Abruf zu tun.
1. Die Wetter-Phasen 
2. Die Wetter-Events (Ereignisse pro Zone)

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