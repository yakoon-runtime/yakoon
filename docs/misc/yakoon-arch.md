# 1️⃣ Die tatsächliche Architektur (wie sie real läuft)

Der entscheidende Punkt ist hier: 

In `Runner.drive()` passiert Folgendes:

1. Exit-Signal prüfen
2. `dialogs.is_waiting(session)` prüfen
3. Falls waiting → `host.on_prompt(...)`
4. Sonst Queue drain (`queue.next_input`)
5. Falls nichts → `host.on_ready(...)`

Das heißt:

> Der Runner ist unsere State-Maschine.
> Nicht der Command-Return.

---

# 2️⃣ Warum CommandResult hier stören würde

Weil eure Architektur bereits diese drei Dinge sauber trennt:

| Mechanismus           | Zuständig für      |
| --------------------- | ------------------ |
| `session.emit()`      | Output             |
| `CommandQueueService` | Control Flow       |
| `DialogService`       | Input-Wartezustand |
| `Session signals`     | Lifecycle (exit)   |

Ein `return` aus `Command.run()` würde:

* einen zweiten Steuerkanal einführen
* nicht vom Runner ausgewertet werden
* nur semantisch doppeln, was DialogService bereits weiß

Ihr habt bereits einen State-Kanal:
`dialogs.is_waiting(session)`

Das ist euer „NeedInput“.

---

# 3️⃣ Was jetzt für FormMode wirklich nötig ist

Nicht CommandResult.
Sondern:

## DialogService muss unterscheiden können:

Heute:

```python
if dialogs.is_waiting(session):
    mode = dialogs.get_mode(session)
    prompt = format_prompt(session)
    await host.on_prompt(prompt=prompt, mode=mode)
```

Das ist Wizard-zentriert.

Für FormMode brauchst du:

```python
if dialogs.is_waiting(session):
    mode = dialogs.get_mode(session)

    if mode == InteractionMode.WIZARD:
        prompt = format_prompt(session)
        await host.on_prompt(prompt=prompt, mode=mode)

    elif mode == InteractionMode.FORM:
        spec = dialogs.get_form_spec(session)
        await host.on_form(spec=spec)
```

Das ist alles.

Keine Returns. Keine neue Steuerlogik.

---

# 4️⃣ Warum eure Queue-Architektur perfekt dazu passt

Euer `_CmdWorkflowStart` macht:

```python
batch_id = wf.start(...)
wf.enqueue_next(...)
```

Dann:

Runner → queue.next_input() → engine.dispatch()

Das ist exakt das „run-until-blocked“-Modell, nur implizit umgesetzt.

Wenn ein Workflow-Command irgendwann:

```python
dialogs.wait_for_input(session, spec)
```

setzt, dann:

* `dialogs.is_waiting(session)` wird True
* Runner stoppt
* Host wird informiert
* Kein weiterer Queue-Drain

Das ist korrekt.

---

# 5️⃣ Was konkret ergänzt werden muss

Nur zwei Dinge:

## A) DialogService bekommt FormSpec-Unterstützung

Heute speichert er vermutlich:

* prompt_text
* mode (secret/normal)

Er braucht zusätzlich:

* interaction_mode (wizard/form)
* optional: form_spec

Also z.B.:

```python
dialogs.wait_for_input(
    session,
    interaction_mode=InteractionMode.FORM,
    form_spec=NeedInputSpec(...)
)
```

---

## B) HostAdapter bekommt optional `on_form(...)`

ConsoleHost () würde das ignorieren oder in Wizard übersetzen.

KivyHost implementiert:

```python
async def on_form(self, *, spec):
    render_form(spec)
```

Mehr nicht.

---

# 6️⃣ Der große Vorteil eures Designs

Viele Systeme brauchen:

* CommandResult
* Futures
* Awaitable chains
* Complex Flow Control

Ihr habt:

> Queue + DialogState + Pump

Das ist robuster.

Ihr seid näher an einem EventLoop-Kernel als an einem RPC-System.

Das ist ein gutes Fundament für eine Textengine mit UI-Fähigkeit.

---

# 7️⃣ Dein Bild ist korrekt

Ja:

* Workflows steuern Ablauf
* DialogService signalisiert Blockierung
* Session.emit streamt Output
* InteractionMode entscheidet nur über Darstellungsform
* FormSpec ist nur eine andere Art von „waiting“

Und:

> UI ist nur Renderer.

Das ist architektonisch sauber.

---

# 8️⃣ Ich würde nur eine Sache formalisieren

Definiere offiziell:

```python
class DialogState(Enum):
    IDLE
    WAITING_WIZARD
    WAITING_FORM
```

Nicht nur `is_waiting()`, sondern auch Art des Wartens.

Damit wird `Runner.drive()` klarer und später erweiterbar (z.B. CONFIRMATION, FILE_UPLOAD etc.).

---
