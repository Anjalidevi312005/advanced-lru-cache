import time
from lru_cache import AdvancedLRUCache

cache = AdvancedLRUCache(2)

print("Adding values...")
cache.put(1, "Apple")
cache.put(2, "Banana")

print(cache.get(1))   # Apple

cache.put(3, "Orange")

print(cache.get(2))   # -1 (evicted)
print(cache.get(3))   # Orange

print("\nTesting TTL...")
cache.put(4, "Temporary", ttl=3)

print(cache.get(4))   # Temporary

time.sleep(4)

print(cache.get(4))   # -1 expired

print("\nStats:")
print(cache.stats())