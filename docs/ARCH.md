
**Drei Invarianten wie ein Prompt läuft:**
1. Ein Dispatch läuft, bis ein Prompt wartet oder der Command fertig ist.
2. Prompt-Antworten führen denselben Command weiter.
3. Nach jedem Dispatch gibt es genau einen Abschluss-Yield.