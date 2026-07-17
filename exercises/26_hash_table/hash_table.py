"""Exercise 26: Hash Table.

A hash table built from scratch with separate chaining, to see what dict
does under the hood -- then a comparison against the real thing.
"""


class HashTable:
    def __init__(self, capacity: int = 8) -> None:
        self._capacity = capacity
        self._size = 0
        self._buckets: list[list[tuple[str, int]]] = [[] for _ in range(capacity)]

    def _bucket_index(self, key: str) -> int:
        # Python's built-in hash() is randomized per-process for str by
        # default (hash randomization, a security hardening measure) --
        # fine here since we only need consistency within one run.
        return hash(key) % self._capacity

    def _maybe_resize(self) -> None:
        # Keep the average chain length low: resize once load factor > 0.75.
        if self._size / self._capacity <= 0.75:
            return
        old_buckets = self._buckets
        self._capacity *= 2
        self._buckets = [[] for _ in range(self._capacity)]
        self._size = 0
        for bucket in old_buckets:
            for key, value in bucket:
                self.put(key, value)

    def put(self, key: str, value: int) -> None:
        index = self._bucket_index(key)
        bucket = self._buckets[index]
        for i, (existing_key, _) in enumerate(bucket):
            if existing_key == key:
                bucket[i] = (key, value)  # overwrite
                return
        bucket.append((key, value))
        self._size += 1
        self._maybe_resize()

    def get(self, key: str) -> int:
        index = self._bucket_index(key)
        for existing_key, value in self._buckets[index]:
            if existing_key == key:
                return value
        raise KeyError(key)

    def remove(self, key: str) -> None:
        index = self._bucket_index(key)
        bucket = self._buckets[index]
        for i, (existing_key, _) in enumerate(bucket):
            if existing_key == key:
                del bucket[i]
                self._size -= 1
                return
        raise KeyError(key)

    def __contains__(self, key: str) -> bool:
        index = self._bucket_index(key)
        return any(existing_key == key for existing_key, _ in self._buckets[index])

    def __len__(self) -> int:
        return self._size

    def load_factor(self) -> float:
        return self._size / self._capacity


def word_frequency(text: str) -> HashTable:
    table = HashTable()
    for word in text.lower().split():
        cleaned = word.strip(".,!?;:")
        try:
            table.put(cleaned, table.get(cleaned) + 1)
        except KeyError:
            table.put(cleaned, 1)
    return table


def main() -> None:
    ht = HashTable(capacity=4)
    ht.put("apples", 10)
    ht.put("bananas", 5)
    ht.put("cherries", 20)
    print(f"get('apples') = {ht.get('apples')}")
    print(f"'bananas' in ht: {'bananas' in ht}")
    print(f"len(ht) = {len(ht)}, load_factor = {ht.load_factor():.2f}")

    ht.put("dates", 7)
    ht.put("elderberries", 3)  # triggers a resize past load factor 0.75
    print(f"after 2 more inserts: len = {len(ht)}, load_factor = {ht.load_factor():.2f}")

    ht.remove("bananas")
    print(f"'bananas' in ht after remove: {'bananas' in ht}")

    try:
        ht.get("missing")
    except KeyError as e:
        print(f"KeyError as expected: {e}")

    text = "the quick brown fox jumps over the lazy dog. The dog barks!"
    freq = word_frequency(text)
    print(f"frequency of 'the' = {freq.get('the')}")
    print(f"frequency of 'dog' = {freq.get('dog')}")

    # --- Real code uses dict: implemented in C, open addressing, far faster ---
    d: dict[str, int] = {}
    for word in text.lower().split():
        cleaned = word.strip(".,!?;:")
        d[cleaned] = d.get(cleaned, 0) + 1
    print(f"dict agrees on 'the': {d['the'] == freq.get('the')}")


if __name__ == "__main__":
    main()
