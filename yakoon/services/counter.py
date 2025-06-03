from yakoon.models.key import Key
from yakoon.models.namespace import Namespace


class ShardedCounterService:

    def __init__(self, store, shard_count: int = 16):
        self.store = store
        self.shard_count = shard_count

    async def get_next_key(self, namespace: Namespace) -> Key:
        """
        Returns the next unique object Key for the given namespace.
        """
        return await self.get_next_id(namespace)

    async def get_next_id(self, namespace: Namespace) -> str:
        """
        Generates the next unique numeric ID (as string) for the given namespace.
        """
        prefix = namespace.get_prefix()
        for attempt in range(self.shard_count):
            shard_id = (attempt + hash(prefix)) % self.shard_count
            key = f"{prefix}:shard:{shard_id}"
            try:
                value = await self.store.increment_and_get(key)
                numeric_id = shard_id * 1_000_000 + value
                return str(numeric_id)
            except Exception:
                continue
        raise RuntimeError("No available shard for ID generation")

    async def get_namespace_stats(self, namespace: Namespace) -> dict:
        """
        Returns a dictionary with shard_id -> current_value for the given namespace.
        Useful for debugging or monitoring ID usage.
        """
        prefix = namespace.get_prefix()
        return await self.store.get_shard_stats(prefix)