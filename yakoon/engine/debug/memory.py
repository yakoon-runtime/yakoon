import asyncio
import gc
from collections import Counter

class MemoryManager:
    def __init__(self, interval: int = 120):
        self.interval = interval
        self._last_snapshot = Counter()
        self._running = False
        self._task = None

    def start(self, interval: int = None):
        self.interval = interval or self.interval
        if not self._running:
            self._running = True
            self._task = asyncio.create_task(self._run())

    def stop(self):
        self._running = False
        if self._task:
            self._task.cancel()

    async def _run(self):
        while self._running:
            await asyncio.sleep(self.interval)
            self._report_if_changed()

    def _snapshot(self) -> Counter:
        gc.collect()
        return Counter(type(obj).__name__ for obj in gc.get_objects())

    def _report_if_changed(self):
        current = self._snapshot()
        diff = {
            key: current[key] - self._last_snapshot.get(key, 0)
            for key in current
        }
        changed = {k: v for k, v in diff.items() if v != 0}

        if changed:
            print("\n[MemoryManager] changes:")
            for typename in sorted(changed, key=lambda k: abs(changed[k]), reverse=True)[:10]:
                delta = changed[typename]
                arrow = "⬆️" if delta > 0 else "⬇️"
                print(f"{typename:20} {current[typename]:5} ({delta:+}) {arrow}")

        self._last_snapshot = current


mem_monitor = MemoryManager()