
# MASTER-TODO's
- System für Industrie - Command-Strukturen mit KI
    - Automatisierung (Rechnungen, PPX, Mails, Produktionsabläufe....)
    - Projekte ("Erstelle Neues Projekt X", "Lade Projekt X")
    - Dokumentiere (Zugriff auf Lokale Version.)
    
---    
## Text To Speach
🎧 TTS-Anbieter (später)
- ElevenLabs – sehr natürlich, API-basiert
- Google Cloud TTS
- OpenTTS – lokal, Open Source
- OpenAI `whisper-1` für Speech-to-Text
- Eine TTS-Engine wäre der natürliche nächste Schritt für immersive, gesprochene Welten.
Und durch den RendererService kann ich diese einfach einhängen wie jede andere Engine.

def render(self, ctx: RenderContext, section: RenderSection) -> str:
    text = super().render(ctx, section)  # z. B. via Jinja
    play_audio(text)  # wandelt Text in gesprochene Sprache
    return text  # oder leer, wenn keine Ausgabe nötig ist

---
## Scripting
- Scriptdateien (scripts/goblin.txt)
    @script teleport_test:
    login testuser
    ic testuser
    teleport #101
    look
    get box

await engine.dispatch(npc_session, "say Wer wagt es, mein Lager zu betreten?")
await engine.dispatch(npc_session, "attack stefan")
await engine.dispatch(npc_session, "look")

- Reaktive Trigger (→ bei player enters, führe batch: aus)
- Memory-Palast-NPCs als interaktive Wissensagenten
- KI-Integration (await gpt.decide(...).then(send))

---
### 🎙️ **Voice Interface (Audio Commands)**
Yakoon wird in Zukunft Sprache als Eingabemodus unterstützen.
Gesprochene Anweisungen werden per Whisper-API in Text umgewandelt und in Commands
übersetzt.

**Bestandteile:**
* `CmdTranscribeAudio`: nimmt Audiodateien entgegen und transkribiert sie
* `CmdInterpret`: analysiert den transkribierten Text semantisch (Intent, Argumente)
* `CmdExecuteIntent`: führt passende Commands mit erkannten Parametern aus

**Ziel:**
> Bedienung der gesamten Plattform per Sprache – z. B.:
>
> „Starte Projekt MindDojo“
> → wird zu `create project domain=realm name=MindDojo`

**Technologie:**
* OpenAI `whisper-1` für Speech-to-Text
* GPT (optional) für Intent-Mapping
* Standard-Commands für Ausführung

