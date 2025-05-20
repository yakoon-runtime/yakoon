
- Templates für die Räume (Jinja2)
- Persistieren aller Objekte
- Und jede Menge Commands (die habe ich schon für Evennia entwickelt. Sind aber
  alle noch anzupassen.
- Unittests (oder besseres - Yukoon-Style)
- Alles Dokumentieren im Code auf Englisch (Docstrings)
- Zudem brauchen wir noch einen Webclient. Warum zu dieser Zeit?
  - Die Entwicklung wird einfacher, wenn wir den Client nicht ständig starten und stoppen
    müssen. Ausserdem tun wir uns im Design mit den Templates später einfacher.

- Namespaces 
  - alles 

- CmdInventory
- CmdGet, CmdPut -> Legen in Boxen / Inventar....


# WETTER: CHAT: Yakoon-04
get_weather(): Er genügt, das erstmal auf Abruf zu tun.
1. Die Wetter-Phasen 
2. Die Wetter-Events (Ereignisse pro Zone)


# GIT Konvention:
git commit -m "feat(cli): add project init command"


# Start RestService
- uvicorn yakoon.app.webapi.app:app --reload

# Install Yakon as component
- Im ProjektRoot: pip install -e .
- C:\Bibliothek\yakoon>  python -m yakoon --init smurf

# Zusammenfassung -> Chatgpt
Mach uns mal eine Zusammenfassung, was wir alles geschafft haben, damit wir konzentriert unsere Zusammenarbeit fortsezen können.


# Application Plan
yakoon/               ← die Engine (pip install yakoon)
minddojo/             ← ein Spielprojekt, erzeugt mit `yakoon --init`
├── game/             ← Lokale Basisschicht (wenn überschrieben)
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
- refactor(game): move phase logic to store
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