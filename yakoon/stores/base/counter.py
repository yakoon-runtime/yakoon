from abc import ABC, abstractmethod

class BaseCounterStore(ABC):
    
    @abstractmethod
    async def increment_and_get(self, key: str) -> int:
        """
        Atomically increments the counter for the given key and returns the new value.
        """
        pass

    @abstractmethod
    async def get_shard_stats(self, prefix: str) -> dict:
        """
        Returns a mapping of shard_id -> current_value for the given prefix.
        """
        pass