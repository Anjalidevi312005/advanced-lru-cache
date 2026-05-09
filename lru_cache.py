import threading
import time


class Node:
    def __init__(self, key, value, expiry=None):
        self.key = key
        self.value = value
        self.expiry = expiry
        self.prev = None
        self.next = None


class AdvancedLRUCache:
    def __init__(self, capacity):
        self.capacity = capacity
        self.cache = {}
        self.lock = threading.Lock()

        # Dummy nodes
        self.left = Node(0, 0)   # Least Recently Used
        self.right = Node(0, 0)  # Most Recently Used
        self.left.next = self.right
        self.right.prev = self.left

        # Stats
        self.hits = 0
        self.misses = 0

    def _remove(self, node):
        prev_node = node.prev
        next_node = node.next

        prev_node.next = next_node
        next_node.prev = prev_node

    def _insert(self, node):
        prev_node = self.right.prev

        prev_node.next = node
        node.prev = prev_node
        node.next = self.right
        self.right.prev = node

    def put(self, key, value, ttl=None):
        with self.lock:
            if key in self.cache:
                self._remove(self.cache[key])

            expiry = time.time() + ttl if ttl else None
            node = Node(key, value, expiry)

            self.cache[key] = node
            self._insert(node)

            if len(self.cache) > self.capacity:
                lru = self.left.next
                self._remove(lru)
                del self.cache[lru.key]

    def get(self, key):
        with self.lock:
            if key not in self.cache:
                self.misses += 1
                return -1

            node = self.cache[key]

            # Check expiration
            if node.expiry and time.time() > node.expiry:
                self._remove(node)
                del self.cache[key]
                self.misses += 1
                return -1

            self._remove(node)
            self._insert(node)

            self.hits += 1
            return node.value

    def delete(self, key):
        with self.lock:
            if key in self.cache:
                self._remove(self.cache[key])
                del self.cache[key]

    def clear(self):
        with self.lock:
            self.cache.clear()

            self.left.next = self.right
            self.right.prev = self.left

    def stats(self):
        total = self.hits + self.misses
        hit_ratio = self.hits / total if total else 0

        return {
            "hits": self.hits,
            "misses": self.misses,
            "hit_ratio": round(hit_ratio, 2)
        }