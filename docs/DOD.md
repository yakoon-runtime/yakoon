
## Workflow v1 – Definition of Done

1. **Einheitliches Run-Modell**

* Jeder Workflow-Start erzeugt `run_id` + `batch_id`.
* Jeder Step-Command trägt `run_id`, `step_id`, `batch_id`.
* Subflows laufen im **gleichen Session-Kontext** und haben `parent_run_id`.

**Test:** `wf.status` zeigt run/step/batch/parent konsistent.

2. **Kleines Step-Vokabular**
   Unterstützt sind genau:

* `input_group` (fields + actions)
* `decision` (branch key)
* `run` (execute)
* `subflow` (call)
* `end` (ok/cancel/fail)

**Test:** Es gibt keine “while”/“for” als eigene Syntax. Loops sind Transitions.

3. **Deterministischer Compiler (Mode-abhängig)**

* Default `mode=prompt`: `input_group` → FieldPromptCommands (1 Feld pro Command)
* `mode=form`: `input_group` → FormPromptCommand (ein Command)
* `wizard` ist optional v1; wenn drin, muss er deterministisch sein (z. B. max_fields pro page)

**Test:** Gleicher Workflow + gleicher Mode ⇒ identische Queue-Sequenz.

4. **PromptSpec als Datenvertrag**
   Ein Prompt liefert **strukturierte** Daten:

* fields (key, label, required, default, validate-hints)
* actions (ok/cancel/…)
* optional presentation hints (title, focus, hide_prompt)

**Test:** Console und Kivy können denselben PromptSpec verarbeiten (degraded UI okay).

5. **Antworten sind mergebar**

* Prompt-Antworten können **partial** sein.
* Engine merged in `run.values`.
* Step gilt als “done”, wenn required fields gesetzt + action gewählt (falls nötig).

**Test:** Form kann alles auf einmal schicken; Console feldweise. Ergebnis identisch.

6. **Validation ist Engine-verbindlich**

* Regeln (min/regex/required/custom) werden *mindestens* in der Engine geprüft.
* Bei Fehler: Step bleibt aktiv, Engine liefert errors + missing.

**Test:** falsche PLZ führt reproduzierbar zu re-prompt (egal welcher Host).

7. **Workflow Inspector Commands**
   Mindestens:

* `wf.status` (current step, pending prompt, last result)
* `wf.values` (redacted, optional)
* `wf.trace` (step history, durations, outcomes)

**Test:** Bei jedem Bug lässt sich ohne UI nachvollziehen, was passiert ist.

8. **Cancel/Abort ist sauber**

* Jede Eingabephase bietet cancel (wenn workflow so definiert).
* Cancel beendet Run deterministisch und leert/stoppt weitere geplante Steps im Batch.

**Test:** Cancel hinterlässt keinen “Zombie”-Workflow in Queue oder Session.

---

## Anti-Patterns (bewusst verbieten)

1. **Output-parsing als Logik**

> “cmd_if liest Textausgabe von cmd1 und entscheidet …”
> Verboten. Entscheidungen lesen nur `run.values` oder standardisierte `result`.

2. **Freiform-Expressions (eval)**
   Keine Python/JS-Ausdrücke im YAML.
   Wenn Bedingungen nötig sind: kleines, sicheres Condition-Vokabular (`equals`, `exists`, `matches`, `in`).

3. **UI-Widget-Referenzen im Workflow**
   Kein “Button”, “TextInput”, “Layout”.
   Nur `fields/actions/hints`. Host entscheidet Darstellung.

4. **Workflows, die Mode wechseln**
   Innerhalb eines Runs bleibt der effective mode stabil (außer explizit erlaubt).
   Sonst fühlt sich alles nach “UI-Update” an.

5. **Queue mit “beiden Branches vorausplanen”**
   Nur den nächsten Step enqueuen.
   Sonst müsste später Branch-Cleanup implementiert werden.

---

## Ein pragmatischer v1-Scope (damit ihr nicht ausufert)

* `wizard` als eigener Mode.
* Bedingungen nur über `decision` + “last_result / values”.
* Subflow “call + join” nur mit `end.ok/cancel/fail`.

---

