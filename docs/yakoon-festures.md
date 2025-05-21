
# MASTER-TODO's
- System für Industrie - Command-Strukturen mit KI
    - Automatisierung (Rechnungen, PPX, Mails, Produktionsabläufe....)
    - Projekte ("Erstelle Neues Projekt X", "Lade Projekt X")
    - Dokumentiere (Zugriff auf Lokale Version.)
    

## Scripting
- Scriptdateien (scripts/goblin.txt)
    @script teleport_test:
    login testuser
    ic testuser
    teleport #101
    look
    get box

await engine.send(npc_session, "say Wer wagt es, mein Lager zu betreten?")
await engine.send(npc_session, "attack stefan")
await engine.send(npc_session, "look")

- Reaktive Trigger (→ bei player enters, führe batch: aus)
- Memory-Palast-NPCs als interaktive Wissensagenten
- KI-Integration (await gpt.decide(...).then(send))

