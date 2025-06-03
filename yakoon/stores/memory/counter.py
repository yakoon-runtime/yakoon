
from collections import defaultdict


class InMemoryCounterStore:

    def __init__(self):
        self._counters = defaultdict(int)

    async def increment_and_get(self, key: str) -> int:
        self._counters[key] += 1
        return self._counters[key]
    
    async def get_shard_stats(self, prefix: str) -> dict:
        result = {}
        for key, value in self._counters.items():
            if key.startswith(f"{prefix}:shard:"):
                shard_id = int(key.rsplit(":", 1)[-1])
                result[shard_id] = value
        return result