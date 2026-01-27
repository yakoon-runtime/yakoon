
# 🧭 Yakoon Roadmap

## 🎯 Vision

Yakoon ist eine text- und commandbasierte Plattform zur Steuerung und Automatisierung von Wissen, Prozessen und Systemen. Ziel ist, dass der Entwickler sein Unternehmen komplett per Tastatur und Sprache steuern kann – mit Kontext, Sessions und klaren Domänen.

---

## ✅ Version 0.1 – Fundament: Plattform + MindDojo

### Ziele

* **Funktionale, stabile Plattformbasis**
* **Persönliche Trainingswelt (MindDojo) als Demo & Testinstanz**
* **Deploymentfähig via Docker**

### Inhalte

* [ ] Engine mit ControllerDirectory, ControllerHooks, Lifecycle klar definiert
* [ ] Sessionverwaltung mit persistenter Speicherbindung (PostgreSQL)
* [ ] MindDojo als private Domain (nicht auslieferbar)
* [ ] Web-Terminal (Markdown, Prompt, Sessionleiste)
* [ ] on\_platform\_validate/on\_initialize stabil integriert
* [ ] Bugfreier Zustand in MindDojo-World (Raumlogik, Commands)
* [ ] Dockerfile + docker-compose mit Konfiguration + Build-Skript

### Erfolgskriterium

* Lokales Deployment möglich
* Nutzung von MindDojo und SessionCommand möglich
* keine internen Fehler im Ablauf

---

## 🚀 Version 0.2 – Yakoon als persönliche SaasCommand-Zentrale

### Ziel

„Ich möchte alles, was ich in meinem Unternehmen tue, per SaasCommand tun können – per Sprache oder Tastatur.“

### Inhalte

* [ ] Aufbau produktiver Domains (`ops`, `finance`, `projects`, `content` ...)
* [ ] SaasCommand-Bindings: REST, Shell, Python
* [ ] Logging & Auditing jeder Session
* [ ] CLI- oder Web-Terminal mit Sprachintegration (Whisper / OpenAI)
* [ ] API-Zugriff auf Firmen-Ressourcen über Commands
* [ ] Konfigurierbare Rechte + CommandDocs
* [ ] Optional: Self-Hosted Admin-Oberfläche (YakoonDashboard)

### Erfolgskriterium

* Eigener Arbeitsalltag kann komplett in Yakoon abgebildet werden
* Wiederverwendbare SaasCommand-Domains entstehen aus Bedarf
* Yakoon wird zur zentralen Oberfläche für Steuerung

---

## 🧠 Weiterer Ausblick

* v0.3: Public-SDK, CommandPack-API, Web-Terminal als NPM-Bundle
* v0.4: Hosting-Layer für Kundeninstanzen
* v1.0: Launch-Produkt für externe Kunden
