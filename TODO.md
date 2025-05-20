
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




# UFT-8 - aktivieren
cmd.exe -> chcp 65001


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