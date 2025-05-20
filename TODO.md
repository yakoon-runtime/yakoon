TODO:
- Webservice



- Namespaces 
  - alles 

- CmdInventory
- CmdGet, CmdPut -> Legen in Boxen / Inventar....


get_weather(): Er genügt, das erstmal auf Abruf zu tun.
1. Die Wetter-Phasen 
2. Die Wetter-Events (Ereignisse pro Zone)


# GIT Konvention:
git commit -m "feat(cli): add project init command"


Mach uns mal eine Zusammenfassung, was wir alles geschafft haben, damit wir konzentriert unsere Zusammenarbeit fortsezen können.


# SETUP
- Im ProjektRoot: pip install -e .
- C:\Bibliothek\yakoon>  python -m yakoon --init smurf


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