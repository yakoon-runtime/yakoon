- Wollen wir die Services wirklich in gamedefinition halten?
  - Warum nicht einfach die Stores importieren? 
  ->> GameDef nicht nicht weiter als Containers missbraucht.
- Protocols?

- CmdTime -> FÜr Zeitstruktur & später Welt
    - Wie setzen wir das um:  2x, 4x Time?
    - Dann legen wir die timephase fest

- Dann Permissions.

- CmdInventory
- CmdGet, CmdPut 

- Dann --init game...


wäre es nicht besse ein on_before_run_command on_after_run_command zu haben.

Hier könnten wir eher eingreifen, dann nach resolve ist der Zustand auf das System
ja noch nicht verändert. Erst durch das command.run?